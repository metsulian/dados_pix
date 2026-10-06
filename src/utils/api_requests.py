from datetime import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from src.utils.database import clean_database, upload_sql, _get_engine, run_query, setup_tables
from sqlalchemy.engine import Engine

import logging
import requests
import time

logger = logging.getLogger(__name__)

TIMEOUT = 120

# Baixa uma quantidade n de dados do ano_mes da API
def get_data(url:str, ano_mes:str, n:int = 100, skip:int = 0, tentativas: int = 3):
    # Parametros para a chamada
    params = {
        "@DataBase": f"'{ano_mes}'",
        "$top": n
    }

    # Tenta retornar os dados 'tentativas' vezes
    for i in range(tentativas):
        try: 
            request = requests.get(url, params=params, timeout=TIMEOUT)
            request.raise_for_status()
            return request.json()["value"]
        except requests.RequestException as e:
            logger.info(f"Tentativa {i + 1} falhou: {e}")
            time.sleep(5)
    raise RuntimeError(f"Falha ao baixar {ano_mes} skip={skip}")


# Retorna uma colecao dos dados a partir de um mes, contando n_meses para tras e trazendo n_dados_mes dados
# eg. get_sequential_data(url, 202606, 6, 2000) retorna uma colecao de 12000 dados, com 2000 de 202606, 2000 dados
# de 202605, e assim por diante
def get_sequential_data(url:str, ano_mes:str, n_meses: int, n_dados_mes: int = 10000):
    inicio = datetime.strptime(str(int(ano_mes) + 1), "%Y%m")
    # Cria a colecao dos meses a serem iterados
    meses = [(inicio - relativedelta(months=i)).strftime("%Y%m") for i in range(1, n_meses+1)]
    data = []

    # Para cada mes, enquanto a quantidade de dados do mes nao for obtida, baixa novos dados
    for mes in tqdm(meses, desc=f"Baixando {len(meses) * n_dados_mes} dados dos meses desejados"):
        logger.info(f'Baixando dados do mes: {mes}...')
        n_dados_baixados = 0
        while n_dados_baixados < n_dados_mes:
            # Quantidade de dados para pedir para a API -> API nao suporta mais de 10000 por vez
            n_pedir = min(10000, n_dados_mes)
            logger.info(f'Baixando {n_pedir} dados...')
            _data = get_data(url, ano_mes=str(mes) ,n=n_pedir, skip=n_dados_baixados)

            if not _data:
                break

            n_dados_baixados += len(_data)
            logger.info(f'Baixados: {n_dados_baixados} dados')
            data.extend(_data)
        time.sleep(3)

    return data

# O mesmo que a funcao anterior, mas em vez de guardar os dados na memoria ate o final da execucao, 
# faz o upload para o banco de dados e limpa a memoria (melhor)
def get_sequential_and_upload(engine: Engine, url: str, ano_mes:str, n_meses: int, n_dados_mes: int = 10000):
    inicio = datetime.strptime(str(int(ano_mes) + 1), "%Y%m")
    # Cria a colecao dos meses a serem iterados
    meses = [(inicio - relativedelta(months=i)).strftime("%Y%m") for i in range(1, n_meses+1)]

    for mes in tqdm(meses, desc=f"Baixando {len(meses) * n_dados_mes} dados dos meses desejados"):
        logger.info(f'Baixando dados do mes: {mes}...')
        n_dados_baixados = 0
        while n_dados_baixados < n_dados_mes:
            # Quantidade de dados para pedir para a API -> API nao suporta mais de 10000 por vez
            n_pedir = min(10000, n_dados_mes)
            logger.info(f'Baixando {n_pedir} dados...')
            data = get_data(url, ano_mes=str(mes) ,n=n_pedir, skip=n_dados_baixados)

            if not data:
                break
            
            n_dados_baixados += len(data)
            logger.info(f'Baixados: {n_dados_baixados} dados')
            # Upa os dados para o postgresql
            upload_sql(engine, data)
        time.sleep(3)


