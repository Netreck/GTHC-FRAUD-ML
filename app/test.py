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

# Transformador personalizado
class CustomTransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        
        X['Hour'] = X['trans_date_trans_time'].dt.hour
        X['month'] = X['trans_date_trans_time'].dt.month
        X['year']= X['trans_date_trans_time'].dt.year
        X['day_of_week']= X['trans_date_trans_time'].dt.day_of_week
        X['is_weekend']= X['trans_date_trans_time'].dt.day_of_week >= 5 
        X['idade']= X['trans_date_trans_time'].dt.year - X['dob'].dt.year

        def distance(row):
            return geodesic((row['lat'], row['long']), (row['merch_lat'], row['merch_long'])).km

        X['distance'] = X.apply(distance, axis=1)

        X.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'], inplace=True, errors='ignore')

        def get_period_of_day(hour):
            if 6 <= hour < 12:
                return 'Manhã'
            elif 12 <= hour < 18:
                return 'Tarde'
            elif 18 <= hour < 24:
                return 'Noite'
            else:
                return 'Madrugada'

        X['period_of_day'] = X['Hour'].apply(get_period_of_day)

        X['trans_count_month'] = X.groupby(['cc_num', 'year', 'month'])['trans_num'].transform('count')
        X['total_amt_month'] = X.groupby(['cc_num', 'year', 'month'])['amt'].transform('sum')
        X['avg_amt_month'] = X['total_amt_month'] / X['trans_count_month']
        X['amt_city_pop_ratio'] = X['amt'] / X['city_pop']
        X['amt_distance_ratio'] = X['amt'] / X['distance']
        X=X.fillna('False')
        X.drop(columns=['merch_long', 'merch_lat', 'long', 'lat', 'dob', 'trans_date_trans_time', 'last', 'first', 'zip', 'trans_num', 'unix_time'], inplace=True, errors='ignore')

        return X