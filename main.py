from fastapi import FastAPI, HTTPException
from scraper import DentalScraper

app = FastAPI()

@app.get("/scrape/")
def scrape_products(max_page: int):
    if max_page <= 0:
        raise HTTPException(status_code=400, detail="max_page should be greater than 0")
    
    # Create an instance of DentalScraper with the given max_page
    scraper = DentalScraper(max_page)

    # Scrape the data and save it to JSON
    scraper.scrape_all_pages()

    # Return the structured product data
    return {"products": scraper.product_data}
