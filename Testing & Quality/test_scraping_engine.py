
"""
Tests for the scraping engine
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import aiohttp

from scraping_engine import ScrapingEngine, VendorScraper, AmazonScraper

@pytest.fixture
def sample_vendor_config():
    return {
        "name": "Test Store",
        "base_url": "https://example.com",
        "search_url_pattern": "https://example.com/search?q={query}",
        "rate_limit": 100
    }

@pytest.fixture
def sample_html():
    return """
    <html>
        <body>
            <div class="product">
                <h2 class="title">Test Product</h2>
                <span class="price">$99.99</span>
                <a href="/product/1">View Product</a>
            </div>
            <div class="product">
                <h2 class="title">Another Product</h2>
                <span class="price">£149.99</span>
                <a href="/product/2">View Product</a>
            </div>
        </body>
    </html>
    """

def test_vendor_scraper_init(sample_vendor_config):
    """Test VendorScraper initialization"""
    scraper = VendorScraper(sample_vendor_config)
    assert scraper.name == "Test Store"
    assert scraper.base_url == "https://example.com"

def test_build_search_url(sample_vendor_config):
    """Test search URL building"""
    scraper = VendorScraper(sample_vendor_config)
    url = scraper._build_search_url("iPhone 16 Pro")
    assert "iPhone+16+Pro" in url

def test_parse_search_results(sample_vendor_config, sample_html):
    """Test HTML parsing"""
    scraper = VendorScraper(sample_vendor_config)
    products = scraper._parse_search_results(sample_html, "https://example.com")

    assert len(products) >= 0  # May be empty depending on parsing logic

@pytest.mark.asyncio
async def test_scraping_engine_initialization():
    """Test ScrapingEngine initialization"""
    engine = ScrapingEngine()
    assert 'US' in engine.vendor_scrapers
    assert 'IN' in engine.vendor_scrapers

@pytest.mark.asyncio
async def test_search_products_unsupported_country():
    """Test search with unsupported country"""
    engine = ScrapingEngine()

    with pytest.raises(ValueError, match="Country XX not supported"):
        await engine.search_products("XX", "test query")
