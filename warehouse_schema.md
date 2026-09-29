# Raw BigQuery Warehouse Tables

Project:
glowing-net-510009-v1

Dataset:
retail_demand

## raw_calendar

Source:
calendar.csv

Purpose:
Stores M5 calendar, date, week and event information.

Key fields:
- date
- wm_yr_wk
- weekday
- wday
- month
- year
- event_name_1
- event_type_1
- event_name_2
- event_type_2

## raw_sales

Source:
sales_train_validation.csv

Purpose:
Stores raw M5 historical sales data in wide format.

Key fields:
- id
- item_id
- dept_id
- cat_id
- store_id
- state_id
- d_1, d_2, d_3, ...

## raw_prices

Source:
sell_prices.csv

Purpose:
Stores weekly selling price information.

Key fields:
- store_id
- item_id
- wm_yr_wk
- sell_price