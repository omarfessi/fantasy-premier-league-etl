{{ 
    config(
        materialized='view'
        ) 
}}

WITH jointure AS (
    SELECT 
        players.player_name,
        players.player_position, 
        bonus_stats.gameweek_id,  
        bonus_stats.stat_value AS bonus
    FROM {{ref('bonus_stats')}} bonus_stats
    JOIN {{ref('players_cleansed')}} players
    ON bonus_stats.player_id = players.player_id
)
SELECT 
    CASE 
    WHEN player_position = 1 THEN 'Goal Keeper'
    WHEN player_position = 2 THEN 'Defender'
    WHEN player_position = 3 THEN 'Midfielder'
    WHEN player_position = 4 THEN 'Forward'
    END AS player_position, 
    bonus, 
    count(*) number_of_players
FROM jointure
GROUP BY bonus, player_position
ORDER BY number_of_players DESC