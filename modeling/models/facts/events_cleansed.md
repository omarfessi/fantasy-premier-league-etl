{% docs events_cleansed %}

This model selects and transforms data from the 'raw_events' table in the 'landing' schema.
It filters the events to include only those where the current date is greater than the event date
and the data has been checked.

{% enddocs %}