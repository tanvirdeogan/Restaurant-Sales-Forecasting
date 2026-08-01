use restaurant_db;

select * from customers;
select * from menu;
select * from sales;

select count(*) as total_customers
from customers;

select count(*) as total_menu_items
from menu;

select count(*) as total_orders
from sales;

-- total revenue
select
sum(total_bill) as total_revenue
from sales;

-- average bill amount
select
avg(total_bill) as average_bill
from sales;

-- highest bill
select
max(total_bill) as highest_bill
from sales;

-- lowest bill
select
min(total_bill) as lowest_bill
from sales;

-- total quantity sold
select
sum(quantity) as total_items_sold
from sales;