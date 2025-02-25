from typing import List, Dict, Any, Optional
from models.product_catalog import PRODUCT_PRICES, PRODUCTS_BY_CATEGORY, CATEGORIES

class ProductService:
    def __init__(self):
        # For now, use the hardcoded product data. Later this will come from a database.
        self.product_prices = PRODUCT_PRICES
        self.products_by_category = PRODUCTS_BY_CATEGORY
        self.categories = CATEGORIES
        
    def get_product_price(self, product_name: str) -> float:
        """Get price for a specific product"""
        return self.product_prices.get(product_name, 0.0)
        
    def get_products_for_category(self, category_name: str) -> List[str]:
        """Get all products for a specific category"""
        return self.products_by_category.get(category_name, [])
        
    def get_all_categories(self) -> List[str]:
        """Get list of all product categories"""
        return self.categories
        
    def filter_products(self, search_text: str) -> List[str]:
        """Filter products based on search text"""
        if not search_text:
            return []
            
        search_text = search_text.lower()
        filtered_products = []
        
        # Search across all categories
        for category in self.categories:
            for product in self.products_by_category.get(category, []):
                if search_text in product.lower():
                    filtered_products.append(product)
                    
        return filtered_products
        
    def get_product_details(self, product_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a product"""
        if product_name not in self.product_prices:
            return None
            
        # Find which category this product belongs to
        category = None
        for cat, products in self.products_by_category.items():
            if product_name in products:
                category = cat
                break
                
        return {
            'name': product_name,
            'price': self.product_prices.get(product_name, 0.0),
            'category': category
        }