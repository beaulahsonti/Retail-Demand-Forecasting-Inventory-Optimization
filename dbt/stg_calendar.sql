-- Staging model for calendar data

SELECT
    *
FROM {{ source('raw', 'calendar') }}