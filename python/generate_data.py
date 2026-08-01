import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# -------------------------------
# GENERATE CUSTOMERS DATASET
# -------------------------------

# create faker object for Indian names
fake = Faker("en_IN")

# cities
cities = [ "Ludhiana", "Delhi", "Mumbai", "Chandigarh", "Jaipur", "Pune", "Banglore", "Amritsar "]

# membership types
memberships = [ "Regular", "Silver", "Gold", "Premium" ]

customers = []

# generate 500 customers
for customer_id in range(1,501):
    customer = {
        "customer_id" : customer_id,
        "customer_name" : fake.name(),
        "gender" : random.choice(["Male", "Female"]),
        "city" : random.choice(cities),
        "membership" : random.choice(memberships)
    }
    customers.append(customer)

# create dataframe
customers_df = pd.DataFrame(customers)

# save csv
customers_df.to_csv("Dataset/customers.csv", index=False)

print("Customers dataset created successfully!")
print(customers_df.head())


# -------------------------------
# GENERATE MENU DATASET
# -------------------------------

menu_items = [

    ("Butter Chicken", "Main Course", 695, 220),
    ("Paneer Butter Masala", "Main Course", 380, 180),
    ("Dal Makhani", "Main Course", 320, 140),
    ("Shahi Paneer", "Main Course", 390, 190),
    ("Chicken Biryani", "Main Course", 420, 210),
    ("Veg Biryani", "Main Course", 300, 140),
    ("Karahi Chicken", "Main Course", 695, 220),
    ("Rara Chicken", "Main Course", 695, 220),
    ("Chilly Chicken", "Main Course", 650, 200),

    ("Paneer Tikka", "Starter", 280, 120),
    ("Chicken Tikka", "Starter", 320, 160),
    ("Hara Bhara Kabab", "Starter", 240, 100),
    ("Spring Rolls", "Starter", 220, 90),

    ("Masala Dosa", "South Indian", 180, 70),
    ("Plain Dosa", "South Indian", 150, 60),
    ("Idli Sambar", "South Indian", 120, 50),
    ("Vada Sambar", "South Indian", 130, 55),

    ("Veg Burger", "Fast Food", 150, 60),
    ("Chicken Burger", "Fast Food", 220, 90),
    ("French Fries", "Fast Food", 120, 45),
    ("Cheese Pizza", "Fast Food", 350, 160),
    ("Veg Pizza", "Fast Food", 320, 150),
    ("Chicken Pizza", "Fast Food", 420, 200),

    ("Cold Coffee", "Beverage", 180, 60),
    ("Hot Coffee", "Beverage", 120, 40),
    ("Tea", "Beverage", 60, 20),
    ("Fresh Lime Soda", "Beverage", 90, 30),
    ("Mango Shake", "Beverage", 150, 60),

    ("Chocolate Brownie", "Dessert", 180, 70),
    ("Ice Cream Sundae", "Dessert", 220, 90),
    ("Gulab Jamun", "Dessert", 120, 40),
    ("Rasmalai", "Dessert", 160, 70),
    ("Cheesecake", "Dessert", 250, 110)
]

menu = []

dish_id = 101

for item in menu_items:
    menu.append({
        "dish_id": dish_id,
        "dish_name": item[0],
        "category": item[1],
        "price": item[2],
        "cost": item[3],
    })

    dish_id += 1
menu_df = pd.DataFrame(menu)
menu_df.to_csv("dataset/menu.csv", index=False)

print("\nMenu Dataset Created Successfully!")
print(menu_df.head())


# -------------------------------
# GENERATE SALES DATASET
# -------------------------------

sales = []
payment_methods = ["Card", "Cash", "UPI"]
start_date = datetime(2026, 1, 1)

for order_id in range(1, 10001):

    customer_id = random.randint(1, 500)

    dish_ids = list(range(101, 131))

    dish_weights = [
        15, 14, 10, 9, 15, 8,
        9, 8, 5, 4,
        6, 3, 5, 4,
        7, 8, 6, 10, 8, 11,
        7, 5, 9, 4, 5,
        5, 4, 6, 5, 3
    ]

    dish_id = random.choices(
        dish_ids,
        weights=dish_weights
    )[0]
    
    quantity = random.choices(
        [1, 2, 3, 4, 5],
        weights=[50, 30, 12, 5, 3]
    )[0]

    unit_price = menu_df.loc[
        menu_df["dish_id"] == dish_id,
        "price"
    ].values[0]

    discount = random.choices(
        [0, 5, 10, 15],
        weights=[70, 15, 10, 5]
    )[0]

    payment_method = random.choices(
        ["UPI", "Card", "Cash"],
        weights=[60, 25, 15]
    )[0]

    # Generate a random order date within 6 months
    random_days = random.randint(0, 180)
    order_date = start_date + timedelta(days=random_days)

    # Generate realistic restaurant order hours
    # Generate realistic restaurant order time

    order_hour = random.choices(
        [11, 12, 13, 14, 18, 19, 20, 21, 22],
        weights=[5, 15, 20, 10, 10, 20, 12, 6, 2]
    )[0]

    order_minute = random.randint(0, 59)

    order_second = random.randint(0, 59)

    order_time = f"{order_hour:02}:{order_minute:02}:{order_second:02}"

    order_date = order_date.strftime("%Y-%m-%d")

    # Calculate total bill
    subtotal = unit_price * quantity
    total_bill = subtotal - (subtotal * discount / 100)

    # Save one sale
    sales.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "dish_id": dish_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "payment_method": payment_method,
        "order_date": order_date,
        "order_time" : order_time,
        "total_bill": round(total_bill, 2)
    })

sales_df = pd.DataFrame(sales)
sales_df.to_csv("dataset/sales.csv", index=False)

print("\nSales Dataset Created Successfully!")
print(sales_df.head())