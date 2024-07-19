import requests
from pprint import pprint
import time
import json
import os 
# site
# https://egov.santos.sp.gov.br/dadosabertos/listar/dados

# lista secretarias
# https://egov.santos.sp.gov.br/dadosabertos/backend/api/listar-filtros

# filtro de secretarias
# https://egov.santos.sp.gov.br/dadosabertos/listar/dados?secretarias=2

#TODO Apliar filtro para as secretarias específicas, não é necessário baixar de todas
#TODO Utilizar os requests com a lib asyncio, para fazer requests mais rapidos de forma asíncrona
#TODO Melhorar tratativas de erros
#TODO Achar uma forma de rodar o processo automático (depende de onde será e como será hospedados o código)

url_secretarias = 'https://egov.santos.sp.gov.br/dadosabertos/backend/api/listar-dados?page='
url_dados = 'https://egov.santos.sp.gov.br/dadosabertos/backend/api/detalhes/downloads/json/'

response = requests.get(url_secretarias+'1')
dados = response.json()

first_page = 1
last_page = dados['last_page']
# codes = [5401]
for i in range(first_page, last_page+1):
    print('page: ', i)
    time.sleep(5)
    response = requests.get(f'{url_secretarias}{i}')
    try:
        dados = response.json()
    except Exception as e:
        try:
            time.sleep(5)
            dados = response.json()
        except Exception as e:
            dados = {
                "data": [{'codigo': f'erro-pagina-{i}'}]
            }

    for d in dados['data']:
        time.sleep(1)
        c = d['codigo']
        print('code: ', c)
        response = requests.get(f'{url_dados}{c}')
        try:
            dados = response.json()
        except requests.exceptions.JSONDecodeError as e:
            time.sleep(30)
            try:
                dados = response.json()
            except Exception as e:
                c = f"{d['codigo']}-erro"
                dados = {"erro: ": str(e)}
                time.sleep(60)

        nome_do_arquivo = f"{c}.json"
        pasta = 'etis'
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        # Caminho completo para o arquivo
        caminho_do_arquivo = os.path.join(pasta, nome_do_arquivo)
        with open(caminho_do_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)