from src.utils.api_requests import get_sequential_and_upload
from src.utils.database import clean_database, upload_sql, _get_engine, run_query, setup_tables

from src.config import API_URL, DB_CONNECTION

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

engine = _get_engine(DB_CONNECTION)

print(clean_database(engine))
print(get_sequential_and_upload(engine, API_URL, '202606', n_meses=24, n_dados_mes=6000))
print(setup_tables(engine))

query_1 = """
    SELECT *
    FROM "DadosSilver"
    LIMIT 5;
"""

query_2 = """
    SELECT "Estado", "Share_Nacional_Estado"
    FROM "DadosEstadoGold"
    WHERE "AnoMes" = '2025-06-01'
    ORDER BY "Share_Nacional_Estado" DESC
    LIMIT 5;
"""

query_3 = """
    SELECT *
    FROM "DadosMunicipioGold"
    LIMIT 5;
"""


print(run_query(engine, query_1))
print('########################')
print(run_query(engine, query_2))
print('########################')
print(run_query(engine, query_3))