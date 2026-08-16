# Restaurant Sales Forecasting and Recommendation System

## Project Overview

The Restaurant Sales Forecasting and Recommendation System is a data science project developed to analyze restaurant sales data, identify important business trends, predict daily sales, and generate useful business recommendations.

The project stores customer, menu, and sales information in MySQL. Python is used for data loading, cleaning, analysis, visualization, machine learning, sales forecasting, and recommendation generation.

## Objectives

- Store restaurant data using a relational database.
- Analyze sales and customer data.
- Identify best-selling and underperforming menu items.
- Analyze revenue and customer trends.
- Identify peak ordering hours and busy days.
- Build a sales prediction model.
- Forecast daily restaurant sales.
- Generate recommendations for inventory and staffing.

## Technologies Used

- Python
- MySQL
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- MySQL Connector
- SQLAlchemy
- Joblib
- Git and GitHub
- Visual Studio Code
- MySQL Workbench

## Database

The project uses three main tables:

### Customers

Stores customer information.

Main fields:

- customer_id
- customer_name
- gender
- city
- membership

### Menu

Stores restaurant menu information.

Main fields:

- dish_id
- dish_name
- category
- price
- cost

### Sales

Stores transaction information.

Main fields:

- order_id
- customer_id
- dish_id
- quantity
- unit_price
- discount
- payment_method
- order_date
- order_time
- total_bill

## Project Workflow

```text
MySQL Database
       ↓
Data Loading
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Data Visualization
       ↓
Machine Learning
       ↓
Sales Forecasting
       ↓
Recommendation System