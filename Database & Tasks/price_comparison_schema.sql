
-- Price Comparison Tool Database Schema

-- Countries table
CREATE TABLE countries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(3) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    exchange_rate DECIMAL(10,6) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table (hierarchical)
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- Vendors table
CREATE TABLE vendors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    base_url VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    api_endpoint VARCHAR(255) NULL,
    rate_limit INT DEFAULT 60,
    rate_period INT DEFAULT 3600,
    is_active BOOLEAN DEFAULT TRUE,
    scraping_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    sku VARCHAR(100),
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    INDEX idx_normalized_name (normalized_name),
    INDEX idx_brand_model (brand, model)
);

-- Prices table
CREATE TABLE prices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    vendor_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    original_price DECIMAL(10,2) NULL,
    discount_percentage DECIMAL(5,2) NULL,
    availability VARCHAR(50) DEFAULT 'in_stock',
    product_url VARCHAR(500) NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    INDEX idx_product_vendor (product_id, vendor_id),
    INDEX idx_scraped_at (scraped_at),
    INDEX idx_current_prices (is_current, product_id)
);

-- Product matching table
CREATE TABLE product_matches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id_1 INT NOT NULL,
    product_id_2 INT NOT NULL,
    confidence_score DECIMAL(3,2) NOT NULL,
    algorithm_used VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id_1) REFERENCES products(id),
    FOREIGN KEY (product_id_2) REFERENCES products(id),
    UNIQUE KEY unique_match (product_id_1, product_id_2)
);

-- Scraping logs table
CREATE TABLE scraping_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_id INT NOT NULL,
    status ENUM('success', 'error', 'rate_limited', 'blocked') NOT NULL,
    products_found INT DEFAULT 0,
    error_message TEXT NULL,
    response_time_ms INT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    INDEX idx_vendor_timestamp (vendor_id, timestamp)
);

-- API rate limiting table
CREATE TABLE api_rate_limits (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_id INT NOT NULL,
    api_key VARCHAR(255) NULL,
    requests_made INT DEFAULT 0,
    rate_limit_remaining INT DEFAULT 1000,
    reset_time TIMESTAMP NULL,
    last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);
