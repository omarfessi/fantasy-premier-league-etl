{{ config(
  materialized='incremental',
  unique_key=['stat_by_player_by_game_id'],
  incremental_strategy='merge',
  merge_update_columns=['value', 'last_updated'],
  partition_by={
      "field": "game_kickoff_time",
      "data_type": "TIMESTAMP",
      "granularity": "day"
    },
  cluster_by = "stat_by_player_by_game_id",
)}}

WITH flat_stats_data AS

(SELECT
  code AS game_id,
  event AS gameweek_id,
  kickoff_time AS game_kickoff_time,
  flat_stats.element.identifier,
  awaytable.element.element AS player_id,
  awaytable.element.value AS value,
  'away' AS side
  
FROM
 {{ source('fantasy_premier_league', 'raw_fixtures')}}
CROSS JOIN
  UNNEST (stats.list) AS flat_stats
CROSS JOIN
  UNNEST (flat_stats.element.a.list) AS awaytable

UNION ALL

SELECT
  code AS game_id,
  event AS gameweek_id,
  kickoff_time AS game_kickoff_time,
  flat_stats.element.identifier,
  hometable.element.element AS player_id,
  hometable.element.value AS value,
  'home' AS side
FROM
 {{ source('fantasy_premier_league', 'raw_fixtures')}}
CROSS JOIN
  UNNEST (stats.list) AS flat_stats
CROSS JOIN
  UNNEST (flat_stats.element.h.list) AS hometable
  ),
data_with_surrogate_key AS (
    SELECT
    *,
    {{ dbt_utils.generate_surrogate_key(['game_id', 'identifier', 'player_id'])}} as stat_by_player_by_game_id,
    {{ dbt.current_timestamp() }} as last_updated
    FROM flat_stats_data
  )

  SELECT data_with_surrogate_key.* FROM data_with_surrogate_key
  {% if is_incremental() %}

  LEFT JOIN {{ this }} as existing_stats ON existing_stats.stat_by_player_by_game_id = data_with_surrogate_key.stat_by_player_by_game_id
  WHERE
  existing_stats.stat_by_player_by_game_id IS NULL
  OR existing_stats.value != data_with_surrogate_key.value
  {% endif %}