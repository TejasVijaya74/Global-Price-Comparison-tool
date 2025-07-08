
"""
Scraping Engine - Core component for fetching prices from multiple websites
"""
import asyncio
import time
import random
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import re

import aiohttp
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential

from database import SessionLocal
from models import Vendor, Country, ScrapingLog

logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Configuration for scraping operations"""
    max_concurrent_requests: int = 5
    request_delay_min: float = 1.0
    request_delay_max: float = 3.0
    timeout: int = 30
    max_retries: int = 3
    use_selenium: bool = False
    respect_robots_txt: bool = True

class VendorScraper:
    """Base class for vendor-specific scrapers"""

    def __init__(self, vendor_config: Dict):
        self.vendor_config = vendor_config
        self.name = vendor_config["name"]
        self.base_url = vendor_config["base_url"]
        self.selectors = vendor_config.get("selectors", {})
        self.search_url_pattern = vendor_config.get("search_url_pattern", "")

    async def search_products(self, query: str, session: aiohttp.ClientSession) -> List[Dict]:
        """Search for products on this vendor"""
        try:
            search_url = self._build_search_url(query)
            products = await self._scrape_search_results(search_url, session)
            return products
        except Exception as e:
            logger.error(f"Error scraping {self.name}: {str(e)}")
            return []

    def _build_search_url(self, query: str) -> str:
        """Build search URL from query"""
        if self.search_url_pattern:
            return self.search_url_pattern.format(query=query.replace(" ", "+"))
        return f"{self.base_url}/search?q={query.replace(' ', '+')}"

    async def _scrape_search_results(self, url: str, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape search results from URL"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_search_results(html, url)
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return []

    def _parse_search_results(self, html: str, base_url: str) -> List[Dict]:
        """Parse HTML and extract product information"""
        soup = BeautifulSoup(html, 'html.parser')
        products = []

        # Generic parsing logic - override in specific scrapers
        product_containers = soup.find_all('div', class_=['product', 'item', 'result'])

        for container in product_containers[:20]:  # Limit to first 20 results
            try:
                product = self._extract_product_info(container, base_url)
                if product:
                    products.append(product)
            except Exception as e:
                logger.debug(f"Error parsing product container: {str(e)}")
                continue

        return products

    def _extract_product_info(self, container, base_url: str) -> Optional[Dict]:
        """Extract product information from container"""
        try:
            # Generic extraction logic
            name_elem = container.find(['h1', 'h2', 'h3', 'h4'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['title', 'name', 'product']
            ))

            price_elem = container.find(['span', 'div'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['price', 'cost', 'amount']
            ))

            link_elem = container.find('a', href=True)

            if not all([name_elem, price_elem, link_elem]):
                return None

            # Extract and clean data
            name = name_elem.get_text(strip=True)
            price_text = price_elem.get_text(strip=True)
            link = urljoin(base_url, link_elem['href'])

            # Extract price number
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
            if not price_match:
                return None

            price = float(price_match.group().replace(',', ''))

            # Extract currency
            currency_match = re.search(r'[£$€¥₹]|USD|EUR|GBP|INR|JPY', price_text)
            currency = self._normalize_currency(currency_match.group() if currency_match else '$')

            return {
                'name': name,
                'price': price,
                'currency': currency,
                'url': link,
                'vendor': self.name,
                'availability': 'in_stock'
            }

        except Exception as e:
            logger.debug(f"Error extracting product info: {str(e)}")
            return None

    def _normalize_currency(self, currency_symbol: str) -> str:
        """Normalize currency symbols to codes"""
        currency_map = {
            '$': 'USD', '£': 'GBP', '€': 'EUR', '¥': 'JPY', '₹': 'INR',
            'USD': 'USD', 'EUR': 'EUR', 'GBP': 'GBP', 'INR': 'INR', 'JPY': 'JPY'
        }
        return currency_map.get(currency_symbol, 'USD')

class AmazonScraper(VendorScraper):
    """Amazon-specific scraper"""

    def _build_search_url(self, query: str) -> str:
        # Amazon search URL pattern
        return f"{self.base_url}/s?k={query.replace(' ', '+')}"

    def _parse_search_results(self, html: str, base_url: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        products = []

        # Amazon-specific selectors
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})

        for container in product_containers[:15]:
            try:
                # Title
                title_elem = container.find('h2').find('a')
                if not title_elem:
                    continue

                name = title_elem.get_text(strip=True)
                link = urljoin(base_url, title_elem['href'])

                # Price
                price_elem = container.find('span', class_='a-price-whole')
                if not price_elem:
                    continue

                price_text = price_elem.get_text(strip=True).replace(',', '')
                price = float(price_text) if price_text.isdigit() else 0

                if price > 0:
                    products.append({
                        'name': name,
                        'price': price,
                        'currency': 'USD',  # Default, should be detected based on domain
                        'url': link,
                        'vendor': self.name,
                        'availability': 'in_stock'
                    })

            except Exception as e:
                logger.debug(f"Error parsing Amazon product: {str(e)}")
                continue

        return products

class ScrapingEngine:
    """Main scraping engine that coordinates multiple vendor scrapers"""

    def __init__(self, config: Optional[ScrapingConfig] = None):
        self.config = config or ScrapingConfig()
        self.user_agent = UserAgent()
        self.vendor_scrapers = {}
        self._load_vendor_configs()

    def _load_vendor_configs(self):
        """Load vendor configurations for different countries"""
        # This would typically be loaded from a database or config file
        vendor_configs = {
            'US': [
                {
                    'name': 'Amazon US',
                    'base_url': 'https://www.amazon.com',
                    'scraper_class': AmazonScraper,
                    'rate_limit': 60
                },
                {
                    'name': 'eBay US',
                    'base_url': 'https://www.ebay.com',
                    'scraper_class': VendorScraper,
                    'search_url_pattern': 'https://www.ebay.com/sch/i.html?_nkw={query}',
                    'rate_limit': 100
                },
                {
                    'name': 'Walmart',
                    'base_url': 'https://www.walmart.com',
                    'scraper_class': VendorScraper,
                    'search_url_pattern': 'https://www.walmart.com/search?q={query}',
                    'rate_limit': 50
                }
            ],
            'IN': [
                {
                    'name': 'Amazon India',
                    'base_url': 'https://www.amazon.in',
                    'scraper_class': AmazonScraper,
                    'rate_limit': 60
                },
                {
                    'name': 'Flipkart',
                    'base_url': 'https://www.flipkart.com',
                    'scraper_class': VendorScraper,
                    'search_url_pattern': 'https://www.flipkart.com/search?q={query}',
                    'rate_limit': 40
                }
            ]
        }

        for country, vendors in vendor_configs.items():
            self.vendor_scrapers[country] = []
            for vendor_config in vendors:
                scraper_class = vendor_config.pop('scraper_class', VendorScraper)
                scraper = scraper_class(vendor_config)
                self.vendor_scrapers[country].append(scraper)

    async def search_products(self, country: str, query: str) -> List[Dict]:
        """Search for products across all vendors in a country"""
        start_time = time.time()

        if country.upper() not in self.vendor_scrapers:
            raise ValueError(f"Country {country} not supported")

        scrapers = self.vendor_scrapers[country.upper()]

        # Create aiohttp session with proper configuration
        connector = aiohttp.TCPConnector(limit=self.config.max_concurrent_requests)
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        headers = {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        ) as session:
            # Create tasks for concurrent scraping
            tasks = []
            for scraper in scrapers:
                task = asyncio.create_task(
                    self._scrape_with_delay(scraper, query, session)
                )
                tasks.append(task)

            # Execute all scraping tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine and clean results
        all_products = []
        for result in results:
            if isinstance(result, list):
                all_products.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Scraping task failed: {str(result)}")

        end_time = time.time()
        logger.info(f"Scraped {len(all_products)} products in {end_time - start_time:.2f}s")

        return all_products

    async def _scrape_with_delay(self, scraper: VendorScraper, query: str, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape with random delay to avoid rate limiting"""
        delay = random.uniform(self.config.request_delay_min, self.config.request_delay_max)
        await asyncio.sleep(delay)

        return await scraper.search_products(query, session)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _make_request_with_retry(self, session: aiohttp.ClientSession, url: str) -> str:
        """Make HTTP request with retry logic"""
        async with session.get(url) as response:
            if response.status == 429:  # Rate limited
                retry_after = int(response.headers.get('Retry-After', 60))
                await asyncio.sleep(retry_after)
                raise Exception("Rate limited, retrying...")

            response.raise_for_status()
            return await response.text()
