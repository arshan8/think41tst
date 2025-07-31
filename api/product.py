from pydantic import BaseModel, Field, condecimal
from typing import Optional

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
