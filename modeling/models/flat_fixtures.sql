{{ config(
  materialized='incremental',
  unique_key=['game_id', 'identifier', 'player_id'],
  partition_by={
      "field": "ingestion_time",
      "data_type": "DATE",
      "granularity": "day"
    },
  cluster_by = "game_kickoff_time",
)}}

SELECT
  code AS game_id,
  event AS gameweek_id,
  kickoff_time AS game_kickoff_time,
  flat_stats.element.identifier,
  awaytable.element.element AS player_id,
  awaytable.element.value AS value,
  'away' AS side,
  ingestion_time
  
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
  'home' AS side,
  ingestion_time
FROM
 {{ source('fantasy_premier_league', 'raw_fixtures')}}
CROSS JOIN
  UNNEST (stats.list) AS flat_stats
CROSS JOIN
  UNNEST (flat_stats.element.h.list) AS hometable

{% if is_incremental() %}
WHERE ingestion_time >= (SELECT coalesce(max(ingestion_time),'1900-01-01') FROM {{ this }} )
{% endif %}