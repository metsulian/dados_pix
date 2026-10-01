import requests
import json

url = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/TransacoesPixPorMunicipio(DataBase=@DataBase)?@DataBase='20201'"

def get_dataframe(n_ultimos = 10000):
    params = {
        '$top': n_ultimos
    }

    request = requests.get(url, params=params)
    with open('pix_dados.json', 'w') as f:
        json.dump(request.json()['value'], f, ensure_ascii=False)

get_dataframe(url, 10000)