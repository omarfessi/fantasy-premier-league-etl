
WITH h_a_players_flat_stats AS ({{ flatten_stats_from_raw_fixtures('goals_scored') }})
SELECT 
	code,
	gameweek,
	kickoff_time, 
	h_player_stats.value as stat_value, 
	h_player_stats.element as player_id,
	'home' AS side
FROM h_a_players_flat_stats 
WHERE h_player_stats.value not null
UNION ALL
SELECT 
	code,
	gameweek,
	kickoff_time, 
	a_player_stats.value as stat_value, 
	a_player_stats.element as player_id,
	'away' AS side
FROM h_a_players_flat_stats
WHERE a_player_stats.value not null

