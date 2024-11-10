
from os.path import dirname, abspath, join, exists
from os import makedirs
from datetime import date
import wget
from zipfile import ZipFile
from pandas import DataFrame, read_csv, concat, read_hdf
from shutil import rmtree
import requests
from io import StringIO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CVM:
    """
    Classe responsável pelo download, extração, processamento e salvamento 
    dos dados financeiros da Comissão de Valores Mobiliários (CVM).

    A classe `CVM` oferece funcionalidades para:
    - Baixar arquivos ZIP contendo dados financeiros da CVM.
    - Extrair arquivos CSV de dentro dos arquivos ZIP.
    - Concatenar os dados CSV em um único arquivo HDF5.
    - Gerenciar diretórios temporários e salvar os dados processados.

    **Atributos:**
    - `url` (str): URL base para download dos arquivos ZIP contendo os dados.
    - `path_project` (str): Caminho do diretório do projeto.
    - `path_base` (str): Caminho base para armazenar os dados da CVM.
    - `path_tmp` (str): Caminho para o diretório temporário de arquivos baixados.
    - `path_files_zip` (str): Caminho para armazenar os arquivos ZIP.
    - `path_files_csv` (str): Caminho para armazenar os arquivos CSV extraídos.
    - `path_data` (str): Caminho para armazenar os arquivos HDF5 processados.
    - `ano_atual` (int): Ano atual, usado para determinar o intervalo de anos.
    - `names_archives_zip` (list): Lista de arquivos ZIP a serem baixados.
    - `nomes` (list): Lista de tipos de demonstrações financeiras a serem processadas.

    **Métodos:**
    - `__init__(self)`: Inicializa a classe `CVM`, configurando os diretórios e URLs.
    - `_wget_zip(self)`: Baixa os arquivos ZIP da CVM para o diretório especificado.
    - `_extract_zip(self)`: Extrai os arquivos CSV dos arquivos ZIP.
    - `_concat_files(self)`: Concatena os arquivos CSV em um arquivo HDF5.
    - `_dell_tmp(self)`: Apaga o diretório temporário após o processamento.
    - `get(self)`: Executa o processo completo de download, extração, concatenação e limpeza.

    **Exceções**:
    - `FileNotFoundError`: Se um arquivo necessário não for encontrado.
    - `json.JSONDecodeError`: Se ocorrer um erro ao decodificar arquivos JSON.
    - `Exception`: Para qualquer erro geral durante o processo de download, extração, concatenação ou salvamento.
    """

    def __init__(self, path_project = None):
        """
        Inicializa a classe `CVM`, configurando os diretórios de trabalho, URLs 
        e os nomes dos arquivos a serem processados.

        :param None: Nenhum parâmetro é necessário para a inicialização.
        :return: Nenhum valor retornado. Apenas configura os diretórios 
                 necessários e define os parâmetros para o download dos dados.
        """
        self.url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
        self.path_project = dirname(abspath(__file__)) if path_project == None else path_project
        self.path_base = join(self.path_project, '.CVM', 'demonstracoes_financeiras')
        self.path_tmp = join(self.path_base, 'tmp')
        self.path_files_zip = join(self.path_tmp, 'files_zip')
        self.path_files_csv = join(self.path_tmp, 'files_csv')
        self.path_data = join(self.path_base, 'data')
        self.path_control = join(self.path_data, '.control')

        self.ano_atual = date.today().year

        self.names_archives_zip = [f'itr_cia_aberta_{ano}.zip' for ano in range(2011, self.ano_atual + 1)]

        self.nomes = ['BPA_con', 'BPA_ind', 'BPP_con', 'BPP_ind', 'DFC_MD_con', 'DFC_MD_ind',
                      'DFC_MI_con', 'DFC_MI_ind', 'DMPL_con', 'DMPL_ind', 'DRA_con', 'DRA_ind',
                      'DRE_con', 'DRE_ind', 'DVA_con', 'DVA_ind']


    def _wget_zip(self):
        """
        Baixa os arquivos ZIP da CVM para o diretório especificado.

        Este método verifica se os arquivos ZIP listados em `self.names_archives_zip` 
        já existem no diretório de destino (`self.path_files_zip`). Para cada arquivo que não for encontrado, 
        a função realiza o download a partir da URL configurada (`self.url`).

        :param None: A função não recebe parâmetros externos, pois utiliza atributos internos da classe.
        :return: Nenhum valor retornado. A função apenas baixa os arquivos e registra logs.
        :raises Exception: Se ocorrer um erro durante o download de um arquivo, a exceção será registrada no log.
        """
        for arquivo in self.names_archives_zip:
            path_file = join(self.path_files_zip, arquivo)
            if not exists(path_file):
                try:
                    wget.download(self.url+arquivo, self.path_files_zip, bar=False)
                    logging.info(f"Download realizado com sucesso: {arquivo}")
                except Exception as erro:
                    logging.error(f"Erro ao fazer o download do arquivo '{arquivo}': {erro}")
            else:
                logging.info(f"Arquivo '{arquivo}' já existe. Nenhum download necessário.")
    
    def _extract_zip(self):
        """
        Extrai arquivos de um arquivo ZIP para o diretório de destino.

        Este método percorre a lista `self.names_archives_zip` e tenta abrir cada arquivo ZIP presente 
        no diretório `self.path_files_zip`. Para cada arquivo ZIP, a função extrai os arquivos contidos 
        nele para o diretório `self.path_files_csv`.

        :param None: A função não recebe parâmetros externos, pois utiliza atributos internos da classe.
        :return: Nenhum valor retornado. A função apenas realiza a extração dos arquivos e registra informações no log.
        :raises Exception: Caso ocorra um erro ao abrir o arquivo ZIP ou ao extrair arquivos do ZIP, a exceção será registrada no log.
        """
        for arquivo in self.names_archives_zip:
            path_file_zip = join(self.path_files_zip, arquivo)
            if exists(path_file_zip):
                try:
                    with ZipFile(path_file_zip, 'r') as zip_ref:
                        arquivos_no_zip = zip_ref.namelist()
                        for arquivo_zip in arquivos_no_zip:
                            try:
                                path_destino = join(self.path_files_csv, arquivo_zip)
                                if not exists(path_destino):
                                    zip_ref.extract(arquivo_zip, self.path_files_csv)
                                    logging.info(f"Arquivo '{arquivo_zip}' do ZIP '{arquivo}' extraído com sucesso.")
                                else:
                                    logging.info(f"Arquivo '{arquivo_zip}' do ZIP '{arquivo}' já existe. Nenhum download necessário.")
                            except Exception as erro:
                                logging.error(f"Erro ao extrair o arquivo '{arquivo_zip}' do ZIP '{arquivo}': {erro}")
                except Exception as erro:
                    logging.error(f"Erro ao abrir o arquivo ZIP '{arquivo}': {erro}")
            else:
                logging.warning(f"Arquivo '{arquivo}' não encontrado no diretório de origem.")

    def _concat_files(self):
        """
        Concatena e salva arquivos CSV em um arquivo HDF5.

        Este método percorre a lista de arquivos CSV (`self.nomes`) e, para cada nome, 
        tenta concatenar os arquivos CSV de 2011 até o ano atual. O arquivo concatenado é então salvo no formato HDF5 no diretório `self.path_data`. 

        :param None: A função não recebe parâmetros externos, pois utiliza atributos internos da classe.
        :return: Nenhum valor retornado. A função apenas realiza a concatenação dos arquivos CSV e o salvamento do arquivo HDF5.
        :raises Exception: Caso ocorra um erro ao abrir os arquivos CSV ou ao salvar o arquivo HDF5, a exceção será registrada no log.
        """
        for nome in self.nomes:
            arquivo = DataFrame()
            path = join(self.path_data, name_file_h5:=f'itr_cia_aberta_{nome}_2011-{self.ano_atual}.h5')
            if not exists(path):
                try:
                    for ano in range(2011, self.ano_atual):
                        file_csv = read_csv(
                            join(self.path_files_csv, name_file_csv:=f'itr_cia_aberta_{nome}_{ano}.csv'), 
                            sep=';', 
                            decimal=',', 
                            encoding='ISO-8859-1'
                            )
                        arquivo = concat([arquivo, file_csv])
                    arquivo.to_hdf(path, key='demontracoes_financeiras', mode='w', complib='zlib', complevel=5)
                    logging.info(f"Arquivo '{name_file_h5}' criado e salvo com sucesso.")
                except Exception as erro:
                    logging.error(f"Erro ao abrir o arquivo '{name_file_csv}': {erro}")
            else:
                logging.info(f"Arquivo '{name_file_h5}' já existe.")    

    def _dell_tmp(self):
        """
        Apaga o diretório temporário após o processamento.

        Este método verifica se o diretório temporário (`self.path_tmp`) existe e o remove após o término
        do processo de extração, concatenação e salvamento dos arquivos.

        :param None: Nenhum parâmetro é necessário.
        :return: Nenhum valor retornado.
        :raises Exception: Caso ocorra um erro ao tentar remover o diretório temporário.
        """
        if exists(self.path_tmp):
            try:
                rmtree(self.path_tmp)
                logging.info(f"Diretório 'tmp' e todo o seu conteúdo foram apagados com sucesso.")
            except Exception as e:
                logging.error(f"Erro ao tentar apagar o diretório 'tmp': {e}")
        else:
            logging.info(f"O diretório 'tmp' não existe.")


    def process_full_flow(self, update : bool = False):
        """
        Executa o processo completo de download, extração, concatenação e limpeza.

        Este método chama as funções `_wget_zip`, `_extract_zip`, `_concat_files` 
        e `_dell_tmp` para realizar todo o fluxo de download, extração, processamento e limpeza.

        :param update: Se `True`, o processo será forçado a rodar mesmo que já tenha sido executado antes.
        :return: Nenhum valor retornado. A função processa os dados e registra informações no log.
        """
        logging.info(f"Verificando se o processo precisa ser executado. Atualização solicitada: {update}")

        if not exists(self.path_control) or update:

            makedirs(self.path_base, exist_ok=True)
            makedirs(self.path_files_zip, exist_ok=True)
            makedirs(self.path_files_csv, exist_ok=True)
            makedirs(self.path_data, exist_ok=True)

            logging.info("Iniciando o download dos dados...")
            self._wget_zip()

            logging.info("Extraindo os arquivos do zip...")
            self._extract_zip()

            logging.info("Concatenando arquivos extraídos...")
            self._concat_files()

            logging.info("Removendo arquivos temporários...")
            self._dell_tmp()

            if not exists(self.path_control):
                logging.info(f"Criação do diretório de controle: {self.path_control}")
                makedirs(self.path_control, exist_ok=True)

            logging.info("Processo completo finalizado com sucesso.")
        else:
            logging.info(f"O processo já foi executado anteriormente. Para atualização, passe 'update=True'.")

    def _table_infos_stocks(self):
        url = 'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/3.%20Empresas%20listadas/todas_empresas_listadas.csv'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        return read_csv(StringIO(response.text), delimiter=';')
    
    def loc(self, symbol : str='VALE', file_name: str = 'BPA_con'):
        symbol = symbol.upper()
        table = self._table_infos_stocks()[['codigo', 'nome_do_pregao', 'codigo_de_negociacao', 'classificacao_setorial', 'cnpj', 'atividade_principal']]
        info_loc = table.loc[table['codigo'] == symbol]
        atividade_principal = info_loc['atividade_principal'].iloc[0]
        table_h5 = read_hdf(join(self.path_data, f'itr_cia_aberta_{file_name}_2011-{self.ano_atual}.h5'))
        return table_h5.loc[table_h5['CNPJ_CIA'] == atividade_principal]


