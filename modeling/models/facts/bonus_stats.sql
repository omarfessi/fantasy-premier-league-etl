WITH h_a_players_flat_stats AS ({{ flatten_stats_from_raw_fixtures('bonus') }})

SELECT * FROM h_a_players_flat_stats