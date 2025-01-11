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
WHERE current_date > event_date AND data_checked = true