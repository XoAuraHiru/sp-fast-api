from .sf_connection import SnowflakeConnector

def get_snowflake() -> SnowflakeConnector:
    return SnowflakeConnector()
