Este script implementa uma classe chamada `CVM` que automatiza o processo de download, extração, concatenação e armazenamento de dados financeiros da Comissão de Valores Mobiliários (CVM). A seguir está um resumo dos principais processos realizados pelo script:

### Resumo do Script:

1. **Download de Arquivos ZIP**:
   O script baixa arquivos ZIP contendo dados financeiros (como balanços e demonstrações financeiras) da CVM. Os arquivos são baixados do site da CVM para um diretório temporário.

2. **Extração dos Arquivos CSV**:
   Após o download, os arquivos ZIP são extraídos para um diretório temporário, gerando arquivos CSV com os dados financeiros.

3. **Concatenação de Arquivos CSV**:
   O script então concatena os arquivos CSV extraídos em um único arquivo HDF5 para facilitar o processamento e a análise dos dados. O arquivo HDF5 consolidado é salvo no diretório de dados do projeto.

4. **Limpeza dos Arquivos Temporários**:
   Após a concatenação, o script remove o diretório temporário usado durante o processo de download e extração dos arquivos.

5. **Processo Completo**:
   A função `process_full_flow()` executa todo o fluxo descrito (download, extração, concatenação e limpeza). Ela também verifica se o processo já foi executado anteriormente para evitar downloads desnecessários, a menos que o parâmetro `update=True` seja passado.

6. **Consultas Específicas (Localização de Dados)**:
   O script também oferece a funcionalidade de consultar os dados financeiros de uma empresa específica, utilizando o código da empresa (ex: 'VALE') e o tipo de demonstração financeira (ex: 'BPA_con'). O método `loc()` é utilizado para localizar e retornar a tabela de dados financeiros correspondentes.

7. **Logs**:
   O script utiliza a biblioteca `logging` para registrar informações detalhadas sobre o processo, incluindo sucessos e falhas em cada etapa.

### Funções e Atributos Importantes:

- **`_wget_zip()`**: Faz o download dos arquivos ZIP da CVM.
- **`_extract_zip()`**: Extrai os arquivos CSV dos arquivos ZIP.
- **`_concat_files()`**: Concatena os arquivos CSV em um único arquivo HDF5.
- **`_dell_tmp()`**: Remove o diretório temporário após o processamento.
- **`process_full_flow()`**: Executa todo o processo de download, extração, concatenação e limpeza.
- **`loc()`**: Localiza dados financeiros específicos de uma empresa e tipo de demonstração.

### Objetivo:

Este script é projetado para facilitar o acesso e processamento dos dados financeiros da CVM, permitindo que os usuários baixem, processem e armazenem essas informações de forma automatizada, além de consultar dados financeiros específicos com facilidade.