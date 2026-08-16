import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

query = """
SELECT
    order_date,
    quantity,
    discount,
    total_bill
FROM sales
"""

sales = pd.read_sql(query, connection)

connection.close()

print(sales.head())
print(sales.shape)


# SALES DATA
sales["order_date"] = pd.to_datetime(sales["order_date"])

daily_sales = (
    sales.groupby("order_date")
    .agg(
        total_sales=("total_bill", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("total_bill", "count"),
        average_discount=("discount", "mean")
    )
    .reset_index()
)

daily_sales["day"] = daily_sales["order_date"].dt.day
daily_sales["month"] = daily_sales["order_date"].dt.month
daily_sales["day_of_week"] = daily_sales["order_date"].dt.dayofweek
daily_sales["is_weekend"] = daily_sales["day_of_week"].isin([5, 6]).astype(int)

print(daily_sales.head())
print(daily_sales.shape)


# SPLITTING THE DATA
features = [
    "total_quantity",
    "total_orders",
    "average_discount",
    "day",
    "month",
    "day_of_week",
    "is_weekend"
]

X = daily_sales[features]
y = daily_sales["total_sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# LINEAR REGRESSION MODEL
linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

mae = mean_absolute_error(y_test, linear_predictions)
rmse = np.sqrt(mean_squared_error(y_test, linear_predictions))
r2 = r2_score(y_test, linear_predictions)

print("\nLinear Regression Results")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 2))


# RANDOM FOREST REGRESSION
random_forest = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

random_forest.fit(X_train, y_train)

rf_predictions = random_forest.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_predictions)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_predictions))
rf_r2 = r2_score(y_test, rf_predictions)

print("\nRandom Forest Results")
print("MAE:", round(rf_mae, 2))
print("RMSE:", round(rf_rmse, 2))
print("R2 Score:", round(rf_r2, 2))


# COMPARISON
comparison = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "MAE": [mae, rf_mae],
    "RMSE": [rmse, rf_rmse],
    "R2 Score": [r2, rf_r2]
})

print("\nModel Comparison")
print(comparison)

best_model = linear_model
best_predictions = linear_predictions

print("\nBest Model: Linear Regression")



import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))

plt.plot(
    y_test.values,
    label="Actual Sales",
    marker="o"
)

plt.plot(
    best_predictions,
    label="Predicted Sales",
    marker="o"
)

plt.title("Actual vs Predicted Daily Sales")
plt.xlabel("Test Data")
plt.ylabel("Sales")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig("images/actual_vs_predicted_sales.png")

plt.show()

# SAVING
import joblib

joblib.dump(best_model, "sales_prediction_model.pkl")

print("\nModel saved successfully.")