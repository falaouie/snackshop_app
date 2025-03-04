# services/data_service.py
# from typing import Dict, List
# from models.product_catalog import Product, ProductOption, Ingredient  # We'll create these models next

# class DataService:
#     def __init__(self):
#         self._cache = {}  # Simple cache for demonstration
        
#     def get_categories(self) -> List[str]:
#         """Get all product categories (replace with DB call later)"""
#         return ["Sandwiches", "Drinks", "Snacks"]  # Temporary hardcoded
        
#     def get_products_by_category(self, category: str) -> List[Product]:
#         """Get products for a category (will later query DB)"""
#         return self._cache.get(category, [])
        
#     def get_product_options(self, product_id: str) -> List[ProductOption]:
#         """Get customization options for a product"""
#         return []