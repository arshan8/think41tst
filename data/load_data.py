import pandas as pd
import mysql.connector

csv_file_path = r"C:\Users\ARSHAN\Desktop\temp\think\think41tst\data\products.csv"

df = pd.read_csv(csv_file_path)
print("CSV data preview:")
print(df.head())

cnx = mysql.connector.connect(
    host='127.0.0.1', 
    port=3306,
    user='root',       
    password='#',
    database='ecommerce'
)
cursor = cnx.cursor()

# Drop existing table to ensure the new schema is applied
cursor.execute("DROP TABLE IF EXISTS products")
cnx.commit()

# Create the products table with the correct schema
create_table_query = """
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    cost DECIMAL(10,2),
    category VARCHAR(255),
    product_name VARCHAR(255),
    brand VARCHAR(255),
    retail_price DECIMAL(10,2),
    department VARCHAR(255),
    sku VARCHAR(255),
    distribution_center_id INT
)
"""
cursor.execute(create_table_query)
cnx.commit()

# Insert CSV data into the MySQL database, updating duplicates if necessary
insert_query = """
INSERT INTO products 
(product_id, cost, category, product_name, brand, retail_price, department, sku, distribution_center_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    cost = VALUES(cost),
    category = VALUES(category),
    product_name = VALUES(product_name),
    brand = VALUES(brand),
    retail_price = VALUES(retail_price),
    department = VALUES(department),
    sku = VALUES(sku),
    distribution_center_id = VALUES(distribution_center_id)
"""

for _, row in df.iterrows():
    data = (
        int(row['id']),
        float(row['cost']),
        row['category'],
        row['name'],
        row['brand'],
        float(row['retail_price']),
        row['department'],
        row['sku'],
        int(row['distribution_center_id'])
    )
    cursor.execute(insert_query, data)
cnx.commit()

# Verify that the data was loaded by querying the MySQL table
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]
print("Total products loaded:", count)

cursor.execute("SELECT * FROM products LIMIT 5")
print("Sample products:")
for sample in cursor.fetchall():
    print(sample)

cursor.close()
cnx.close()
