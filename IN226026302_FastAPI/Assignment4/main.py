from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Initialise App
app = FastAPI(title="Cart System API", version="1.0")

# All DB
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

cart = []
orders = []

# Useful functions
def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

def calculate_total(product, quantity):
    return product["price"] * quantity

@app.get("/")
def home():
    return {"message": "Cart System API Running"}

# Assignment Task 4

# Question 1 - create cart/add endpoint
# Question 3 - handling product_id out_of_stock and not found
# Question 4 - updating the cart
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int=1):
    product = find_product(product_id)

    # Question 3 part
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    if not product["in_stock"]:
        raise HTTPException(status_code=404, detail="Product out of stocks!")
    
    # Question 4 part
    for item in cart:
        if item["product_id"]==product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])

            return {
                "message": "Cart updated",
                "cart": cart
            }

    # Question 1 part

    subtotal = calculate_total(product, quantity)
    item_data = {
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": subtotal
    }
    cart.append(item_data)

    return {
        "message": "Added to cart",
        "cart_item": item_data
    }

# Question 2 - create GET /cart endpoint
@app.get("/cart")
def get_Cart():
    if not cart:
        return {
            "message": "Cart is empty"
        }
    item_count = len(cart)
    grand_total = sum([item["subtotal"] for item in cart])
    return {
        "items": cart,
        "item_count": item_count,
        "grand_total": grand_total
    }

# Question 5 part 1 - create DELETE /cart/{product_id} endpoint
@app.delete("/cart/{product_id}")
def delete_from_cart(product_id: int):
    for index, item in enumerate(cart):
        if item['product_id'] == product_id:
            removed_product = cart.pop(index)
            return {
                "message": f"Successfully removed {removed_product["product_name"]}"
            }
    raise HTTPException(status_code=404, detail="Product not found in the cart!")

# Question 5 part 2 - create POST /cart/checkout endpoint
@app.post("/cart/checkout")
def cart_checkout(customer_name: str, customer_address: str):
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty!")
    grand_total = sum([item["subtotal"] for item in cart])
    new_order = {
        "order_id": len(orders)+1,
        "customer_name": customer_name,
        "customer_address" : customer_address,
        "order": list(cart),
        "total_price": grand_total
    }
    orders.append(new_order)
    cart.clear()
    return {
        "message": "Checkout successful",
        "customer_name": customer_name,
        "total_price": grand_total
    }

# Question 5 part 3 - create GET /orders endpoint
@app.get("/orders")
def get_all_orders():
    if not orders:
        return{
            "message": "No new orders added!"
        }
    return {
        "orders": orders,
        "order_count": len(orders)
    }