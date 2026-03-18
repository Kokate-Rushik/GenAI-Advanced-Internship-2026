from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from contextlib import asynccontextmanager
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_all_db()

    yield
    save_all_db()

# Initialise App
app = FastAPI(lifespan=lifespan, title="FastAPI Task 5")

# All DB
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

cart = []
orders = []

def save_all_db():
    if orders:
        try:
            with open("orders.json", "w") as f:
                json.dump(orders, f, indent=4)
            print("Successfully saved orders to disk.")
        except IOError as e:
            print(f"Error: Could not save data. {e}")
    else:
        print("Orders is empty")

def load_all_db():
    try:
        with open("orders.json", "r") as f:
            data = json.load(f)
            orders.clear()
            orders.extend(data)
    except FileNotFoundError:
        pass


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



# Assignment Task 5

# Question 1 - create /product/search endpoint
@app.get("/products/search")
def search_product(keyword: str):
    result = [p['name'] for p in products if keyword.lower() in p['name'].lower()]
    if not result:
        return {
            "message": f"No products found for: {keyword}"
        }
    return {
        'keyword': keyword,
        'search_result': len(result),
        'result': result
    }

# Question 2 - create /product/sort endpoint
class SortbyFields(str, Enum):
    name= 'name'
    price= 'price'
    category= 'category'

class OrderOption(str, Enum):
    ase= 'ase'
    desc= 'desc'

@app.get("/products/sort")
def sort_product_by(
    sort_by: SortbyFields = SortbyFields.price,
    order: OrderOption = OrderOption.ase
):
    reserve_order = order==OrderOption.desc
    try:
        result = sorted(products, key= lambda p:p[sort_by.value], reverse=reserve_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return{
        'result': result
    }

# Question 3 - create /product/page endpoint
@app.get("/products/page")
def get_page(page: int=1, limit:int=2):
    total_pages = int(len(products)/limit+0.5)
    start = (page-1)*limit
    result = list(products)[start:start+limit]
    return {
        'products': result,
        'total_pages': total_pages
    }

# Question 4 - create '/order/search' endpoint
@app.get("/order/search")
def search_order_by_name(customer_name: str):
    result = [order for order in orders if order['customer_name'].lower()==customer_name.lower()]
    total_spend = sum(order['total_price'] for order in result)
    if not result:
        return {
            'message': f'No orders with Customer name {customer_name} found'
        }
    return {
        'customer_name': customer_name,
        'total_found': len(result),
        'total_spend': total_spend,
        'order': result
    }

# Question 5 - create /products/sort-by-category
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key=lambda p: (p['category'], p['price']))
    return {
        'products': result,
        'total_count': len(result)
    }

# Question 6 - create /products/browse endpoint
@app.get("/products/browse")
def browse_product(
    keyword: str=None,
    sort_by: SortbyFields=SortbyFields.price,
    order: OrderOption=OrderOption.ase,
    page: int=1,
    limit: int=4
):
    if keyword:
        result = [p for p in products if keyword.lower() in p['name'].lower()]
    else: result = list(products)
    is_reverse = order==OrderOption.desc
    result = sorted(result, key=lambda p: p[sort_by], reverse=is_reverse)
    total_pages = int(len(result)/limit+0.5)
    start = (page-1)*limit
    result = result[start:start+limit]
    return {
        'keyword': keyword,
        'sort_by': sort_by,
        'order': order,
        'page': page,
        'limit': limit,
        'total_page': total_pages,
        'products': result
    }

# Bonus Question - create /orders/page endpoint
@app.get("/orders/page")
def page_orders_db(page: int=1, limit:int=3):
    total_pages = int(len(orders)/limit+0.5)
    start = (page-1)*limit
    result = list(orders)[start:start+limit]
    return {
        'orders': result,
        'total_pages': total_pages
    }

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

