import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:2210@localhost:3306/restaurant_db"
)


# read tables
customers = pd.read_sql("select * from customers", engine)
menu = pd.read_sql("select * from menu", engine)
sales = pd.read_sql("select * from sales", engine)


# dispaly first five rows
print("\nCustomers")
print(customers.head())
print("\nMenu")
print(menu.head())
print("\nSales")
print(sales.head())


# check shape of the table (number of rows and columns in each table)
print("\nCustomers Shape:",customers.shape)
print("Menu Shape:",menu.shape)
print("Sales Shape:",sales.shape)


# check column names
print("\nCustomers Columns")
print(customers.columns)
print("\nMenu Columns")
print(menu.columns)
print("\nSales Columns")
print(sales.columns)


# check data types
print("\nCustomers Info")
customers.info()
print("\nMenu Info")
menu.info()
print("\nSales Info")
sales.info()