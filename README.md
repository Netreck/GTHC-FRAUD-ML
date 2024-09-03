# Projeto Dados - Greem Team Hacker Club (GTHC) - UFABC

Projeto desenvolvido para a frente de dados do GTHC, a ideia é utilizar um modelo de ML para detectar fraudes em transações bancárias.

## Futuras Modificações

Pretendo realizar as seguintes melhorias no projeto:
- **Organização do Código**: Refatorar o código para melhorar a estrutura e a legibilidade, uma vez que é a primeira vez que trabalho com algumas das tecnologias utilizadas.
- **Utilização do Modelo RandomForest**: De acordo com pesquisas, o modelo de Machine Learning RandomForest é mais preciso para análise de fraudes, e planejo implementá-lo no futuro.
- **Deploy do Projeto**: Publicar o projeto em um site, facilitando o acesso e utilização.
- **Migração para PostgreSQL**: Substituir o uso do arquivo CSV por PostgreSQL, com o qual pretendo me familiarizar melhor.
- **Salvar o Modelo em uma Pipeline do Sklearn**: Criar uma pipeline para melhorar o processamento do DataFrame durante o treinamento do modelo. Ainda não consegui criar uma pipeline corretamente, o que impactou o feature engineering do projeto.

## Principais Tecnologias
Python, Uvicorn, Sklearn, pandas,FastAPI...

Dataset Utilizado disponivel no Kaggle
## Funcionamento

![image](https://github.com/user-attachments/assets/92bcab40-fad3-40c3-a8d3-0e0777c55a7f)

![image](https://github.com/user-attachments/assets/9535ec11-b5d3-424b-81eb-80ddfe77ccbe)

      

## Como Utilizar

1. Clone o repositório:
   ```
   git clone <URL_do_repositório>
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Inicie o servidor FastAPI com o Uvicorn:
   ```
   uvicorn app.app:app
   ```

4. Acesse o endereço IP fornecido pelo Uvicorn no terminal.

5. Na interface, você pode copiar três exemplos de transações bancárias em string no modelo CSV(separados por vírgulas (dado1,dado2,dado3,...)).

6. Ao enviar os dados, a API processará as informações e retornará um score entre 0 e 1000. Quanto maior o score, maior a probabilidade de a transação ser fraudulenta.

## Modelagem e Predição
Colunas do treinamento: Index(['Hour', 'amt', 'amt_city_pop_ratio', 'amt_distance_ratio',
       'avg_amt_month', 'city_pop', 'day_of_week', 'distance', 'gender_F',
       'gender_M', 'idade', 'is_weekend', 'month', 'period_of_day_Madrugada',
       'period_of_day_Manhã', 'period_of_day_Noite', 'period_of_day_Tarde',
       'total_amt_month', 'trans_count_month', 'year'],
      dtype='object')

      
Atualmente, o modelo utilizado é o **DecisionTree**.
