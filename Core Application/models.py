
"""
SQLAlchemy models for the price comparison tool
"""
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    currency = Column(String(3), nullable=False)
    exchange_rate = Column(DECIMAL(10, 6), default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    vendors = relationship("Vendor", back_populates="country")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    products = relationship("Product", back_populates="category")
    parent = relationship("Category", remote_side=[id])

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    base_url = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    api_endpoint = Column(String(255), nullable=True)
    rate_limit = Column(Integer, default=60)
    rate_period = Column(Integer, default=3600)
    is_active = Column(Boolean, default=True)
    scraping_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    country = relationship("Country", back_populates="vendors")
    prices = relationship("Price", back_populates="vendor")
    scraping_logs = relationship("ScrapingLog", back_populates="vendor")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    normalized_name = Column(String(255), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    sku = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="products")
    prices = relationship("Price", back_populates="product")

    # Indexes
    __table_args__ = (
        Index('idx_brand_model', 'brand', 'model'),
    )

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    original_price = Column(DECIMAL(10, 2), nullable=True)
    discount_percentage = Column(DECIMAL(5, 2), nullable=True)
    availability = Column(String(50), default="in_stock")
    product_url = Column(String(500), nullable=False)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    is_current = Column(Boolean, default=True)

    # Relationships
    product = relationship("Product", back_populates="prices")
    vendor = relationship("Vendor", back_populates="prices")

    # Indexes
    __table_args__ = (
        Index('idx_product_vendor', 'product_id', 'vendor_id'),
        Index('idx_current_prices', 'is_current', 'product_id'),
    )

class ProductMatch(Base):
    __tablename__ = "product_matches"

    id = Column(Integer, primary_key=True, index=True)
    product_id_1 = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_id_2 = Column(Integer, ForeignKey("products.id"), nullable=False)
    confidence_score = Column(DECIMAL(3, 2), nullable=False)
    algorithm_used = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ScrapingLog(Base):
    __tablename__ = "scraping_logs"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    status = Column(String(20), nullable=False)  # success, error, rate_limited, blocked
    products_found = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    vendor = relationship("Vendor", back_populates="scraping_logs")

    # Indexes
    __table_args__ = (
        Index('idx_vendor_timestamp', 'vendor_id', 'timestamp'),
    )

class ApiRateLimit(Base):
    __tablename__ = "api_rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    api_key = Column(String(255), nullable=True)
    requests_made = Column(Integer, default=0)
    rate_limit_remaining = Column(Integer, default=1000)
    reset_time = Column(DateTime(timezone=True), nullable=True)
    last_request = Column(DateTime(timezone=True), server_default=func.now())
