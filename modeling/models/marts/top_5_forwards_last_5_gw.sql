SELECT 
player_name, 
player_position, 
stat_value, 
goals.gameweek_id,
points.value AS unit_value,
points.value * stat_value AS total_points
FROM {{ref('goals_scored_stats')}} goals
JOIN {{ref('players_cleansed')}} players ON goals.player_id = players.player_id
JOIN {{ref('stat_points')}} points ON points.position = players.player_position
WHERE stat = 'goals_scored'
ORDER BY stat_value DESC