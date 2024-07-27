import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from statistics import median


class BaseDetectorOutlier:
    def __init__(self, csv_path, epsilon=3):
        self.id_arquivo = csv_path.split('/')[-1]
        self.infos = pd.read_csv(csv_path, sep=';')
        self.codigos = []
        self.datas = []
        self.secretarias = []
        self.epsilon = epsilon    # valor básico para os cálculos dos limites
        self.limite_inferior = 0  # sempre maior ou igual a zero
        self.limite_superior = 0  # sempre positivo
        self.metrica_basica  = 0  # média ou mediana
        self.desvio_padrao   = 0
        self.nome_metrica = ''
        self.dados = self.__processar_dados()
        self.__gerar_valores()

    def __processar_dados(self):
        """
        escolhe a coluna para ser processada,
        troca todas as vírgulas por ponto,
        transforma os dados em float32 e
        retira todos valores nulos.
        return: numpy array-float32 com uma dimensão
        """

        self.dados = self.infos['valores_valor'].values
        self.dados = np.array(self.dados, dtype='float32')
        self.codigos = self.infos['codigo'].values
        self.datas = self.infos['valores_data']
        self.secretarias = self.infos['fonte']
        self.valores_codigo = self.infos['valores_codigo']

        dados_nao_nulos = []
        for d in self.dados:
            if d > 0:
                dados_nao_nulos.append(d)
        return np.array(dados_nao_nulos)

    def __gerar_valores(self, mediana=True):
        if mediana:
            self.nome_metrica = 'mediana'
            self.metrica_basica = median(self.dados)
        else:
            self.nome_metrica = 'média'
            self.metrica_basica = self.dados.mean()

        self.desvio_padrao = self.dados.std()
        self.limite_inferior = max(self.metrica_basica - self.desvio_padrao - self.epsilon, 0)
        self.limite_superior = self.metrica_basica + self.desvio_padrao + self.epsilon

    def get_outliers(self):
        outliers = []
        for codigo, dado, secretaria, val_cod in zip(self.codigos,
                                                     self.dados,
                                                     self.secretarias,
                                                     self.valores_codigo):
            if dado < self.limite_inferior or dado > self.limite_superior:
                outliers.append([self.id_arquivo,
                                 val_cod,
                                 dado,
                                 self.metrica_basica,
                                 secretaria,
                                 self.desvio_padrao,
                                 self.limite_superior,
                                 self.limite_inferior])
        return outliers

    def descricao(self):
        print('Métrica utilizada:', self.nome_metrica)
        print("Valor da métrica:", self.metrica_basica)
        print('Epsilon utilizado:', self.epsilon)
        print('Limite inferior:', self.limite_inferior)
        print('Limite superior:', self.limite_superior)
        print('Desvio padrão:', self.desvio_padrao)

    def escrever_csv(self):
        if not os.path.exists(''):
            file = open(csv_name, 'a')
            file.write('codigo;valor_outlier;data;fonte\n')
        else:
            file = open(csv_name, 'a')

        with open(csv_name, 'a') as file:
            for outlier in self.get_outliers():
                for i in range(len(outlier)-1):
                    file.write(str(outlier[i]) + ';')
                file.write(str(outlier[-1]) + '\n')

if __name__ == '__main__':
    load_dotenv()
    CAMINHO_BASE = f'{os.getenv("CAMINHO_SAIDA")}'
    dicionario_outliers = []
    for file in os.listdir(CAMINHO_BASE + '/2_silver/'):
        test = BaseDetectorOutlier(CAMINHO_BASE + '/2_silver/' + file, 0)
        test.descricao()

        outliers = test.get_outliers()

        if len(outliers) == 0:
            print("Nenhum outlier encontrado.")
        else:
            print()
            for outlier in outliers:
                print('Código:', outlier[0])
                print('Valor encontrado:', outlier[1])
                print('Data:', outlier[2])
                print('Fonte:', outlier[3])
                print()

        test.escrever_csv()
