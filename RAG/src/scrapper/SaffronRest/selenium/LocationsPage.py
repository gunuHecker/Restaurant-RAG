from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def get_html_from_saffron(output_path="data/raw/saffron/locationsPage.html"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://saffronrestaurant.co.in/locations/"
        driver.get(url)
        time.sleep(5)
        html_content = driver.page_source

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[✓] HTML content saved to {output_path}")

    except Exception as e:
        print(f"[✗] Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    get_html_from_saffron()
