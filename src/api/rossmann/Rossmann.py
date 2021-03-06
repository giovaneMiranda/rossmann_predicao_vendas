import pickle 
import inflection
import pandas as pd 
import math
import datetime
import numpy as np

class Rossmann(object):
    def __init__(self):
        self.home_path = '/home/giovane/pythonProject/predicao_vendas/'
     
        self.store_type_encoding = pickle.load( open(self.home_path + 'parameter/store_type_encoding.pkl', 'rb'))
        self.promo2_time_week_scaler = pickle.load( open(self.home_path + 'parameter/promo2_time_week_scaler.pkl', 'rb'))
        self.promo2_since_year_scaler = pickle.load( open(self.home_path + 'parameter/promo2_since_year_scaler.pkl', 'rb'))
        self.competition_distance_scaler = pickle.load( open(self.home_path + 'parameter/competition_distance_scaler.pkl', 'rb'))
        self.year_scaler = pickle.load( open(self.home_path + 'parameter/year_scaler.pkl', 'rb'))
        

    def data_cleaning(self, df2):
        ## 1. Renomea colunas
        cols_old = df2.columns
        snake_case = lambda x : inflection.underscore(x)
        cols_new = list(map(snake_case, cols_old))
        df2.columns = cols_new
        
        # alterando tipo do atributo
        df2['date'] = pd.to_datetime(df2['date'], format='%Y-%m-%d')
        
        ## 2. Preencher dados faltantes, NA
        # competition_distance
        df2['competition_distance'] = df2['competition_distance'].apply(lambda x : 200000.0 if math.isnan(x) 
                                                                        else x )

        # competition_open_since_month
        df2['competition_open_since_month'] = df2.apply(lambda x : x['date'].month 
                                                        if math.isnan(x['competition_open_since_month']) 
                                                                        else x['competition_open_since_month'], axis=1 )

        # competition_open_since_year
        df2['competition_open_since_year'] = df2.apply(lambda x : x['date'].year 
                                                        if math.isnan(x['competition_open_since_year']) 
                                                                        else x['competition_open_since_year'], axis=1 )
        # promo2_since_week
        df2['promo2_since_week'].fillna(0, inplace=True)

        # promo2_since_year
        df2['promo2_since_year'].fillna(0, inplace=True)

        # promo_interval
        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct'
                     , 11: 'Nov', 12: 'Dec'}

        df2['promo_interval'].fillna(0, inplace=True)
        df2['month_map'] = df2['date'].dt.month.map(month_map)

        df2['is_promo2'] = df2[['promo_interval', 'month_map']].apply(lambda x : 0 if x['promo_interval'] == 0 else
                                                                      1 if x['month_map'] in x['promo_interval'].split(',')
                                                                      else 0, axis=1)
        
        ## 3. Altera Data type 
        # alterando o tipo dos catributos 'promo2_since_week', 'promo2_since_year' para int 
        df2['promo2_since_week'] = df2['promo2_since_week'].astype(int)
        df2['promo2_since_year'] = df2['promo2_since_year'].astype(int)

        # alterando o tipo dos catributos 'competition_open_since_month', 'competition_open_since_year' para int 
        df2['competition_open_since_month'] = df2['competition_open_since_month'].astype(int)
        df2['competition_open_since_year'] = df2['competition_open_since_year'].astype(int)
        
        return df2
    
    
    def feature_engineering(self, df3):
        # criacao de features com base nas ja existentes

        #year
        df3['year'] = df3['date'].dt.year

        #month
        df3['month'] = df3['date'].dt.month

        #day
        df3['day'] = df3['date'].dt.day

        #week of year
        df3['week_of_year'] = df3['date'].dt.weekofyear

        #year week
        df3['year_week'] = df3['date'].dt.strftime('%Y-%W')


        #promo Since
        df3['promo2_since'] = df3['promo2_since_year'].astype(str) + '-' + df3['promo2_since_week'].astype(str)
        df3['promo2_since'] = df3['promo2_since'].apply(lambda x : 0 if x == '0-0' else datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7))
        df3['promo2_time_week'] = df3.apply(lambda x: 0 if x['promo2_since'] == 0 else ((x['date']-x['promo2_since'])/7).days, axis=1).astype(int)

        #assortiment
        df3['assortment'] = df3['assortment'].apply(lambda x : 'basic' if  x=='a'  else 'extra' if x=='b' else 'extended')

        #state holiday
        df3['state_holiday'] = df3['state_holiday'].apply(lambda x : 'public holiday' if  x=='a' else 'easter holiday' if x=='b' 
                                                          else 'christmas' if x=='c' else 'regular day')
        # Filtragem por linha
        df3 = df3[df3['open']!=0] 

        # Filtragem por coluna
        cols_drop = ['open', 'promo_interval', 'month_map']
        df3 = df3.drop(cols_drop, axis=1)
        

        return df3
    
    
    def data_preparation(self, df6):
        # 1. Rescalonamento de variaveis
        # competition_distance
        df6['competition_distance'] = self.competition_distance_scaler.fit_transform(df6[['competition_distance']].values)
        
        # year
        df6['year'] = self.year_scaler.fit_transform(df6[['year']].values)
        
        # promo2_time_week
        df6['promo2_time_week'] = self.promo2_time_week_scaler.fit_transform(df6[['promo2_time_week']].values)
        

        # promo2_since_year
        df6['promo2_since_year'] = self.promo2_since_year_scaler.fit_transform(df6[['promo2_since_year']].values)
        
        
        # 2. Encoding de variaveis categoricas
        # state_holiday 
        df6 = pd.get_dummies(df6, prefix= ['state_holiday'], columns=['state_holiday'])

        # store_type 
        df6['store_type'] = self.store_type_encoding.fit_transform(df6['store_type'])
        
        # assortment
        assortment_dict = {'basic' : 1, 'extra' : 2 , 'extended' : 3}
        df6['assortment'] = df6['assortment'].map(assortment_dict)
        
        
        # 3. Transformacao de natureza
        # month
        df6['month_sin'] = df6['month'].apply(lambda x: np.sin(x * (2. * np.pi/12)))
        df6['month_cos'] = df6['month'].apply(lambda x: np.cos(x * (2. * np.pi/12)))

        # day
        df6['day_sin'] = df6['day'].apply(lambda x: np.sin(x * (2. * np.pi/30)))
        df6['day_cos'] = df6['day'].apply(lambda x: np.cos(x * (2. * np.pi/30)))

        # week_of_year
        df6['week_of_year_sin'] = df6['week_of_year'].apply(lambda x: np.sin(x * (2. * np.pi/52)))
        df6['week_of_year_cos'] = df6['week_of_year'].apply(lambda x: np.cos(x * (2. * np.pi/52)))

        # day_of_week
        df6['day_of_week_sin'] = df6['day_of_week'].apply(lambda x: np.sin(x * (2. * np.pi/7)))
        df6['day_of_week_cos'] = df6['day_of_week'].apply(lambda x: np.cos(x * (2. * np.pi/7)))

        # competition_open_since_month
        df6['competition_open_since_month_sin'] = df6['competition_open_since_month'].apply(lambda x: np.sin(x * (2. * np.pi/12)))
        df6['competition_open_since_month_cos'] = df6['competition_open_since_month'].apply(lambda x: np.cos(x * (2. * np.pi/12)))

        # promo2_since_week
        df6['promo2_since_week_sin'] = df6['promo2_since_week'].apply(lambda x: np.sin(x * (2. * np.pi/52)))
        df6['promo2_since_week_cos'] = df6['promo2_since_week'].apply(lambda x: np.cos(x * (2. * np.pi/52)))
        
        cols_selected = ['store','promo', 'store_type', 'assortment', 'competition_distance', 'competition_open_since_year', 'promo2', 
                                'promo2_since_year', 'promo2_time_week', 'month_cos',  'month_sin', 'day_sin', 'day_cos', 'week_of_year_cos',
                                'week_of_year_sin', 'day_of_week_sin', 'day_of_week_cos', 'competition_open_since_month']
        

        return df6[cols_selected]
    
    def get_prediction(self, test_data, original_data, model):
        prediction =  model.predict(test_data)
        
        # juntando predicao com os dados originais
        original_data['prediction'] = np.expm1(prediction)
        
        return original_data.to_json(orient = 'records', date_format = 'iso')