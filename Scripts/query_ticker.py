
import requests
from pandas import read_csv, read_csv
from io import StringIO

class QueryTicker:

    def __init__(self):
        pass

    def _get_empresas_listadas(self):
        url = 'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/3.%20Empresas%20listadas/todas_empresas_listadas.csv'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        return read_csv(StringIO(response.text), delimiter=';')
    
    def loc(self, ticker):
        table = self._get_empresas_listadas()
        loc_ticker = table.loc[table['codigo_de_negociacao'] == ticker][['codigo_de_negociacao', 'atividade_principal']]
        # print(loc_ticker)

        df = read_csv(r'D:\Projects\cvm-demonstracoes-financeiras\extracted_data\concat_csv\itr_cia_aberta_BPA_con_2011-2024.csv',
                      sep=',', encoding='utf-8')
        
        print(loc_ticker['atividade_principal'].iloc[0])

        print(df.loc[df['CNPJ_CIA'] == loc_ticker['atividade_principal'].iloc[0]])

QueryTicker().loc('VALE3')

    
    
    