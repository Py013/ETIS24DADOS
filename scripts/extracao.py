import requests, json, os
from time import sleep
from ptymer import Timer
from dotenv import load_dotenv

load_dotenv() 
url_dados = os.getenv('URL_BASE_DADOS')
qtd = os.getenv('QTD_LISTAS_PAGINA') # Quantidade de listas por página
url_listas = f"{os.getenv('URL_BASE_SECRETARIAS')}/listar-dados?per_page={qtd}"
secretarias = os.getenv('ID_SECRETARIAS').split(',') # Códigos das secretarias: SEDUC, SEFIN, SESEG
autarquias = os.getenv('ID_AUTARQUIAS').split(',') # Códigos das autarquias: CET
tempo_espera = float(os.getenv('ESPERA_REQUISICOES', 1.28)) # Segundos
if not os.path.exists(caminho_saida := f"{os.getenv('CAMINHO_SAIDA', 'etis')}/1_bronze/"): os.makedirs(caminho_saida) # Cria a pasta de saída
# Configurações de acesso aos dados


def acessarListas(url: str, pagina: int):
    print(f"Página {pagina}!")
    try:
        response = requests.get(f'{url}{pagina}')
        response.raise_for_status()
        data = response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print('Erro 429 - Muitas requisições!')
            sleep(30)

    except Exception as e:
        print(f'Erro em acessar página {pagina}!\n Erro: {e}\nResponse:{response}')

    else:
        return data['data']

    return acessarListas(url, pagina)
# Função para acessar as listas


def acessarDados(url: str, c: int, depth: int, caminho_saida: str):
    print(f"Código {c}!")
    try:
        response = requests.get(f'{url}{c}')
        response.raise_for_status()
        data = response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print('Erro 429 - Muitas requisições!')
            sleep(30)
    
    except Exception as e:
        print(f'Erro em acessar dados de {c}!\n Erro: {e}\nResponse:{response}')
    
    else:
        salvarArquivo(data, c, caminho_saida)
        return

    if depth < 3: acessarDados(url, c, depth+1, caminho_saida) # Tenta acessar novamente
    else: salvarArquivo({"erro": str(e)}, f'{c}_erro', caminho_saida) # Salva o erro
# Função para acessar os dados (json)


def salvarArquivo(dados: json, c: int, pasta: str):
    try:
        with open(os.path.join(pasta, f'{c}.json'), 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

    except Exception as e:
        print(f'Erro ao salvar arquivo {c}.json! Erro: \n{e}')
# Função para salvar os arquivos


if __name__ == '__main__':
    listaCodigos = []

    for cod_secretaria in secretarias:
        print(f'Secretaria {cod_secretaria}!')
        last_page = requests.get(f'{url_listas}&secretarias={cod_secretaria}&page=1').json()['last_page'] # Pega o número da última página
        for i in range(1, last_page+1): # Itera sobre as páginas
            listaCodigos.extend([item['codigo'] for item in acessarListas(f'{url_listas}&secretarias={cod_secretaria}&page=', i)]) # Adiciona os códigos da página
            sleep(tempo_espera)
            
    for cod_autarquia in autarquias:
        print(f'Autarquia {cod_autarquia}!')
        last_page = requests.get(f'{url_listas}&autarquias={cod_autarquia}&page=1').json()['last_page'] # Pega o número da última página
        for i in range(1, last_page+1): # Itera sobre as páginas
            listaCodigos.extend([item['codigo'] for item in acessarListas(f'{url_listas}&autarquias={cod_autarquia}&page=', i)]) # Adiciona os códigos da página
            sleep(tempo_espera)

    print(f'Quantidade de códigos: {len(listaCodigos)}')

    with Timer(visibility=True) as tm:
        for c in listaCodigos:
            acessarDados(url_dados, c, 0, caminho_saida)
            sleep(tempo_espera)
        