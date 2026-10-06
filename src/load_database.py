from src.utils.api_requests import get_sequential_and_upload
from src.utils.database import clean_database, _get_engine, run_query, setup_tables

from src.config import API_URL, DB_CONNECTION

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

engine = _get_engine(DB_CONNECTION)

clean_database(engine) #Limpa o Banco de Dados
get_sequential_and_upload(engine, API_URL, '202606', n_meses=48, n_dados_mes=10000) #Baixa os dados da API e carrega na tabela bronze em armazenar em RAM
setup_tables(engine) #Inicializa tabelas silver e gold