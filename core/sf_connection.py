import logging
import os
import time

from snowflake.connector import DictCursor
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SnowflakeConnector:
    def __init__(self):
        self.engine = None
        self.session = None
        self.connection = None

    def connect(self):
        if not self.engine:
            try:
                url = URL(
                    account=os.getenv('SNOWFLAKE_ACCOUNT'),
                    user=os.getenv('SNOWFLAKE_USER'),
                    password=os.getenv('SNOWFLAKE_PASSWORD'),
                    database=os.getenv('SNOWFLAKE_DATABASE'),
                    schema=os.getenv('SNOWFLAKE_SCHEMA'),
                    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                )

                self.engine = create_engine(url)
                self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                self.connection = self.engine.raw_connection()

            except Exception as e:
                raise

    def get_session(self):
        if not self.engine:
            self.connect()
        return self.session()

    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection

    def commit_bulk_records(self, query: str, params: list):
        with self.get_connection().cursor() as cursor:
            cursor.executemany(query, params)
            self.get_connection().commit()

    def commit_record(self, query: str, params: list):
        with self.get_connection().cursor() as cursor:
            cursor.execute(query, params)
            self.get_connection().commit()

    def fetch_records(self, query: str, params: list):
        with self.get_connection().cursor(DictCursor) as cursor:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records

    def close(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None
