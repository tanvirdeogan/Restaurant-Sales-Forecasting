import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:2210@localhost:3306/restaurant_db"
)

# read tables
customers = pd.read_sql("select * from customers", engine)
menu = pd.read_sql("select * from menu", engine)
sales = pd.read_sql("select * from sales", engine)


# check for missing values
print("Customers Missing Values")
print(customers.isnull().sum())
print("\nMenu Missing Values")
print(menu.isnull().sum())
print("\nSales Missing Values")
print(sales.isnull().sum())


# check duplicate records
print("\nCustomer Duplicates:", customers.duplicated().sum())
print("Menu Duplicates:", menu.duplicated().sum())
print("Sales Duplicates:", sales.duplicated().sum())


# summary statistics
print("\nSales Summary")
print(sales.describe())


# revenue summary
print("\nTotal Revenue:", sales["total_bill"].sum())
print("Average Bill:", sales["total_bill"].mean())
print("Maximum Bill:", sales["total_bill"].max())
print("Minimum Bill:", sales["total_bill"].min())


# orders by payment method
sales["payment_method"].value_counts().plot(kind="bar")

plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")

plt.show()


# orders by city
customers["city"].value_counts().plot(kind="bar")

plt.title("Customers by City")
plt.xlabel("City")
plt.ylabel("Customers")

plt.show()


# membership distribution
customers["membership"].value_counts().plot(kind="pie", autopct="%1.1f%%")

plt.title("Membership Distribution")

plt.ylabel("")

plt.show()


# order quantity distribution
sales["quantity"].plot(kind="hist", bins=10)

plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Frequency")

plt.show()
