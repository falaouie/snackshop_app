"""
Product catalog module containing category and product definitions.
This module serves as a temporary storage for product data before database implementation.
"""

# Categories available in the POS system
CATEGORIES = ["Main", "Sandwiches", "Snacks", "Beverages", "Desserts"]

# Products organized by category
PRODUCTS_BY_CATEGORY = {
    "Main": [
        "Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", 
        "Steak N Cheese", "Vegan Sandwich", "BLT 2", "Tuna", 
        "Veggie 3", "Egg Sandwich 2", "Steak N Cheese 2",
        "Vegan Sandwich", "BLT 3", "Tuna", 
        "Another Vegan Sandwich", "Another BLT", "Another Tuna"
    ],
    "Sandwiches": [
        "Chicken Club6", "BLT5", "Tuna8", "Veggie5", 
        "Egg Sandwich4", "Steak N Cheese", "Vegan Sandwich"
    ],
    "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
    "Beverages": ["Coffee", "Tea", "Soda", "Soda Diet", "Lemonade", "Water"],
    "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
}

# Product prices
PRODUCT_PRICES = {
    "Chicken Club": 8.50,
    "BLT": 6.50,
    "Tuna": 7.00,
    "Veggie": 6.00,
    "Egg Sandwich": 5.50,
    "Steak N Cheese": 9.50,
    "Vegan Sandwich": 7.50,
    "Chips": 2.00,
    "Popcorn": 2.50,
    "Nuts": 3.00,
    "Pretzels": 2.50,
    "Coffee": 3.50,
    "Tea": 2.50,
    "Soda": 2.00,
    "Soda Diet": 2.00,
    "Lemonade": 3.00,
    "Water": 1.50,
    "Cookies": 2.50,
    "Brownies": 3.50,
    "Muffins": 3.00,
    "Fruit Cup": 4.00
}

def get_products_for_category(category_name):
    """
    Get all products for a specific category.
    
    Args:
        category_name (str): Name of the category
        
    Returns:
        list: List of product names in the category
    """
    return PRODUCTS_BY_CATEGORY.get(category_name, [])

def get_product_price(product_name):
    """
    Get the price for a specific product.
    
    Args:
        product_name (str): Name of the product
        
    Returns:
        float: Price of the product, or 0.0 if not found
    """
    return PRODUCT_PRICES.get(product_name, 0.0)