from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
from price_comparison_scraping import scrape_product_data

app = FastAPI()

class ProductQuery(BaseModel):
    product_name: str

@app.post("/scrape")
async def scrape(product_query: ProductQuery):
    try:
        # Call your existing scrape function
        result = scrape_product_data(product_query.product_name)
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Run the API with uvicorn
    # By default, it will run on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
