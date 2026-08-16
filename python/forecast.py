import mysql.connector
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2210",
    database="restaurant_db"
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

daily_sales = daily_sales.sort_values("order_date")

daily_sales["day"] = daily_sales["order_date"].dt.day
daily_sales["month"] = daily_sales["order_date"].dt.month
daily_sales["day_of_week"] = daily_sales["order_date"].dt.dayofweek
daily_sales["is_weekend"] = daily_sales["day_of_week"].isin([5, 6]).astype(int)

daily_sales["previous_day_sales"] = daily_sales["total_sales"].shift(1)
daily_sales["previous_week_sales"] = daily_sales["total_sales"].shift(7)

daily_sales["rolling_7_day_sales"] = (
    daily_sales["total_sales"]
    .shift(1)
    .rolling(7)
    .mean()
)

daily_sales = daily_sales.dropna()

features = [
    "total_quantity",
    "total_orders",
    "average_discount",
    "day",
    "month",
    "day_of_week",
    "is_weekend",
    "previous_day_sales",
    "previous_week_sales",
    "rolling_7_day_sales"
]

X = daily_sales[features]
y = daily_sales["total_sales"]

split = int(len(daily_sales) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\nImproved Forecasting Model")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 2))


plt.figure(figsize=(10, 5))

plt.plot(
    y_test.values,
    label="Actual Sales"
)

plt.plot(
    predictions,
    label="Predicted Sales"
)

plt.title("Actual vs Predicted Daily Sales")
plt.xlabel("Days")
plt.ylabel("Sales")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig("images/final_sales_forecast.png")

plt.show()

joblib.dump(model, "sales_forecasting_model.pkl")

print("\nForecasting model saved successfully.")


joblib.dump(model, "sales_forecasting_model.pkl")
joblib.dump(features, "forecast_features.pkl")

print("\nForecasting model saved successfully.")