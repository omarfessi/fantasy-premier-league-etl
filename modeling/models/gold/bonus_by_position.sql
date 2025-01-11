{{ 
    config(
        materialized='view'
        ) 
}}

WITH jointure AS (
SELECT bronze_players.player_name,bronze_players.position, bonus_stats.gameweek,  bonus_stats.stat_value AS bonus
FROM {{ref('bonus_stats' )}}
JOIN bronze_players ON bonus_stats.player_id = bronze_players.player_id
)
SELECT position, bonus, count(*) number_of_players
FROM jointure
GROUP BY bonus, position
ORDER BY number_of_players DESC