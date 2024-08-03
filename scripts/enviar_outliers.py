import csv
import requests
import os
from dotenv import load_dotenv

load_dotenv()
CAMINHO_BASE = f'{os.getenv("CAMINHO_SAIDA")}'

dir = os.path.join(f'{CAMINHO_BASE}/3_gold/outliers.csv')

with open(dir, mode='r', newline='') as file:
    outliers = csv.DictReader(file)
    for o in outliers:
        print('out: ', o)
        try:
            response = requests.post(f'{os.getenv("DOMINIO")}/Indicador/Add', json=o)
            if response.status_code == 200:
                print(f"Sucesso: {response.json()}")
            else:
                print(f"Falha na requisição: {response.status_code}, {response.text}")
        except Exception as e:
            print('Erro: ', e)
        