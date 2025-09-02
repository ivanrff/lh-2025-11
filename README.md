# Modelo Preditivo de Nota IMDB

O arquivo ```Relatório Jupyter.ipynb``` contém todas as entregas de informação solicitadas. Ele utiliza dois datasets diferentes do dataset disponibilizado. Ainda que não seja boa prática, pra facilitar, eu subi os dois datasets neste repositório.

Datasets necessários para rodar o relatório (disponíveis neste repositório):
1. ```data/desafio_indicium_imdb_final.csv```: Esse arquivo é o csv disponibilizado, porém com alguns valores faltantes preenchidos com dados de APIs. Para criar este dataset a partir do dataset original, deve-se rodar o arquivo ```manipulate_csv.py```, explicado abaixo.
2. ```data/US_inflation_from_macrotrends.csv```: Dataset de dados de inflação nos Estados Unidos. Disponível em: https://www.macrotrends.net/2497/historical-inflation-rate-by-year



> [!IMPORTANT]
> Na primeira célula do relatório há um parte onde é necessário baixar recursos do nltk:

```
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```
Esta parte só precisa ser executada uma vez.

## Outros arquivos

- ```manipulate_csv.py```: Neste arquivo utilizei duas APIs diferentes, e ele supõe a existência de um arquivo ```API_KEY.py``` com as duas chaves de API. ```API_KEY template.py``` mostra como esse arquivo deve ser.
<br>
    - ```api_connections.py```: Contêm funções auxiliares de ```manipulate_csv.py```.
<br>
- ```modelling_utils.py``` e ```overview_utils.py```: Contêm funções auxiliares que decidi mover para fora do Relatório para reduzir poluição visual.
<br>
- ```model.pkl```: é o modelo final treinado.

## Testar a predição

Para testar a predição basta rodar a última seção do Relatório, "Carregar o modelo e prever The Shawshank Redemption". Essa seção foi feita para atuar de forma standalone do resto do código do relatório.
