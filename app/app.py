from fastapi import FastAPI
import pandas as pd 
import pickle
from pydantic import BaseModel
import pickle

import sys
import os
from pydantic import BaseModel




###############
import nbformat
# Função para importar uma célula de código do notebook
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
import pandas as pd
from geopy.distance import geodesic
import joblib
from io import StringIO
import numpy as np
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Request

templates = Jinja2Templates(directory=os.path.join("app","templates"))

###############


app=FastAPI()

class ClasseURL(BaseModel):
    url: str

class ClasseScore(BaseModel):
    score:float



file_path = os.path.join('models', 'model_primeiro.pkl')

with open(file_path, 'rb') as file:
    model = pickle.load(file)
 
 ##############################################

ClasseURL 
{
    'url',''
}

def predict(classe_url):  
# Usando StringIO para simular um arquivo

    colunas = [
    "Unnamed: 0",
    "trans_date_trans_time",
    "cc_num",
    "merchant",
    "category",
    "amt",
    "first",
    "last",
    "gender",
    "street",
    "city",
    "state",
    "zip",
    "lat",
    "long",
    "city_pop",
    "job",
    "dob",
    "trans_num",
    "unix_time",
    "merch_lat",
    "merch_long"
]
    
    df = pd.read_csv(StringIO(classe_url),header=None,names=colunas)
    df = df.dropna()
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['dob'] = pd.to_datetime(df['dob'])
    df['Hour'] = df['trans_date_trans_time'].dt.hour
    df['month'] = df['trans_date_trans_time'].dt.month
    df['year']= df['trans_date_trans_time'].dt.year
    df['day_of_week']= df['trans_date_trans_time'].dt.day_of_week
    df['is_weekend']= df['trans_date_trans_time'].dt.day_of_week >= 5 
    df['idade']= df['trans_date_trans_time'].dt.year - df['dob'].dt.year
    def distance(row):
        return geodesic((row['lat'],row['long']),(row['merch_lat'],row['merch_long'])).km

    df['distance']= df.apply(distance, axis=1)
    df.drop(columns=['Unnamed: 0'], inplace=True)
    def get_period_of_day(hour):
        if 6 <= hour < 12:
            return 'Manhã'
        elif 12 <= hour < 18:
            return 'Tarde'
        elif 18 <= hour < 24:
            return 'Noite'
        else:
            return 'Madrugada'

    df['period_of_day'] = df['Hour'].apply(get_period_of_day)
    df['month'] = df['trans_date_trans_time'].dt.month
    df['year'] = df['trans_date_trans_time'].dt.year
    df['trans_count_month'] = df.groupby(['cc_num', 'year', 'month'])['trans_num'].transform('count')
    df['total_amt_month'] = df.groupby(['cc_num', 'year', 'month'])['amt'].transform('sum')
    df['avg_amt_month'] = df['total_amt_month'] / df['trans_count_month']
    df['avg_amt_month'] = df['total_amt_month'] / df['trans_count_month']
    df['amt_city_pop_ratio'] = df['amt'] / df['city_pop']
    df['amt_distance_ratio'] = df['amt'] / df['distance']
    df.drop(columns=['merchant','category','street','city','state','job'], inplace=True)
    df.drop(columns=['cc_num','merch_long','merch_lat','long','lat','dob','trans_date_trans_time','last','first','zip','trans_num','unix_time'], inplace=True)
    columns_to_dummify = ['gender','period_of_day']
    dummies = pd.get_dummies(df[columns_to_dummify])
    df = pd.concat([df.drop(columns_to_dummify, axis=1), dummies], axis=1)
    colunas_desejadas = [
    'gender_F', 
    'gender_M',               
    'period_of_day_Madrugada',   
    'period_of_day_Manhã',       
    'period_of_day_Noite',       
    'period_of_day_Tarde'
]

# Adicione colunas ausentes com valor 0
    for coluna in colunas_desejadas:
        if coluna not in df.columns:
            df[coluna] = 0
    df = df.sort_index(axis=1)
    score= np.round(model.predict_proba(df)[:,1][0]*1000,0)
    return score

    


@app.post("/e_fraude")
def get_prediction(classe_url : ClasseURL):
    score = predict(classe_url.url)
    return {"Score":score}
    

@app.get("/test")
def home():
    return {"hello world"}

import os

@app.get("/")
def get_home(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request})


@app.post("/")
def post_home(request : Request, url : str = Form(...)):
    payload = ClasseURL(url=url)
    score = predict(payload.url)

    return templates.TemplateResponse("index_scored.html", {"request" : request, "url" : "-", "score" : score})
