from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, condecimal
from typing import Optional, List
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Enable CORS (for local frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:5500"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 for HTML templating
templates = Jinja2Templates(directory="templates")

# Home route (HTML page)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Pydantic model for Product
class Product(BaseModel):
    product_id: int
    cost: condecimal(max_digits=10, decimal_places=2)
    category: Optional[str] = Field(default=None, max_length=255)
    product_name: Optional[str] = Field(default=None, max_length=255)
    brand: Optional[str] = Field(default=None, max_length=255)
    retail_price: condecimal(max_digits=10, decimal_places=2)
    department: Optional[str] = Field(default=None, max_length=255)
    sku: Optional[str] = Field(default=None, max_length=255)
    distribution_center_id: Optional[int]

# MySQL connection helper
def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='bADBOY$1',  # replace if needed
        database='ecommerce'
    )

# GET all products with optional pagination
@app.get("/api/products", response_model=List[Product])
def get_products(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products LIMIT %s OFFSET %s", (limit, skip))
        products = cursor.fetchall()
        return products
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# GET product by ID
@app.get("/api/products/{id}", response_model=Product)
def get_product(id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
