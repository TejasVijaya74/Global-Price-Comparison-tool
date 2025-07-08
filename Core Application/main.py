
"""
Price Comparison Tool - Main FastAPI Application
"""
import os
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from datetime import datetime

from database import SessionLocal, init_db
from models import Product, Price, Vendor, Country
from scraping_engine import ScrapingEngine
from product_matcher import ProductMatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Price Comparison Tool",
    description="A generic tool to fetch product prices from multiple websites across countries",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Database initialized")

# Pydantic models for API requests/responses
class ProductSearchRequest(BaseModel):
    country: str
    query: str

class PriceResponse(BaseModel):
    link: str
    price: str
    currency: str
    productName: str
    vendor: str
    availability: str = "in_stock"
    originalPrice: Optional[str] = None
    discountPercentage: Optional[float] = None

class ProductSearchResponse(BaseModel):
    products: List[PriceResponse]
    total_results: int
    search_time_ms: int
    country: str
    query: str

# Global instances
scraping_engine = ScrapingEngine()
product_matcher = ProductMatcher()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Price Comparison Tool API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "search": "/search?country={country}&query={query}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.post("/search", response_model=ProductSearchResponse)
async def search_products(
    request: ProductSearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Main endpoint to search for products across multiple vendors
    """
    start_time = datetime.now()

    try:
        # Run scraping process
        results = await scraping_engine.search_products(
            country=request.country,
            query=request.query
        )

        # Process and match products
        matched_products = product_matcher.match_and_deduplicate(results)

        # Convert to response format
        price_responses = []
        for product in matched_products:
            price_responses.append(PriceResponse(
                link=product["url"],
                price=str(product["price"]),
                currency=product["currency"],
                productName=product["name"],
                vendor=product["vendor"],
                availability=product.get("availability", "in_stock"),
                originalPrice=str(product.get("original_price")) if product.get("original_price") else None,
                discountPercentage=product.get("discount_percentage")
            ))

        # Sort by price (ascending)
        price_responses.sort(key=lambda x: float(x.price))

        end_time = datetime.now()
        search_time_ms = int((end_time - start_time).total_seconds() * 1000)

        # Store results in database (background task)
        background_tasks.add_task(
            store_search_results,
            request.country,
            request.query,
            matched_products
        )

        return ProductSearchResponse(
            products=price_responses,
            total_results=len(price_responses),
            search_time_ms=search_time_ms,
            country=request.country,
            query=request.query
        )

    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search", response_model=ProductSearchResponse)
async def search_products_get(
    country: str = Query(..., description="Country code (e.g., US, IN, UK)"),
    query: str = Query(..., description="Product search query"),
    background_tasks: BackgroundTasks = None
):
    """
    GET endpoint for product search (for easy testing)
    """
    request = ProductSearchRequest(country=country, query=query)
    return await search_products(request, background_tasks)

@app.get("/vendors/{country}")
async def get_vendors_by_country(country: str):
    """Get all active vendors for a specific country"""
    db = SessionLocal()
    try:
        vendors = db.query(Vendor).join(Country).filter(
            Country.code == country.upper(),
            Vendor.is_active == True
        ).all()

        return [
            {
                "id": vendor.id,
                "name": vendor.name,
                "base_url": vendor.base_url,
                "rate_limit": vendor.rate_limit
            }
            for vendor in vendors
        ]
    finally:
        db.close()

@app.get("/countries")
async def get_supported_countries():
    """Get all supported countries"""
    db = SessionLocal()
    try:
        countries = db.query(Country).all()
        return [
            {
                "code": country.code,
                "name": country.name,
                "currency": country.currency
            }
            for country in countries
        ]
    finally:
        db.close()

async def store_search_results(country: str, query: str, products: List[dict]):
    """Background task to store search results in database"""
    db = SessionLocal()
    try:
        # Implementation for storing results
        logger.info(f"Storing {len(products)} products from search: {query} in {country}")
        # Add database storage logic here
    except Exception as e:
        logger.error(f"Error storing search results: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
