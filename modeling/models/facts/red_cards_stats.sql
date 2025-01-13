{{
    config(
        materialized='incremental',
        unique_key=['game_id', 'gameweek_id']
    )
}}

{{ flatten_stats_from_raw_fixtures('red_cards') }} --here I used a macro to relax this SQL file ( Ephemeral models are also possible)
SELECT 
stack_vertically_stats.game_id,
stack_vertically_stats.gameweek_id,
stack_vertically_stats.game_kickoff_time,
stack_vertically_stats.player_id,
players.player_name,
stack_vertically_stats.side,
stack_vertically_stats.stat_value,
points.value AS unit_value,
points.value * stat_value AS total_points,
stack_vertically_stats.ingestion_time AS ingestion_time
FROM stack_vertically_stats
JOIN {{ref('players_cleansed')}} players ON players.player_id = stack_vertically_stats.player_id
JOIN {{ref('stat_points')}} points ON points.position = players.player_position
WHERE stat = 'red_cards'
{% if is_incremental() %}

AND stack_vertically_stats.ingestion_time >= (SELECT coalesce(max(ingestion_time),'1900-01-01') FROM {{ this }} )

{% endif %}

