-- Staging model for pricing data

SELECT
    *
FROM {{ source('raw', 'prices') }}