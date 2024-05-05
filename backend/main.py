from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from price_comparison_scraping import scrape_product_data

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

@app.get("/search")
async def search(product_name: str = Query(None, description="The name of the product to search for")):
    if product_name:
        try:
            results = scrape_product_data(product_name)
            return {"data": results}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"detail": "Product name is required"}

if __name__ == "__main__":
    # Run the API with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
