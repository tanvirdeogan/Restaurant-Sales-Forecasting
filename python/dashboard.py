import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:2210@localhost:3306/restaurant_db"
)

customers = pd.read_sql("SELECT * FROM customers", engine)
menu = pd.read_sql("SELECT * FROM menu", engine)
sales = pd.read_sql("SELECT * FROM sales", engine)

# TOP 10 BEST SELLING DISHES
dish_sales = (
    sales.merge(menu, on="dish_id")
         .groupby("dish_name")["quantity"]
         .sum()
         .sort_values(ascending=False)
         .head(10)
)

plt.figure(figsize=(10,6))

dish_sales.plot(kind="bar")

plt.title("Top 10 Best Selling Dishes")
plt.xlabel("Dish")
plt.ylabel("Quantity Sold")

plt.tight_layout()

plt.savefig("images/top_10_best_selling_dishes.png")

plt.show()


# REVENUE BY CATEGORY
category_revenue = (
    sales.merge(menu, on="dish_id")
         .groupby("category")["total_bill"]
         .sum()
)

plt.figure(figsize=(8,5))

category_revenue.plot(kind="bar")

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig("images/revenue_by_category.png")

plt.show()


# REVENUE BY CITY
city_revenue = (
    sales.merge(customers, on="customer_id")
         .groupby("city")["total_bill"]
         .sum()
)

plt.figure(figsize=(10,5))

city_revenue.plot(kind="bar")

plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig("images/revenue_by_city.png")

plt.show()


# PAYMENT METHOD DISTRIBUTION
sales["payment_method"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Payment Method Distribution")

plt.ylabel("")

plt.savefig("images/payment_method_distribution.png")

plt.show()


# PEAK ORDER HOURS
sales["order_time"] = pd.to_timedelta(sales["order_time"])

sales["hour"] = (
    sales["order_time"]
    .dt.total_seconds()
    .floordiv(3600)
    .astype(int)
)

hourly_orders = (
    sales.groupby("hour")
    .size()
    .sort_index()
)

plt.figure(figsize=(10, 5))

plt.plot(
    hourly_orders.index,
    hourly_orders.values,
    marker="o"
)

plt.title("Peak Order Hours")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")

plt.xticks(hourly_orders.index)

plt.grid(True)

plt.tight_layout()

plt.savefig("images/peak_order_hours.png")

plt.show()


# MEMBERSHIP DISTRIBUTION
customers["membership"].value_counts().plot(
    kind="bar"
)

plt.title("Membership Distribution")
plt.xlabel("Membership")
plt.ylabel("Customers")

plt.tight_layout()

plt.savefig("images/membership_distribution.png")

plt.show()


