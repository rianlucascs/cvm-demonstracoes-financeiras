![cvm](https://juvenilalves.com.br/wp-content/uploads/2022/02/CVM.png)

# CVM Demonstrações Financeiras

Este projeto automatiza o download, extração e processamento de dados financeiros da Comissão de Valores Mobiliários (CVM). Além disso, possibilita a consulta aos dados financeiros de empresas específicas, visando facilitar a análise e o armazenamento eficiente das informações.

## Como usar

1. Instalação das bibliotecas
    ```bash
    python -m pip install -r https://raw.githubusercontent.com/rianlucascs/cvm-demonstracoes-financeiras/master/requirements.txt
    ```

2. Acesso aos dados
    ```python
    # Importando a biblioteca 'requests' para realizar requisições HTTP
    import requests
    from os import getcwd

    # URL do script Python da classe CVM hospedado no GitHub
    url = 'https://raw.githubusercontent.com/rianlucascs/cvm-demonstracoes-financeiras/master/Scripts/cvm.py'

    # Realizando a requisição HTTP para baixar o conteúdo do script
    # A URL aponta para o script Python hospedado no GitHub, e com o 'requests.get()', estamos baixando esse script.
    response = requests.get(url)

    # Usando o 'exec' para executar o código baixado. 
    # O comando 'exec(response.text)' executa o conteúdo do script que foi baixado. Isso torna a classe 'CVM' 
    # disponível para ser instanciada e utilizada no código abaixo.
    exec(response.text)

    # Definindo o 'path_project' com o diretório de trabalho atual do script.
    # O parâmetro 'path_project' é configurado com o diretório onde o script está sendo executado. 
    # 'getcwd()' retorna o diretório atual e é utilizado para armazenar os dados no local correto.
    cvm = CVM(path_project=getcwd())

    # Chamando o método 'process_full_flow', que realiza o download, extração, concatenação e limpeza dos dados.
    # A flag 'update=False' indica que não será feita uma nova execução, caso o processo já tenha sido realizado anteriormente.
    cvm.process_full_flow(update=False)

    # Exibindo os tipos de demonstrações financeiras disponíveis.
    # Após o processamento dos dados pela classe 'CVM', a variável 'nomes' contém os tipos de demonstrações financeiras processados.
    print(cvm.nomes)

    # Exemplo de como acessar uma tabela específica.
    # O método 'loc' é usado para buscar dados financeiros específicos de uma empresa, neste caso, 'VALE', 
    # e o tipo de demonstração 'BPA_con' (Balanço Patrimonial Consolidad), com base nos dados processados pela classe.
    table = cvm.loc('VALE', 'BPA_con')

    # Exibindo a tabela ou os dados relacionados à empresa 'VALE' e à demonstração 'BPA_con'.
    # A tabela de dados da empresa será exibida com os detalhes financeiros solicitados.
    print(table)

    ```

    Tabela
    |   | CNPJ_CIA              | DT_REFER | VERSAO | DENOM_CIA | CD_CVM | GRUPO_DFP                             | MOEDA | ESCALA_MOEDA | ORDEM_EXERC | DT_FIM_EXERC | CD_CONTA | DS_CONTA                | VL_CONTA          | ST_CONTA_FIXA |
    |---|-----------------------|----------|--------|-----------|--------|---------------------------------------|-------|--------------|-------------|--------------|----------|-------------------------|-------------------|---------------|
    | 86576 | 33.592.510/0001-54     | 2011-03-31 | 1      | VALE S.A. | 4170   | DF Consolidado - Balanço Patrimonial Ativo | REAL  | MIL          | PENÚLTIMO   | 2010-12-31   | 1        | Ativo Total             | 214662114.000000  | S             |
    | 86577 | 33.592.510/0001-54     | 2011-03-31 | 1      | VALE S.A. | 4170   | DF Consolidado - Balanço Patrimonial Ativo | REAL  | MIL          | ÚLTIMO      | 2011-03-31   | 1        | Ativo Total             | 217320211.000000  | S             |
    | 86578 | 33.592.510/0001-54     | 2011-03-31 | 1      | VALE S.A. | 4170   | DF Consolidado - Balanço Patrimonial Ativo | REAL  | MIL          | PENÚLTIMO   | 2010-12-31   | 1.01     | Ativo Circulante        | 54268731.000000   | S             |
    | 86579 | 33.592.510/0001-54     | 2011-03-31 | 1      | VALE S.A. | 4170   | DF Consolidado - Balanço Patrimonial Ativo | REAL  | MIL          | ÚLTIMO      | 2011-03-31   | 1.01     | Ativo Circulante        | 46568993.000000   | S             |
    | 86580 | 33.592.510/0001-54     | 2011-03-31 | 1      | VALE S.A. | 4170   | DF Consolidado - Balanço Patrimonial Ativo | REAL  | MIL          | PENÚLTIMO   | 2010-12-31   | 1.01.01  | Caixa e Equivalentes de Caixa | 13468958.000000  | S             |


## Sobre os dados


### 1. **Balanço Patrimonial Ativo (BPA)**
   - **O que é:** Apresenta a posição financeira de uma empresa, detalhando o que ela possui (Ativos) e o que deve (Passivos) em um determinado momento. 
   - **Componentes:**
     - **Ativo:** O que a empresa possui, incluindo caixa, contas a receber, estoques, investimentos, imobilizado, etc.
     - **Passivo:** O que a empresa deve, incluindo dívidas de curto e longo prazo, fornecedores, impostos a pagar, etc.
     - **Patrimônio Líquido:** A diferença entre o ativo e o passivo, que reflete o valor dos recursos próprios dos acionistas ou proprietários da empresa.

### 2. **Balanço Patrimonial Passivo (BPP)**
   - **O que é:** A parte do balanço patrimonial que detalha as obrigações da empresa (passivos) e a estrutura de financiamento da mesma (patrimônio líquido).
   - **Componentes:**
     - **Passivo Circulante:** Obrigações de curto prazo, geralmente com vencimento em até 12 meses.
     - **Passivo Não Circulante:** Obrigações de longo prazo, com vencimento superior a 12 meses.
     - **Patrimônio Líquido:** A parte do balanço que representa a participação dos acionistas após deduzir todas as obrigações.

### 3. **Demonstração de Fluxo de Caixa - Método Direto (DFC-MD)**
   - **O que é:** Relatório financeiro que detalha as entradas e saídas de caixa da empresa. No **método direto**, são apresentados os fluxos operacionais, de investimento e de financiamento diretamente.
   - **Componentes:**
     - **Atividades Operacionais:** Fluxos relacionados às operações principais da empresa, como recebimentos de vendas e pagamentos a fornecedores.
     - **Atividades de Investimento:** Fluxos relacionados à compra e venda de ativos de longo prazo, como imóveis e equipamentos.
     - **Atividades de Financiamento:** Fluxos relacionados a empréstimos, emissão de ações, pagamento de dividendos, etc.

### 4. **Demonstração de Fluxo de Caixa - Método Indireto (DFC-MI)**
   - **O que é:** Assim como a DFC-MD, essa demonstração também apresenta o fluxo de caixa da empresa, mas no **método indireto** começa com o lucro líquido e ajusta para as variações de caixa que não são capturadas pela contabilidade de competência (como depreciação, variações de capital de giro, etc).
   - **Componentes:**
     - **Lucro Líquido:** Ajustado para refletir as transações não monetárias.
     - **Ajustes de Itens não Monetários:** Como depreciação e amortização.
     - **Variação no Capital de Giro:** Como variação em contas a pagar, contas a receber, estoques, etc.

### 5. **Demonstração das Mutações do Patrimônio Líquido (DMPL)**
   - **O que é:** Apresenta as variações no patrimônio líquido da empresa durante o período, como aumento de capital, lucros ou prejuízos acumulados, dividendos pagos, ajustes de reavaliação, etc.
   - **Componentes:**
     - **Lucros ou Prejuízos Acumulados:** Como o lucro líquido do exercício impacta o patrimônio líquido.
     - **Ajustes de Reavaliação e Outros:** Inclui mudanças no valor de ativos e passivos, reavaliações de ativos, ajustes de câmbio, etc.

### 6. **Demonstração de Resultado Abrangente (DRA)**
   - **O que é:** Reflete todas as receitas, despesas e outras transações que afetam o patrimônio líquido da empresa, incluindo aquelas que não estão diretamente ligadas ao lucro líquido, como variações no valor de ativos financeiros e outros itens de ajuste.
   - **Componentes:**
     - **Lucro ou Prejuízo Líquido:** O resultado final das operações.
     - **Outros Resultados Abrangentes:** Como ganhos ou perdas de reavaliação de ativos e passivos financeiros, impactos de câmbio e reclassificação de itens.

### 7. **Demonstração de Resultado (DRE)**
   - **O que é:** A Demonstração de Resultado (ou Demonstração do Resultado do Exercício) mostra o desempenho da empresa durante um período, evidenciando as receitas, custos e despesas, além de calcular o lucro ou prejuízo do exercício.
   - **Componentes:**
     - **Receita Bruta:** A receita obtida com a venda de bens ou serviços.
     - **Custos das Vendas:** Os custos diretamente relacionados à produção ou aquisição de bens ou serviços.
     - **Lucro Bruto:** Receita Bruta menos os Custos das Vendas.
     - **Despesas Operacionais:** Como despesas de vendas, administrativas e financeiras.
     - **Lucro Líquido:** O lucro após a dedução de impostos e outras despesas.

### 8. **Demonstração de Valor Adicionado (DVA)**
   - **O que é:** Apresenta a riqueza criada pela empresa durante o período, destacando como essa riqueza foi distribuída entre empregados, governo, acionistas e a própria empresa.
   - **Componentes:**
     - **Valor Adicionado Bruto:** A diferença entre a receita líquida e o custo das mercadorias ou serviços vendidos.
     - **Distribuição de Valor Adicionado:** Como a riqueza gerada foi distribuída, incluindo salários, impostos, lucros e dividendos.

## Contato

Estou à disposição para esclarecer dúvidas ou fornecer mais informações. Você pode entrar em contato através das seguintes opções:

- **LinkedIn:** [Visite meu perfil no LinkedIn](www.linkedin.com/in/rian-lucas)
- **GitHub:** [Explore meu repositório no GitHub](https://github.com/rianlucascs)
- **Celular:** +55 61 96437-9500


Fico sempre aberto a colaborações e oportunidades de networking!