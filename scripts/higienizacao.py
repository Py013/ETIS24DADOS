import pandas as pd
import json
import os

dados_json = []

dir_name = './etis/2_silver'

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

for filename in os.listdir("./etis/1_bronze"):
    filepath = os.path.join("./etis/1_bronze", filename)
    
    with open(filepath, "r") as file:
        if ".gitempty" in filename:
            continue
        else:
            data = json.load(file)
        
        dados_normalizados = pd.json_normalize(data)

        orgao = "autarquias" if len(dados_normalizados['autarquias'][0]) > 0 else "secretarias"

        dados_normalizados['id_orgao'] = dados_normalizados[orgao].apply(lambda x: x[0]['codigo'] if len(x) > 0 else None)
        dados_normalizados['sigla_orgao'] = dados_normalizados[orgao].apply(lambda x: x[0]['sigla'] if len(x) > 0 else None)
        dados_normalizados['metas_numero'] = dados_normalizados['metas'].apply(lambda x: x[0]['numero'] if len(x) > 0 else None)
        dados_normalizados['eixos_codigo'] = dados_normalizados['eixos'].apply(lambda x: x[0]['codigo'] if len(x) > 0 else None)
        dados_normalizados['tags_codigo'] = dados_normalizados['tags'].apply(lambda x: x[0]['codigo'] if len(x) > 0 else None)
        dados_normalizados['tipo_orgao'] = orgao
        dados_normalizados.drop(columns=['autarquias', 'secretarias'], inplace=True)
        dados_normalizados.drop(columns=['periodicidade.codigo', 'periodicidade.descricao'], inplace=True)

        valores_expanded = dados_normalizados['valores'].explode().apply(pd.Series)
        
        valores_expanded = valores_expanded.rename(columns={
            'valor': 'valores_valor',
            'data': 'valores_data',
            'codigo': 'valores_codigo',
            'descricao': 'valores_descricao'
        })

        dados_normalizados = dados_normalizados.drop(columns=['valores']).join(valores_expanded)

        
        dados_normalizados = dados_normalizados[dados_normalizados['valores_descricao'].isnull()]

        if len(dados_normalizados) > 0:
            output_filepath = os.path.join(dir_name, filename.replace(".json", ".csv"))
            dados_normalizados.to_csv(output_filepath, index=False, header=True, sep=";")
