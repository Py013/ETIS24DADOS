# ETIS24DADOS
Área da Squad de Dados

## Configuração setup local

Instalar e ativar virtualenv

```bash
python3 -m venv .venv
# Linux/Mac
source .venv/bin/activate
```

Instalar dependencias

```bash
pip install -U pip && pip install -r requirements.txt
```

Configurar variáveis de ambiente local

```bash
# Criar arquivo .env
URL_BASE_SECRETARIAS=https://egov.santos.sp.gov.br/dadosabertos/backend/api
URL_BASE_DADOS=https://egov.santos.sp.gov.br/dadosabertos/backend/api/detalhes/downloads/json/
IS_DEV_LOCAL=True
DEV_LOCAL_MAX_REQUEST=1
QTD_LISTAS_PAGINA=250
ID_SECRETARIAS=2907, 4681, 2859, 576, 779
ID_AUTARQUIAS=822, 1736
ESPERA_REQUISICOES=1.29
CAMINHO_SAIDA=etis

```

Fazer o build da imagem

```bash
docker image build -t python-dados-etis .
```

Executar o container 
`Persistindo volume de etis com arquivos .json`

```bash
docker container run -d --env-file=.env -v ${PWD}/etis:/etis python-dados-etis
```
