## Como usar

1. Instalação das bibliotecas
    ```bash
    python -m pip install -r https://raw.githubusercontent.com/rianlucascs/cvm-demonstracoes-financeiras/master/requirements.txt
    ```

2. Acesso aos dados
    ```python
    # Importando a biblioteca 'requests' para realizar requisições HTTP
    import requests

    # URL do script Python da classe CVM hospedado no GitHub
    url = 'https://raw.githubusercontent.com/rianlucascs/cvm-demonstracoes-financeiras/master/Scripts/cvm.py'

    # Realizando a requisição HTTP para baixar o conteúdo do script
    response = requests.get(url)

    # Usando o 'exec' para executar o código baixado. 
    exec(response.text)

    # Agora que o script foi carregado e a classe CVM está disponível, podemos criar uma instância da classe.
    cvm = CVM()

    # Chamando o método process_full_flow, que realiza o download, extração, concatenação e limpeza dos dados
    # A flag 'update=False' indica que não vamos forçar uma nova execução, caso o processo já tenha sido realizado.
    cvm.process_full_flow(update=False)

    # Exibindo os tipos de demonstrações financeiras disponíveis
    print(cvm.nomes)

    # Exemplo de como acessar uma tabela específica. A função 'loc' foi suposta para buscar os dados financeiros
    # relacionados à empresa 'VALE' e ao tipo de demonstração 'BPA_con'.
    table = cvm.loc('VALE', 'BPA_con')

    # Exibindo a tabela ou dados relacionados
    print(table)

    ```