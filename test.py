from src.utils.database import upload_sql, _get_engine, run_query
from src.utils.api_requests import get_data

from src.config import API_URL

DB_CONNECTION = "postgresql+psycopg2://app:app_pass@localhost:3000/appdb"

data = get_data(API_URL)
engine = _get_engine(DB_CONNECTION)
#upload_sql(engine, data)
query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    ORDER BY table_name;
"""
print(run_query(engine, query))