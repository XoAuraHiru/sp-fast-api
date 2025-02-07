import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Snowflake connection
snowflake_url = f"snowflake://{os.getenv("SNOWFLAKE_USER")}:{os.getenv("SNOWFLAKE_PASSWORD")}@"\
                f"{os.getenv("SNOWFLAKE_ACCOUNT")}.snowflakecomputing.com/"\
                f"{os.getenv("SNOWFLAKE_DATABASE")}/{os.getenv("SNOWFLAKE_SCHEMA")}?"\
                f"warehouse={os.getenv("SNOWFLAKE_WAREHOUSE")}"

snowflake_engine = create_engine(snowflake_url)
SnowflakeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=snowflake_engine)
SnowflakeBase = declarative_base()

# Database dependency functions
def get_mysql_db():
    db = MySQLSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_snowflake_db():
    db = SnowflakeSessionLocal()
    try:
        yield db
    finally:
        db.close()