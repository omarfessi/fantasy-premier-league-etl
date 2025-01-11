SELECT 
    id as player_id,
    first_name as player_first_name,
    second_name as player_second_name,
    web_name as player_name,
    position as player_position,
    team_id as player_team_id,
    cost as player_current_cost,
    ingestion_time
FROM {{source('landing', 'raw_elements')}}


