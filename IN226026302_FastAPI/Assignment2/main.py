from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# Question 1 - added 3 more products with product_id 5,6,7
products = [
    {'id': 1, 'name': 'Wireless Mouse','price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 199999, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5 ,'name': 'Laptop Table', 'price':1299,'category':'Electronics','in_stock':False},
    {'id': 6 , 'name': 'Mechanical Keyboard', 'price':2499,'category':'Electronics','in_stock':True},
    {"id": 7, "name": "Cello Office Stationery Kit", "price": 92, "category": "Stationery", "in_stock": True}
]

feedback_db = []
orders_db = []

@app.get("/")
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get("/products")
def get_all_products():
    return {'product': products, 'total': len(products)}

@app.get('products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

@app.get('/products/filters')
def filter_products(
    category: str = Query(None, description='Electronics or Stationery'),
    max_price: int = Query(None, description='Maximum Price'),
    in_stock: bool = Query(None, description='True = in stock only')
):
    result = products

    if category:
        result = [p for p in result if p['category']== category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {'filtered+products': result, 'count': len(result)}

# Assignment 2 Code

# Question 1 - created /products/filter endpoint
@app.get('/products/filter')
def filterBetweenPrice(
    min_price: int = Query(None, description="Minimum Price"),
    max_price: int = Query(None, description="Maximum Price")
):
    result = [p for p in products if p['price']>=min_price]
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
    return {'result': result, 'min_price': min_price, 'max_price': max_price, 'count': len(result)}

# Question 2 - created /products/{product_id}/price endpoint
@app.get('/products/{product_id}/price')
def getNamePrice(product_id: int):
    if product_id > len(products):
        return {'error': 'Product not found!'}
    product = next((p for p in products if p['id']==product_id), None)
    return {'name':product['name'], 'price': product['price']}

# Question 3 - created POST /feedback endpoint

class CustomerFeedback(BaseModel):
    customer_name: str = Field('Anonymous', min_length=2)
    product_id: int = Field(..., gt=0)
    ratings: int = Field(..., gt=0, le=5)
    comment: Optional[str] = Field(None, max_length=300)

@app.post('/feedback')
async def create_Feedback(feedback: CustomerFeedback):
    new_entry = feedback.model_dump()
    feedback_db.append(new_entry)

    return {
        'message': 'Form submitted successfully',
        'feedback': new_entry,
        'total_feedback': len(feedback_db)
    }

# Question 4 - create /products/summary
@app.get('/products/summary')
def products_summary():
    total_products = len(products)
    in_stock = len([p for p in products if p['in_stock']==True])
    out_stock = total_products-in_stock
    category = set([p['category'] for p in products])
    most_exp = max(products, key=lambda p: p['price'])
    most_exp = {'name':most_exp['name'], 'price':most_exp['price']}
    cheap = min(products, key=lambda p: p['price'])
    cheap = {'name':cheap['name'], 'price':cheap['price']}

    return {
        'total_products': total_products,
        'in_stock': in_stock,
        'out_stock': out_stock,
        'most_expensive': most_exp,
        'cheapest': cheap,
        'categories': category
    }

# Question 5.1 - create POST /orders/bulk endpoint
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0, examples=[1])
    qty: int = Field(..., gt=0, le=51, examples=[1])

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

@app.post('/orders/bulk')
def bulk_Order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.qty
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.qty, "subtotal": subtotal})

    new_order = {
        "order_id": len(orders_db) + 1,
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total,
        "status": "pending" 
    }
    orders_db.append(new_order)
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}


# BONUS endpoint
@app.get('/orders/{order_id}')
def get_order(order_id: int):
    order = next((o for o in orders_db if o["order_id"] == order_id), None)
    if not order:
        return {"error": "Order not found"}
    return order

@app.patch('/orders/{order_id}/confirm')
def confirm_order(order_id: int):
    order = next((o for o in orders_db if o["order_id"] == order_id), None)
    if not order:
        return {"error": "Order not found"}
    
    order["status"] = "confirmed"
    return {"message": f"Order {order_id} has been confirmed", "status": order["status"]}

# Assignment 1 code

# Question 2 - created 'products/category/{category_name}' endpoint
@app.get('/products/category/{category_name}')
def filter_by_category(category_name: str):
    results = [p for p in products if p['category']== category_name]
    
    if results: return {f'filter_By_{category_name}': results, 'count': len(results)}
    else: return {"error": "No products found in this category"}

# Question 3 - created 'products/instock' endpoint
@app.get('/products/instock')
def get_instock():
    results = [p for p in products if p['in_stock']==True]
    return {'in_stock_products': results, 'count': len(results)}

# Question 4 - created '/store/summary' endpoint
@app.get('/store/summary')
def store_summary():
    total_products = len(products)
    in_stock = len([p for p in products if p['in_stock']==True])
    out_stock = total_products-in_stock
    category = set([p['category'] for p in products])

    return {
        'store_name': "My E-commerce Store",
        'total_products': total_products,
        'in_stock': in_stock,
        'out_stock': out_stock,
        'categories': category
    }

# Question 5 - created '/products/search/{keyword}' endpoint
@app.get('/products/search/{keyword}')
def search_product(keyword: str):
    result = [p for p in products if keyword.lower() in p['name'].lower()]
    if result:
        return {
            'keyword': keyword,
            'results': result,
            'total_matches': len(result)
        }
    else: return{'message': 'No products matched'}

# Bonus Question - created '/products/deals' endpoints
@app.get('/products/deals')
def get_deals():
    cheapest = min(products, key=lambda p: p['price'])
    expensive = max(products, key=lambda p: p['price'])
    return {
        'best_deals': cheapest,
        'premium_pick': expensive
    }

