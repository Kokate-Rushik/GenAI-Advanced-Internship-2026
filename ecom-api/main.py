from fastapi import FastAPI, HTTPException, Request, Query

app = FastAPI()

products = [
  {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": true},
  {"id": 2, "name": "Borosil Chef Delite Chopper", "price": 1949, "category": "Kitchen Appliances", "in_stock": true},
  {"id": 3, "name": "Kangaro DP-480 Paper Punch", "price": 135, "category": "Office Supplies", "in_stock": true},
  {"id": 4, "name": "Philips 4.1L Air Fryer HD9200/90", "price": 5587, "category": "Kitchen Appliances", "in_stock": true},
  {"id": 5, "name": "Umi Rotating Desk Organizer", "price": 499, "category": "Office Supplies", "in_stock": true},
  {"id": 6, "name": "DuRoBo Krono E-reader", "price": 23500, "category": "Electronics", "in_stock": true},
  {"id": 7, "name": "Cello Office Stationery Kit", "price": 492, "category": "Office Supplies", "in_stock": true},
  {"id": 8, "name": "Humble Kart 4-Compartment Organizer", "price": 928, "category": "Office Supplies", "in_stock": false},
  {"id": 9, "name": "Xreal 1S AR Glasses", "price": 37700, "category": "Electronics", "in_stock": true},
  {"id": 10, "name": "Prestige PIC 20 NEO Induction Cooktop", "price": 2960, "category": "Kitchen Appliances", "in_stock": true}
]


@app.get("/")
def home():
    return {"message": "Welcome to home page"}

@app.get("/about")
def about():
    return {"name": "Rushik", "Organization": "Innomatics Research Labs", "Role": "Agentic AI Intern"}

@app.get("/{full_path:path}")
def not_found_handler(request: Request, full_path: str):
    return HTTPException(status_code=404, detail=f"Oops! The page at '{full_path}' does not exists.")

@app.get("/product")
def get_all_products():
    return {'product': products, 'total': len(products)}

@app.get('product/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

@app.get('/products/filter')

def filter_products(

    category:  str  = Query(None, description='Electronics or Stationery'),

    max_price: int  = Query(None, description='Maximum price'),

    in_stock:  bool = Query(None, description='True = in stock only')

):

    result = products          # start with all products

 

    if category:

        result = [p for p in result if p['category'] == category]

 

    if max_price:

        result = [p for p in result if p['price'] <= max_price]

 

    if in_stock is not None:

        result = [p for p in result if p['in_stock'] == in_stock]

 

    return {'filtered_products': result, 'count': len(result)}




