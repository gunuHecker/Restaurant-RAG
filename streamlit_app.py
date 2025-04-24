import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from transformers import pipeline, BitsAndBytesConfig, AutoModelForSeq2SeqLM, AutoTokenizer

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
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

@st.cache_resource
# Initialize HuggingFaceHub LLM and custom prompt
def get_llm_and_prompt():
    # hf_model = pipeline(
    #     model="google/flan-t5-small",
    #     task="text2text-generation",
    #     device=0,
    #     max_new_tokens=64,
    #     # temperature=0.7
    # )
    bnb_config = BitsAndBytesConfig(load_in_8bit=True)
    model_name = "google/flan-t5-large"
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        device_map="auto",
        trust_remote_code=True,
        quantization_config=bnb_config
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True
    )
    hf_model = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=128,
        temperature=0.2
    )

    llm = HuggingFacePipeline(pipeline=hf_model, return_full_text=False)
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
    st.markdown("### Final Answer")
    st.write(answer)