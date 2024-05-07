from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from price_comparison_scraping import scrape_product_data
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv('PRICE_COMP_OPENAI_API')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class ProductQuery(BaseModel):
    product_name: str

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

@app.get("/search")
async def search(product_name: str = Query(None, description="The name of the product to search for")):
    if product_name:
        try:
            results = scrape_product_data(product_name)
            recommendation = get_recommendation(api_key, product_name)["choices"][0]["message"]["content"]
            print(recommendation)
            #delete "data": results, "recommendation": recommendation for debugging
            return {"data": results, "recommendation": recommendation}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"detail": "Product name is required"}

if __name__ == "__main__":
    # Run the API with uvicorn
    #changed from uvicorn.run(app, host="127.0.0.1....""
    uvicorn.run(app, host="0.0.0.0", port=8090)
