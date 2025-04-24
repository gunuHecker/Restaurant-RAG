import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
# from langchain.llms import OpenAI
from transformers import pipeline
from huggingface_hub import InferenceClient
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional

import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

class HFInferenceClientLLM(LLM):
    """LangChain LLM wrapper around huggingface_hub.InferenceClient.chat.completions."""
    
    client: InferenceClient
    model: str
    max_tokens: int = 256
    temperature: float = 0.7

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model, "max_tokens": self.max_tokens, "temperature": self.temperature}

    @property
    def _llm_type(self) -> str:
        return "hf-inference-client"


# Streamlit UI
st.set_page_config(page_title="Restaurant RAG Chatbot", layout="wide")
st.title("Zomato Restaurant RAG Chatbot")

@st.cache_resource
# Load and vectorize documents
def load_vectorstore():
    loader = TextLoader("data/processed/text/combined_restaurants.txt", encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = loader.load_and_split(splitter)
    # Use a local embedding model
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vs = FAISS.from_documents(docs, embeddings)
    return vs

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

@st.cache_resource
# Initialize HuggingFaceHub LLM and custom prompt
def get_llm_and_prompt():
    client = InferenceClient(provider="nebius", api_key=HUGGINGFACEHUB_API_TOKEN)
    llm = HFInferenceClientLLM(
        client=client,
        model="Qwen/Qwen2.5-1.5B-Instruct",
        max_tokens=512,
        temperature=0.7,
    )
    prompt = PromptTemplate(
        template="""You are a helpful assistant.
            Answer ONLY from the provided restaurant context.
            If the context is insufficient, just say you don't know.

            {context}
            Question: {question}""",
        input_variables=["context", "question"],
    )
    
    return llm, prompt

llm, prompt = get_llm_and_prompt()

# === RAG Runnable Pipeline Setup ===
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

parallel_chain = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough(),
})

parser = StrOutputParser()

main_chain = parallel_chain | prompt | llm | parser

# User query
query = st.text_input("Ask a question about our restaurants:")
if query:
    with st.spinner("Retrieving answer..."):
        answer = main_chain.invoke(query)
    st.write(answer)