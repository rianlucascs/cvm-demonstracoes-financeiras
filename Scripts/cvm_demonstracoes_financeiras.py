
import pandas as pd
import wget
from zipfile import ZipFile
from os.path import join, dirname, abspath, exists
from os import listdir, remove
from datetime import date

class CVM_DemonstracoesFinanceiras:
    
    def __init__(self):
        self.url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
        path_base = dirname(dirname(abspath(__file__)))
        self.path_extracted_data = join(path_base, 'extracted_data')
        self.path_processed_data = join(path_base, 'processed_data')

        self.ano_atual = date.today().year

        self.nomes = ['BPA_con', 'BPA_ind', 'BPP_con', 'BPP_ind', 'DFC_MD_con', 'DFC_MD_ind',
                      'DFC_MI_con', 'DFC_MI_ind', 'DMPL_con', 'DMPL_ind', 'DRA_con', 'DRA_ind',
                      'DRE_con', 'DRE_ind', 'DVA_con', 'DVA_ind']
                 
    def _get_names_zip(self) -> list:
        arquivos_zip = []
        for ano in range(2011, self.ano_atual + 1):
            arquivos_zip.append(f'itr_cia_aberta_{ano}.zip')
        return arquivos_zip

    def _download_zip(self, names_zip):
        path = join(self.path_extracted_data, 'files_zip')
        for arq in names_zip:
            if not exists(join(path, arq)):
                wget.download(self.url+arq, path)

    def _extract_zip(self, names_zip):
        for arq in names_zip:
            path_file_zip = join(self.path_extracted_data, 'files_zip', arq)
            path_file_csv = join(self.path_extracted_data, 'files_csv')
            if not exists(join(path_file_csv, arq)):
                ZipFile(path_file_zip, 'r').extractall(path_file_csv)

    def _concat_files(self, update):
        for nome in self.nomes:
            arquivo = pd.DataFrame()
            for ano in range(2011, self.ano_atual):
                path_file = join(self.path_extracted_data, 'files_csv', f'itr_cia_aberta_{nome}_{ano}.csv')
                file_csv = pd.read_csv(path_file, sep=';', decimal=',', encoding='ISO-8859-1')
                arquivo = pd.concat([arquivo, file_csv])
            path_file_extracted_data = join(self.path_extracted_data, 'concat_csv', f'itr_cia_aberta_{nome}_2011-{self.ano_atual}.csv')
            if not exists(path_file_extracted_data) or update:
                arquivo.to_csv(path_file_extracted_data, index=False)

    def _transform_hdf(self):
        for nome in self.nomes:
            path_file_extracted_data = join(self.path_extracted_data, 'concat_csv', f'itr_cia_aberta_{nome}_2011-{self.ano_atual}.csv')
            path_file_processed_data = join(self.path_processed_data, f'itr_cia_aberta_{nome}_2011-{self.ano_atual}.h5')
            if not exists(path_file_processed_data):
                df_data = pd.read_csv(path_file_extracted_data, sep=',', decimal=',', encoding='ISO-8859-1')
                df_data.to_hdf(path_file_processed_data, key='df', mode='w', index=False)

    def _remove_files(self):
        for folder_1 in ['concat_csv', 'files_csv', 'files_zip']:
            path = join(self.path_extracted_data, folder_1)
            for file in listdir(path):
                if not '.txt' in file:
                    remove(join(path, file))

    def run(self, update=False):
        names_zip = self._get_names_zip()
        self._download_zip(names_zip)
        self._extract_zip(names_zip)
        self._concat_files(update)
        self._transform_hdf()
        self._remove_files()
        

if __name__ == '__main__':
    cvm_demonstracoes_financeiras = CVM_DemonstracoesFinanceiras()
    cvm_demonstracoes_financeiras.run(update=True)
