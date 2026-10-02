from src.utils.database import clean_database, upload_sql, _get_engine, run_query, setup_tables
from src.utils.api_requests import get_data

from src.config import API_URL

DB_CONNECTION = "postgresql+psycopg2://app:app_pass@localhost:3000/appdb"

data = get_data(API_URL)
engine = _get_engine(DB_CONNECTION)
print(clean_database(engine))
print(upload_sql(engine, data))
print(setup_tables(engine))

query = """
    SELECT *
    FROM "DadosSilver"
    WHERE id = 1;
"""
print(run_query(engine, query))