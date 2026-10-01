import requests


TIMEOUT = 120


def get_data(url, n_ultimos = 100, tentativas: int = 3):
    params = {
        '$top': n_ultimos
    }
    for i in range(tentativas):
        try: 
            request = requests.get(url, params=params, timeout=TIMEOUT)
            request.raise_for_status()
            return request.json()["value"]
        except requests.RequestException as e:
            print(f"Tentativa {i + 1} falhou: {e}")

    
