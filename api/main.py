from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, condecimal
from typing import Optional, List
import mysql.connector
from mysql.connector import Error

app = FastAPI()


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


def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='bADBOY$1',  #
        database='ecommerce'           #
    )


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
