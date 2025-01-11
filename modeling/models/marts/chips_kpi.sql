{{ 
    config(
        materialized='view'
        ) 
}}

WITH
flat_chips_per_gw AS (
  SELECT
    event_id,
    gameweek,
    flat_chips_played.unnest.chip_name AS chip_name,
    flat_chips_played.unnest.num_played AS num_played
FROM {{ref('events_cleansed')}} e
CROSS JOIN UNNEST(e.chips_played) AS flat_chips_played
)

SELECT gameweek, chip_name, num_played
FROM flat_chips_per_gw
ORDER BY event_id

    