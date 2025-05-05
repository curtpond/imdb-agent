"""Snowflake configuration settings."""

SNOWFLAKE_CONFIG = {
    'account': 'KNXRWEH-XIB19247',
    'user': 'CURTPOND',
    'warehouse': 'COMPUTE_WH',  # default warehouse
    'database': 'IMDB_DB',
    'schema': 'MOVIES'
}

# Add any additional configuration settings here
DEFAULT_TIMEOUT = 60  # seconds
RETRY_COUNT = 3
