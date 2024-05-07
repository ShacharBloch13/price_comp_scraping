from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('PRICE_COMP_OPENAI_API')
UA_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"]

def get_user_agent():
    """Returns a random user agent string."""
    return random.choice(UA_list)



def get_recommendation(api_key, product_name):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    body = json.dumps({
        'messages': [
            {'role': 'system',
             'content': 'You are an experienced salesperson looking to recommend a product to a customer, based on what he searched before. You are going to want to recommend products that may be related to the product he searched for. Return only 1 product by its name. For example, if someone looked for an acoustic guitar, you may want to recommend a guitar pick, and your response should be "Guitar Pick".'
             },
            {'role': 'user',
             'content': f'I am looking to buy {product_name}. Can you recommend a product for me?'
            }
        ],
        'model': 'gpt-3.5-turbo',
        'temperature': 0.5
    })

    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Looks like your API key is incorrect. Please check your API key and try again.")
        else:
            print(f"Failed to fetch. Status code: {response.status_code}")
    except Exception as err:
        print(f"An error occurred: {err}")

def setup_driver():
    """Configures and returns a Selenium WebDriver."""
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode for automation.
    options.add_argument("--incognito")  # Opens Chrome in incognito mode.
    UA = get_user_agent()
    options.add_argument(f'user-agent={UA}')  # Sets the user agent to avoid bot detection.
    print(f"Using user agent: {UA}")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service('C:\\Users\\user\\Desktop\\Code_Projects\\chromedriver.exe')  # Update the path to where Chromedriver is installed
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def select_country_bestbuy(driver):
    try:
        # Wait and click on the "United States" link
        wait = WebDriverWait(driver, 10)
        us_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'us-link')))
        us_link.click()
        print("Selected country: United States on Best Buy")
    except Exception as e:
        print("Could not select country on Best Buy:", e)



def scrape_product_data(product_name):
    """Scrapes product data from Best Buy, Walmart, and Newegg."""
    driver = setup_driver()
    results = []
    wait = WebDriverWait(driver, 10)
    # Dictionary of sites and their search URL patterns
    sites = {
        'Best Buy': f'https://www.bestbuy.com/site/searchpage.jsp?st={product_name.replace(" ", "+")}',
        'Walmart': f'https://www.walmart.com/search/?query={product_name.replace(" ", "+")}',
        'Newegg': f'https://www.newegg.com/p/pl?d={product_name.replace(" ", "+")}'
    }

    for site, url in sites.items():
        driver.get(url)
        

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        if site == 'Best Buy':
            print(url)
            select_country_bestbuy(driver)
            driver.save_screenshot('debug_screenshot_bestbuy.png')
            best_buy_url = f'https://www.bestbuy.com/site/searchpage.jsp?st={product_name}'
            driver.get(best_buy_url)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h4.sku-title a')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_element = soup.find('h4', class_='sku-title').find('a') if soup.find('h4', class_='sku-title') else None
            price_element = soup.find('div', class_='priceView-hero-price priceView-customer-price').find('span', {"aria-hidden": "true"}) if soup.find('div', class_='priceView-hero-price priceView-customer-price') else None
            url = driver.current_url
   
        elif site == 'Walmart':
            print(url)
            driver.execute_script("window.scrollTo(0, 100)")  # Scroll down to avoid captcha
            driver.save_screenshot('debug_screenshot_walmart.png')
            try:
                product = driver.find_element(By.CSS_SELECTOR, '[data-item-id]')
                product_element = product.find_element(By.CSS_SELECTOR, '[data-automation-id="product-title"]')
                price_element = product.find_element(By.CSS_SELECTOR, '[data-automation-id="product-price"]')

                url = driver.current_url
                print("Product and price fetched from Walmart")
            except Exception as e:
                print("Error fetching from Walmart:", e)
        elif site == 'Newegg':
            print(url)
            driver.save_screenshot('debug_screenshot_newegg.png')
            product_element = soup.find('a', class_='item-title')
            price_element = soup.find('li', class_='price-current')
            url = driver.current_url

        item_title = product_element.text.strip() if product_element else 'Product not found'
        price = price_element.text.strip().split()[0] if price_element else 'Price not found'
        if price != 'Price not found' and len(price) > 2 and "." not in price:
            price = price[:-2] + '.' + price[-2:]
        url = url if url else 'URL not found'

        results.append({
            'Site': site,
            'Item Title Name': item_title,
            'Price(USD)': price,
            'Go to website:': url

        })


    driver.quit()
    return results

# Main function to test the scraping function
if __name__ == "__main__":
    product_name = "iphone 13 case"
    data = scrape_product_data(product_name)
    recommendation_temp = get_recommendation(api_key, product_name)
    recommendation = recommendation_temp['choices'][0]['message']['content']
    print(api_key) # Print the API key to check if it is loaded correctly
    for result in data:
        print(result)
    
