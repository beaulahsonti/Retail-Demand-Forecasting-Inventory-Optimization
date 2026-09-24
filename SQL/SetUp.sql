## Verify RAW_CALENDAR Row Count
### Objective
Verify that the calendar dataset was successfully loaded into Snowflake.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_CALENDAR;


## Verify RAW_SALES_TRAIN_VALIDATION Row Count
### Objective
Verify that the M5 sales validation dataset was completely loaded into Snowflake.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION;

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_CALENDAR;

## Verify RAW_SELL_PRICES Row Count
### Objective
Verify that the complete M5 sell prices dataset was successfully loaded into Snowflake.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_SELL_PRICES;

## Verify RAW_SALES_TRAIN_EVALUATION Row Count
### Objective
Verify that the M5 evaluation sales dataset was successfully loaded into Snowflake.

SELECT COUNT(*)
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_EVALUATION

## Inspect RAW_SALES_TRAIN_VALIDATION Schema
### Objective
Inspect the structure, column names, and data types of the raw sales validation table before performing any transformations.

DESCRIBE TABLE RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION;


## Inspect Sample Sales Records
### Objective
Examine a small number of records from the raw sales table to understand how product, store, and daily sales information is represented.

SELECT *
FROM RETAIL_DEMAND.PUBLIC.RAW_SALES_TRAIN_VALIDATION
LIMIT 5;

## Inspect Calendar Data
### Objective
Examine the calendar table to understand how the M5 day identifiers correspond to actual dates and calendar information.

SELECT *
FROM RETAIL_DEMAND.PUBLIC.RAW_CALENDAR
LIMIT 10;