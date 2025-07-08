# Create the product matching engine
product_matcher_code = '''
"""
Product Matcher - Uses fuzzy matching to identify similar products across vendors
"""
import re
import logging
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass

import pandas as pd
from fuzzywuzzy import fuzz, process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class MatchConfig:
    """Configuration for product matching"""
    min_similarity_score: float = 0.75
    max_price_difference_percent: float = 50.0
    use_brand_matching: bool = True
    use_price_filtering: bool = True
    normalize_names: bool = True

class ProductNormalizer:
    """Normalizes product names for better matching"""
    
    def __init__(self):
        # Common words to remove or normalize
        self.stop_words = {
            'the', 'and', 'or', 'with', 'for', 'new', 'original', 'genuine',
            'official', 'authentic', 'brand', 'product', 'item', 'piece'
        }
        
        # Brand variations mapping
        self.brand_variations = {
            'apple': ['apple', 'iphone', 'ipad', 'macbook', 'imac'],
            'samsung': ['samsung', 'galaxy'],
            'sony': ['sony', 'playstation', 'ps4', 'ps5'],
            'nintendo': ['nintendo', 'switch'],
            'microsoft': ['microsoft', 'xbox', 'surface'],
            'hp': ['hp', 'hewlett packard', 'hewlett-packard'],
            'dell': ['dell'],
            'lenovo': ['lenovo', 'thinkpad'],
            'asus': ['asus'],
            'acer': ['acer'],
        }
        
        # Common abbreviations and expansions
        self.abbreviations = {
            'gb': 'gigabyte',
            'tb': 'terabyte',
            'mb': 'megabyte',
            'ram': 'memory',
            'ssd': 'solid state drive',
            'hdd': 'hard disk drive',
            'cpu': 'processor',
            'gpu': 'graphics card',
            'lcd': 'liquid crystal display',
            'led': 'light emitting diode',
            'oled': 'organic led',
            'uhd': 'ultra high definition',
            '4k': 'ultra high definition',
            'fhd': 'full high definition',
            'hd': 'high definition'
        }
    
    def normalize_name(self, name: str) -> str:
        """Normalize product name for matching"""
        if not name:
            return ""
        
        # Convert to lowercase
        normalized = name.lower().strip()
        
        # Remove special characters and extra spaces
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Expand abbreviations
        words = normalized.split()
        expanded_words = []
        for word in words:
            if word in self.abbreviations:
                expanded_words.append(self.abbreviations[word])
            else:
                expanded_words.append(word)
        
        normalized = ' '.join(expanded_words)
        
        # Remove stop words
        words = [word for word in normalized.split() if word not in self.stop_words]
        normalized = ' '.join(words)
        
        return normalized.strip()
    
    def extract_brand(self, name: str) -> Optional[str]:
        """Extract brand from product name"""
        normalized_name = name.lower()
        
        for brand, variations in self.brand_variations.items():
            for variation in variations:
                if variation in normalized_name:
                    return brand
        
        return None
    
    def extract_specifications(self, name: str) -> Dict[str, str]:
        """Extract technical specifications from product name"""
        specs = {}
        
        # Storage capacity (GB, TB)
        storage_match = re.search(r'(\\d+)\\s*(gb|tb)', name.lower())
        if storage_match:
            amount, unit = storage_match.groups()
            specs['storage'] = f"{amount}{unit}"
        
        # RAM
        ram_match = re.search(r'(\\d+)\\s*(gb|mb)\\s*(ram|memory)', name.lower())
        if ram_match:
            amount, unit, _ = ram_match.groups()
            specs['ram'] = f"{amount}{unit}"
        
        # Screen size
        screen_match = re.search(r'(\\d+(?:\\.\\d+)?)\\s*(?:inch|"|′)', name.lower())
        if screen_match:
            specs['screen_size'] = screen_match.group(1)
        
        # Model numbers
        model_match = re.search(r'[a-zA-Z]{1,3}\\d{2,6}[a-zA-Z]*', name)
        if model_match:
            specs['model'] = model_match.group()
        
        return specs

class ProductMatcher:
    """Main product matching engine"""
    
    def __init__(self, config: Optional[MatchConfig] = None):
        self.config = config or MatchConfig()
        self.normalizer = ProductNormalizer()
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=5000,
            stop_words='english'
        )
    
    def match_and_deduplicate(self, products: List[Dict]) -> List[Dict]:
        """Main method to match and deduplicate products"""
        if not products:
            return []
        
        logger.info(f"Starting product matching for {len(products)} products")
        
        # Normalize product names
        normalized_products = self._normalize_products(products)
        
        # Group by category/brand if possible
        grouped_products = self._group_products_by_category(normalized_products)
        
        # Find matches within each group
        all_matched_groups = []
        for group in grouped_products:
            matched_groups = self._find_matches_in_group(group)
            all_matched_groups.extend(matched_groups)
        
        # Merge matches and select best representatives
        final_products = self._merge_matches(all_matched_groups)
        
        logger.info(f"Product matching completed. {len(final_products)} unique products found")
        return final_products
    
    def _normalize_products(self, products: List[Dict]) -> List[Dict]:
        """Normalize all product names and extract metadata"""
        normalized = []
        
        for product in products:
            normalized_product = product.copy()
            
            # Normalize name
            original_name = product.get('name', '')
            normalized_name = self.normalizer.normalize_name(original_name)
            
            normalized_product.update({
                'original_name': original_name,
                'normalized_name': normalized_name,
                'brand': self.normalizer.extract_brand(original_name),
                'specifications': self.normalizer.extract_specifications(original_name),
                'name_length': len(normalized_name.split()),
                'price_per_char': product.get('price', 0) / max(len(normalized_name), 1)
            })
            
            normalized.append(normalized_product)
        
        return normalized
    
    def _group_products_by_category(self, products: List[Dict]) -> List[List[Dict]]:
        """Group products by brand/category for more efficient matching"""
        brand_groups = defaultdict(list)
        no_brand_group = []
        
        for product in products:
            brand = product.get('brand')
            if brand and self.config.use_brand_matching:
                brand_groups[brand].append(product)
            else:
                no_brand_group.append(product)
        
        groups = list(brand_groups.values())
        if no_brand_group:
            groups.append(no_brand_group)
        
        return groups
    
    def _find_matches_in_group(self, products: List[Dict]) -> List[List[Dict]]:
        """Find matching products within a group using multiple algorithms"""
        if len(products) <= 1:
            return [products] if products else []
        
        # Calculate similarity matrix
        similarity_matrix = self._calculate_similarity_matrix(products)
        
        # Find clusters of similar products
        clusters = self._cluster_similar_products(products, similarity_matrix)
        
        return clusters
    
    def _calculate_similarity_matrix(self, products: List[Dict]) -> np.ndarray:
        """Calculate similarity between all product pairs"""
        n = len(products)
        similarity_matrix = np.zeros((n, n))
        
        names = [p['normalized_name'] for p in products]
        
        # Use multiple similarity metrics
        for i in range(n):
            for j in range(i + 1, n):
                # Fuzzy string similarity
                fuzzy_score = fuzz.token_sort_ratio(names[i], names[j]) / 100.0
                
                # Price similarity (if enabled)
                price_score = 1.0
                if self.config.use_price_filtering:
                    price_score = self._calculate_price_similarity(products[i], products[j])
                
                # Specification similarity
                spec_score = self._calculate_spec_similarity(products[i], products[j])
                
                # Combined score
                combined_score = (fuzzy_score * 0.6 + price_score * 0.2 + spec_score * 0.2)
                
                similarity_matrix[i][j] = combined_score
                similarity_matrix[j][i] = combined_score
        
        # Self-similarity is 1.0
        np.fill_diagonal(similarity_matrix, 1.0)
        
        return similarity_matrix
    
    def _calculate_price_similarity(self, product1: Dict, product2: Dict) -> float:
        """Calculate price similarity between two products"""
        price1 = product1.get('price', 0)
        price2 = product2.get('price', 0)
        
        if price1 == 0 or price2 == 0:
            return 0.5  # Neutral score if price missing
        
        # Calculate percentage difference
        avg_price = (price1 + price2) / 2
        price_diff_percent = abs(price1 - price2) / avg_price * 100
        
        if price_diff_percent <= self.config.max_price_difference_percent:
            return 1.0 - (price_diff_percent / self.config.max_price_difference_percent)
        else:
            return 0.0
    
    def _calculate_spec_similarity(self, product1: Dict, product2: Dict) -> float:
        """Calculate specification similarity between two products"""
        specs1 = product1.get('specifications', {})
        specs2 = product2.get('specifications', {})
        
        if not specs1 and not specs2:
            return 1.0  # Both have no specs
        
        if not specs1 or not specs2:
            return 0.5  # One has specs, other doesn't
        
        # Compare common specifications
        common_keys = set(specs1.keys()) & set(specs2.keys())
        if not common_keys:
            return 0.5
        
        matches = sum(1 for key in common_keys if specs1[key] == specs2[key])
        return matches / len(common_keys)
    
    def _cluster_similar_products(self, products: List[Dict], similarity_matrix: np.ndarray) -> List[List[Dict]]:
        """Cluster products based on similarity matrix"""
        n = len(products)
        visited = set()
        clusters = []
        
        for i in range(n):
            if i in visited:
                continue
            
            # Start new cluster
            cluster = [products[i]]
            visited.add(i)
            
            # Find all similar products
            for j in range(i + 1, n):
                if j not in visited and similarity_matrix[i][j] >= self.config.min_similarity_score:
                    cluster.append(products[j])
                    visited.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def _merge_matches(self, matched_groups: List[List[Dict]]) -> List[Dict]:
        """Merge matched groups and select best representative for each"""
        final_products = []
        
        for group in matched_groups:
            if len(group) == 1:
                final_products.append(group[0])
            else:
                # Select best representative from group
                representative = self._select_best_representative(group)
                
                # Add information about alternatives
                alternatives = [p for p in group if p != representative]
                representative['alternatives'] = alternatives
                representative['price_range'] = {
                    'min': min(p['price'] for p in group),
                    'max': max(p['price'] for p in group),
                    'avg': sum(p['price'] for p in group) / len(group)
                }
                
                final_products.append(representative)
        
        # Sort by price
        final_products.sort(key=lambda x: x['price'])
        
        return final_products
    
    def _select_best_representative(self, group: List[Dict]) -> Dict:
        """Select the best representative product from a matched group"""
        # Score each product based on multiple criteria
        scored_products = []
        
        for product in group:
            score = 0
            
            # Prefer products with more complete information
            if product.get('brand'):
                score += 10
            if product.get('specifications'):
                score += len(product['specifications']) * 2
            
            # Prefer products with reasonable name length (not too short/long)
            name_length = product.get('name_length', 0)
            if 3 <= name_length <= 15:
                score += 5
            
            # Prefer products from known vendors (could be made configurable)
            vendor_scores = {
                'Amazon': 15, 'eBay': 10, 'Walmart': 12, 'Best Buy': 10,
                'Flipkart': 12, 'Target': 8
            }
            vendor = product.get('vendor', '')
            score += vendor_scores.get(vendor, 0)
            
            # Prefer lower prices (slight preference)
            min_price = min(p['price'] for p in group)
            if product['price'] == min_price:
                score += 5
            
            scored_products.append((score, product))
        
        # Return product with highest score
        scored_products.sort(key=lambda x: x[0], reverse=True)
        return scored_products[0][1]
    
    def calculate_match_confidence(self, product1: Dict, product2: Dict) -> float:
        """Calculate confidence score for two products being the same"""
        name_sim = fuzz.token_sort_ratio(
            product1.get('normalized_name', ''),
            product2.get('normalized_name', '')
        ) / 100.0
        
        price_sim = self._calculate_price_similarity(product1, product2)
        spec_sim = self._calculate_spec_similarity(product1, product2)
        
        return (name_sim * 0.6 + price_sim * 0.2 + spec_sim * 0.2)
'''

with open('product_matcher.py', 'w') as f:
    f.write(product_matcher_code)

print("✅ product_matcher.py created")
print("🔍 Product matching features:")
print("  - Fuzzy string matching with multiple algorithms")
print("  - Brand and specification extraction")
print("  - Price similarity filtering")
print("  - Product name normalization")
print("  - Clustering and deduplication")
print("  - Best representative selection")
print("  - Confidence scoring")