WITH 
goals_contributions_value_per_position AS (
  SELECT * 
  FROM {{ref("stat_points")}}
  WHERE stat IN ('goals_scored', 'assists')

),
stats_per_players AS (
  SELECT
  ff.value,
  identifier,
  ff.player_id,
  pc.player_name,
  pc.player_position,
  g_contrib.stat,
  g_contrib.value as stat_value_per_position

FROM
  {{ref("flat_fixtures")}} AS ff
LEFT JOIN
  {{ref("players_cleansed")}} AS pc
ON
  ff.player_id = pc.player_id

LEFT JOIN goals_contributions_value_per_position AS g_contrib
ON pc.player_position = g_contrib.position
WHERE
  ff.identifier IN ('assists', 'goals_scored'))

SELECT player_name, SUM(SAFE_MULTIPLY(value, stat_value_per_position)) AS value
FROM stats_per_players
GROUP BY player_name