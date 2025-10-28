"""Inventory management system with proper error handling and security."""
import json
import logging
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory.
    
    Args:
        item (str): Item name to add
        qty (int): Quantity to add
        logs (list): Optional list to append log entries
        
    Returns:
        None
    """
    if logs is None:
        logs = []
    
    if not item:
        return
    
    # Type validation
    if not isinstance(item, str):
        logging.error(f"Invalid item type: {type(item)}. Expected string.")
        return
    
    if not isinstance(qty, int):
        logging.error(f"Invalid quantity type: {type(qty)}. Expected integer.")
        return
    
    stock_data[item] = stock_data.get(item, 0) + qty
    log_entry = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_entry)
    logging.info(log_entry)


def remove_item(item, qty):
    """
    Remove an item from the inventory.
    
    Args:
        item (str): Item name to remove
        qty (int): Quantity to remove
        
    Returns:
        None
    """
    try:
        if item not in stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")
        
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info(f"Removed all '{item}' from inventory")
    except KeyError as e:
        logging.error(str(e))


def get_qty(item):
    """
    Get the quantity of an item in inventory.
    
    Args:
        item (str): Item name to query
        
    Returns:
        int: Quantity of item in stock, 0 if not found
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.
    
    Args:
        file (str): Path to JSON file to load
        
    Returns:
        None
    """
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info(f"Successfully loaded data from {file}")
    except FileNotFoundError:
        logging.warning(f"File {file} not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {file}: {e}")


def save_data(file="inventory.json"):
    """
    Save inventory data to a JSON file.
    
    Args:
        file (str): Path to JSON file to save
        
    Returns:
        None
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        logging.info(f"Successfully saved data to {file}")
    except IOError as e:
        logging.error(f"Error saving to {file}: {e}")


def print_data():
    """
    Print current inventory in a formatted report.
    
    Returns:
        None
    """
    print("\n" + "=" * 50)
    print("INVENTORY REPORT")
    print("=" * 50)
    if not stock_data:
        print("No items in inventory")
    else:
        for item, quantity in stock_data.items():
            print(f"{item:20} -> {quantity:5}")
    print("=" * 50 + "\n")


def check_low_items(threshold=5):
    """
    Check for items below a quantity threshold.
    
    Args:
        threshold (int): Minimum quantity threshold (default: 5)
        
    Returns:
        list: List of items below threshold
    """
    result = []
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """
    Main execution function to demonstrate inventory operations.
    
    Returns:
        None
    """
    logging.info("Starting inventory system")
    
    # Valid operations
    add_item("apple", 10)
    add_item("banana", 5)
    
    # Invalid operations - will log errors
    add_item(123, "ten")  # Invalid types - will be caught by validation
    
    # Remove operations
    remove_item("apple", 3)
    remove_item("orange", 1)  # Will log error - item doesn't exist
    
    # Query operations
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    
    # File operations
    save_data()
    load_data()
    print_data()
    
    # Removed dangerous eval() - replaced with safe alternative
    print("System running safely without eval()")
    
    logging.info("Inventory system operations completed successfully")


if __name__ == "__main__":
    main()