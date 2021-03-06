from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import pickle 
import pandas as pd 

# carregando modelo
model = pickle.load(open ('/home/giovane/pythonProject/predicao_vendas/model/model_rossmann.pkl', 'rb'))

app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predicr():
    test_json  = request.get_json()
    
    # Valida se a dados na requisicao 
    if test_json:
        #unico json
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
            
        #multiplos json
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
    
    else:
        return Response( '{}', status=200, mimetype ='application/json') 
    
    # Instasiando classe Rossmann
    pipeline = Rossmann()
    
    # limpeza dos dados
    df1 = pipeline.data_cleaning(test_raw)
    
    # feature engineering e filtragem 
    df2 = pipeline.feature_engineering(df1)
    
    # preparacao dos dados, modelagem 
    df3 = pipeline.data_preparation(df2)
    
    # prediction
    df_response = pipeline.get_prediction(df3,test_raw, model)
    
    return df_response
    
if __name__ == '__main__':
    app.run('0.0.0.0')