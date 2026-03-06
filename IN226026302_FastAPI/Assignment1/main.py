from fastapi import FastAPI, Query

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

@app.get('/products/filter')
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