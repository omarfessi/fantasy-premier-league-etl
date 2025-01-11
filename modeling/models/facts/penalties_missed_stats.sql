{{
    config(
        materialized='incremental',
        unique_key=['game_id', 'gameweek_id']
    )
}}

{{ flatten_stats_from_raw_fixtures('penalties_missed') }} --here I used a macro to relax this SQL file ( Ephemeral models are also possible)
SELECT * FROM stack_vertically_stats

{% if is_incremental() %}

where ingestion_time >= (SELECT coalesce(max(ingestion_time),'1900-01-01') FROM {{ this }} )

{% endif %}

