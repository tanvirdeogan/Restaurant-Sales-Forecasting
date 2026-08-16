import mysql.connector
import pandas as pd


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2210",
    database="restaurant_db"
)

customers = pd.read_sql("SELECT * FROM customers", connection)
menu = pd.read_sql("SELECT * FROM menu", connection)
sales = pd.read_sql("SELECT * FROM sales", connection)

connection.close()


# DISHES TO STOCK MORE
dish_sales = (
    sales.merge(menu, on="dish_id")
    .groupby(["dish_id", "dish_name", "category"])
    .agg(
        quantity_sold=("quantity", "sum"),
        revenue=("total_bill", "sum")
    )
    .reset_index()
    .sort_values("quantity_sold", ascending=False)
)

top_dishes = dish_sales.head(5)

print("\nDishes to Stock More")
print(top_dishes[[
    "dish_name",
    "category",
    "quantity_sold",
    "revenue"
]])


# UNDERPERFORMING DISHES
underperforming = dish_sales.tail(5).sort_values(
    "quantity_sold"
)

print("\nUnderperforming Menu Items")
print(underperforming[[
    "dish_name",
    "category",
    "quantity_sold",
    "revenue"
]])


# BUSIEST DAYS
sales["order_date"] = pd.to_datetime(sales["order_date"])

daily_orders = (
    sales.groupby("order_date")
    .agg(
        total_orders=("order_id", "count"),
        total_sales=("total_bill", "sum")
    )
    .reset_index()
    .sort_values("total_orders", ascending=False)
)

busy_days = daily_orders.head(10)

print("\nBusiest Days")
print(busy_days)


# DAY REQUIRING MORE STAFF
sales["day_of_week"] = sales["order_date"].dt.day_name()

weekday_orders = (
    sales.groupby("day_of_week")
    .agg(
        total_orders=("order_id", "count"),
        total_sales=("total_bill", "sum")
    )
    .reset_index()
    .sort_values("total_orders", ascending=False)
)

print("\nStaffing Recommendation by Day")
print(weekday_orders)


# PEAK HOURS
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
    .reset_index(name="total_orders")
    .sort_values("total_orders", ascending=False)
)

print("\nPeak Hours")
print(hourly_orders.head(5))






top_revenue_dishes = dish_sales.sort_values(
    "revenue",
    ascending=False
).head(5)

print("\nTop Revenue Generating Dishes")
print(
    top_revenue_dishes[
        ["dish_name", "category", "quantity_sold", "revenue"]
    ]
)

print("\nHighest Revenue Items:")
for dish in top_revenue_dishes["dish_name"]:
    print("-", dish)


print("\nRECOMMENDATIONS")

print("\nStock More:")
for _, row in top_dishes.iterrows():
    print(
        f"- {row['dish_name']}: "
        f"{row['quantity_sold']} units sold, "
        f"revenue ₹{row['revenue']:,.2f}"
    )

print("\nReview Underperforming Items:")
for _, row in underperforming.iterrows():
    print(
        f"- {row['dish_name']}: "
        f"{row['quantity_sold']} units sold, "
        f"revenue ₹{row['revenue']:,.2f}"
    )

print("\nIncrease Staffing On:")
for _, row in weekday_orders.head(3).iterrows():
    print(
        f"- {row['day_of_week']}: "
        f"{row['total_orders']} orders"
    )

print("\nPeak Staffing Hours:")
for _, row in hourly_orders.head(3).iterrows():
    print(
        f"- {int(row['hour'])}:00: "
        f"{row['total_orders']} orders"
    )