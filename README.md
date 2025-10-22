# Projeto de Predição de Score de Crédito e Inadimplência

Este projeto utiliza **regressão logística** para prever o **score de crédito** e a **inadimplência** de clientes. O modelo foi treinado com a base de dados *Default of Credit Card Clients*, fornecida pelo **UCI Machine Learning Repository**. Embora a base seja antiga e proveniente de um banco de Taiwan, os resultados podem ainda ser relevantes, dependendo do contexto, mas podem não refletir com precisão dados mais recentes ou específicos do Brasil.

## Arquivos do Projeto

- **relatorio.pdf**: Documento explicativo sobre a análise, incluindo identificação de problemas, métricas utilizadas, variáveis relevantes e a acurácia do modelo.
- **EDA.ipynb**: Jupyter Notebook com a exploração e análise inicial do dataset.
- **modelagem.ipynb**: Jupyter Notebook detalhando o processo completo de modelagem do modelo preditivo.
- **app.py**: Arquivo Python que cria uma interface gráfica, permitindo ao usuário preencher seus dados e receber o score e a probabilidade de inadimplência.

Todos os códigos estão devidamente documentados para facilitar a compreensão e permitir que qualquer pessoa entenda as etapas do processo.

---

## Requisitos

Antes de rodar o código ou executar o aplicativo, você precisa garantir que as bibliotecas necessárias estejam instaladas no seu ambiente. Para isso, siga os passos abaixo:

**No terminal (por exemplo, no VSCode), execute os seguintes comandos:**

1. **Criar um ambiente virtual**:
   
   ```bash
   python -m venv venv

2. **Ativar o ambiente virtual**

   ```bash
   .\venv\Scripts\activate

3. **Instalar bibliotecas necessárias**

   ```bash
   pip install pandas scikit-learn matplotlib seaborn statsmodels xlrd

## Rodando o programa

### Executar o aplicativo

Para abrir a interface gráfica que prevê o score e a chance de inadimplência, basta rodar o arquivo **app.py**

### Criando o Executável

O executável (.exe) gerado pelo PyInstaller para este projeto excede o limite de 100MB do GitHub, por isso não foi anexado a este repositório. No entanto, se você deseja gerar o executável em seu ambiente local, siga os passos abaixo:

1. **Instalar o PyInstaller:**

   ```bash
   pip install pyinstaller

2. **Criar o executável:**

   ```bash
   pyinstaller --onefile --windowed --add-data "modelos;modelos" --hidden-import sklearn app.py

3. **Localizar o Executável:**

   
