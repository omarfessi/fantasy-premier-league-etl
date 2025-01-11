{% macro flatten_stats_from_raw_fixtures(stat_type) %}
(
    SELECT
        code,
        event AS gameweek,
        kickoff_time,
        CASE 
            WHEN flatten_stats.unnest.h IS NOT NULL THEN UNNEST(flatten_stats.unnest.h) 
        END AS h_player_stats,
        CASE 
            WHEN flatten_stats.unnest.a IS NOT NULL THEN UNNEST(flatten_stats.unnest.a) 
        END AS a_player_stats
    FROM {{source('landing', 'raw_fixtures' )}} t
    CROSS JOIN UNNEST(t.stats) AS flatten_stats
    WHERE flatten_stats.unnest.identifier = '{{ stat_type }}'
)
{% endmacro %}
