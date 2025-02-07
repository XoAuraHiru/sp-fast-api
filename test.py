from fastapi import FastAPI

from core.snowflake import test_snowflake_connection

app = FastAPI(title="Todo App API")

@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/test-snowflake")
def read_root():
    test_snowflake_connection()
    return {"Hello": "snowflake"}
