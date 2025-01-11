SELECT 
    id as team_id,
    name as team_name,
    short_name as team_short_name,
    strength as team_strength, 
    strength_overall_home,
    strength_overall_away,
    strength_attack_home,
    strength_attack_away,
    strength_defence_home,
    strength_defence_away,
    ingestion_time
FROM {{source('landing', 'raw_teams')}}