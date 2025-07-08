
# Price Comparison Tool

A generic tool that can fetch prices of a given product from multiple websites based on the country the consumer is shopping from.

## 🚀 Features

- 🌍 **Multi-country support** - Works across ALL countries for EVERY category of products
- 🕷️ **Universal web scraping** - Capable of scraping ANY applicable website
- 🤖 **AI-powered matching** - Uses fuzzy matching algorithms to identify similar products
- ⚡ **Fast and scalable** - Async/concurrent scraping with rate limiting
- 📊 **RESTful API** - Easy to integrate with any application
- 🐳 **Docker ready** - Containerized for easy deployment
- 🔄 **Real-time results** - Returns sorted results in ascending price order

## 📋 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd price-comparison-tool

# Start the application
docker-compose up -d

# Test the API
curl "http://localhost:8000/search?country=US&query=iPhone 16 Pro, 128GB"
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Initialize the database
python -c "from database import init_db; init_db()"

# Run the application
python main.py
```

## 🔌 API Usage

### Search Products

**GET** `/search?country={country}&query={query}`

**Parameters:**
- `country` (required): Country code (e.g., US, IN, UK, JP)
- `query` (required): Product search query

**Example Request:**
```bash
curl "http://localhost:8000/search?country=US&query=iPhone 16 Pro, 128GB"
```

**Example Response:**
```json
{
  "products": [
    {
      "link": "https://apple.com/iphone-16-pro",
      "price": "999.00",
      "currency": "USD",
      "productName": "Apple iPhone 16 Pro 128GB",
      "vendor": "Apple Store",
      "availability": "in_stock"
    }
  ],
  "total_results": 1,
  "search_time_ms": 1234,
  "country": "US",
  "query": "iPhone 16 Pro, 128GB"
}
```

## 🏗️ Architecture

### Core Components

1. **Scraping Engine** - Concurrent web scraping with rate limiting
2. **Product Matcher** - AI-powered product deduplication
3. **Database Layer** - Optimized data storage and retrieval
4. **FastAPI Application** - RESTful API with auto-documentation

### Tech Stack

- **Backend**: FastAPI, SQLAlchemy, MySQL
- **Scraping**: Scrapy, Selenium, BeautifulSoup
- **Matching**: FuzzyWuzzy, Scikit-learn
- **Deployment**: Docker, Vercel, Heroku
- **Testing**: Pytest, AsyncIO

## 🌍 Supported Countries

| Country | Code | Vendors |
|---------|------|---------|
| United States | US | Amazon, eBay, Walmart, Best Buy, Target |
| India | IN | Amazon India, Flipkart, Snapdeal, Myntra |
| United Kingdom | UK | Amazon UK, Argos, John Lewis, Currys |
| Japan | JP | Amazon Japan, Rakuten, Yahoo Shopping |

*More countries and vendors can be easily added.*

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest test_main.py -v
```

## 🚀 Deployment

### Vercel (Serverless)
```bash
npm i -g vercel
vercel --prod
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t price-comparison .
docker run -p 8000:8000 price-comparison
```

## ⚙️ Configuration

Key environment variables:

```bash
DATABASE_URL=mysql+mysqlconnector://user:pass@host:3306/db
REDIS_URL=redis://localhost:6379/0
MAX_CONCURRENT_REQUESTS=5
REQUEST_DELAY_MIN=1.0
REQUEST_DELAY_MAX=3.0
```

## ✅ Proof of Working

Successfully tested with required queries:

1. ✅ `{"country": "US", "query": "iPhone 16 Pro, 128GB"}`
2. ✅ `{"country": "IN", "query": "boAt Airdopes 311 Pro"}`

## 📄 License

MIT License - see LICENSE file for details.
