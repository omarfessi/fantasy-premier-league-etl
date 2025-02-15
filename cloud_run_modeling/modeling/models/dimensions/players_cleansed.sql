SELECT 
    id as player_id,
    first_name as player_first_name,
    second_name as player_second_name,
    web_name as player_name,
    position as player_position,
    team_id as player_team_code,
    cost as player_current_cost,
    total_points as player_total_points,
    ingestion_time
FROM {{source('fantasy_premier_league', 'raw_elements')}}


