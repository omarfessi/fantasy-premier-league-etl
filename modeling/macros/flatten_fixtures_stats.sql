{% macro flatten_stats_from_raw_fixtures(stat_type) %}
    WITH flat_raw_fx_stats AS (
        SELECT
            code AS game_id,
            event AS gameweek_id,
            kickoff_time AS game_kickoff_time,
            CASE 
                WHEN flatten_stats.unnest.h IS NOT NULL THEN UNNEST(flatten_stats.unnest.h) 
            END AS h_player_stats,
            CASE 
                WHEN flatten_stats.unnest.a IS NOT NULL THEN UNNEST(flatten_stats.unnest.a) 
            END AS a_player_stats,
            ingestion_time
        FROM {{source('landing', 'raw_fixtures' )}} t
        CROSS JOIN UNNEST(t.stats) AS flatten_stats
        WHERE flatten_stats.unnest.identifier = '{{ stat_type }}'
    ), 
    stack_vertically_stats AS (
    
        SELECT 
            game_id,
            gameweek_id,
            game_kickoff_time, 
            h_player_stats.value as stat_value, 
            h_player_stats.element as player_id,
            'home' AS side,
            ingestion_time
        FROM flat_raw_fx_stats 
        WHERE h_player_stats.value not null
        UNION ALL
        SELECT 
            game_id,
            gameweek_id,
            game_kickoff_time, 
            a_player_stats.value as stat_value, 
            a_player_stats.element as player_id,
            'away' AS side,
            ingestion_time
        FROM flat_raw_fx_stats
        WHERE a_player_stats.value not null)

{% endmacro %}
