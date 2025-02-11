import snowflake.connector
from contextlib import contextmanager
from .config import settings


@contextmanager
def get_snowflake_conn():
    conn = snowflake.connector.connect(
        user=settings.SNOWFLAKE_USER,
        password=settings.SNOWFLAKE_PASSWORD,
        account=settings.SNOWFLAKE_ACCOUNT,
        warehouse=settings.SNOWFLAKE_WAREHOUSE,
        database=settings.SNOWFLAKE_DATABASE,
        schema=settings.SNOWFLAKE_SCHEMA
    )
    try:
        yield conn
    finally:
        conn.close()
