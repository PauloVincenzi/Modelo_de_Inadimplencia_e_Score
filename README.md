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

1. **Criar um ambiente virtual**:

   No terminal (por exemplo, no VSCode), execute o seguinte comando para criar um ambiente virtual:

   ```bash
   python -m venv venv


1)
  python -m venv venv

2)
No windowns:
  .\venv\Scripts\activate
No Linux/macOS:
  source venv/bin/activate

3)
  pip install pandas scikit-learn matplotlib seaborn statsmodels xlrd

# Rodar o programa

Para abrir o aplicativo que prediz o Score e chance de inadimplência basta executar o arquivo 'app.py'

O executável (.exe) desse arquivo excede o tamanho (100 mB) permitido pelo GitHub e por isso não foi anexado neste repositório, porém, caso queira criar um executável, siga os passos abaixo:

No terminal:

1)
  pip install pyinstaller

2)
  pyinstaller --onefile --windowed --add-data "modelos;modelos" --hidden-import sklearn app.py

3)
O executável 'app.exe' foi criado na pasta build ('Modelo_de_Inadimplencia_e_Score\build\app.exe')
Transfira o executável para a pasta raiz ('Modelo_de_Inadimplencia_e_Score')

4)
Opcional:
Se quiser pode excluir as pastas e arquivos temporários gerados: build, dist e app.spec
Se quiser renomei o executável 'app.exe' para 'Calculadora_de_Score.exe'
