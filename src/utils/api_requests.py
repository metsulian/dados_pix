import requests
import pandas as pd

from sqlalchemy import create_engine

TIMEOUT = 120

def get_data(url, n_ultimos = 10000, tentativas: int = 3):
    params = {
        '$top': n_ultimos
    }
    for i in range(tentativas):
        try: 
            request = requests.get(url, params=params, timeout=TIMEOUT)
            request.raise_for_status()
            return request.json()
        except requests.RequestException as e:
            print(f"Tentativa {i} falhou: {e}")

def load_sql(data, connection_string: str):
    df = pd.json_normalize(data)
    if df.empty: raise SystemExit("A API nao retornou registros")

    date = pd.Timestamp.now(tz="UTC")
    df["data_carregado"] = date

    engine = create_engine(connection_string)

    TABLE = f'Dados_Pix_{date}'
    df.to_sql(TABLE, engine, if_exists="replace", index=False)
    
    return True
