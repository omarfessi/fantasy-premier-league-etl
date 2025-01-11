{{
    config(
        materialized='incremental',
        unique_key=['event_id']
    )
}}
SELECT 
    id AS event_id,
    gameweek,
    average_fplmanager_score,
    highest_fplmanager_score,
    highest_scoring_fplmanager_id,
    fplmanagers_count,
    data_checked,
    event_date,
    chips_played,
    most_selected_player as most_selected_player_id,
    most_transferred_player_in AS most_transferred_player_in_id,
    most_captained AS most_captained_player_id,
    most_vice_captained AS most_vice_captained_player_id,
    top_player_info,
    transfers_made,
    ingestion_time
FROM
{{ source('landing', 'raw_events') }}
WHERE data_checked = true

{% if is_incremental() %}

AND ingestion_time >= (SELECT coalesce(max(ingestion_time),'1900-01-01') FROM {{ this }} )

{% endif %}