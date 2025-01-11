WITH h_a_players_flat_stats AS ({{ flatten_stats_from_raw_fixtures('penalties_saved') }})

SELECT * FROM h_a_players_flat_stats
