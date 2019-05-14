from gradientboost import GradientBoost
import pandas as pd
import pickle
from pymongo import MongoClient
import ast
import time

def _predict_db(json, model):
    df = pd.DataFrame([json])
    return model.predict_proba(df)[:,1]

def predict_one(json):
    """
    input:  json:json object
    output: dict with
    """
    with open('modelg2.p', 'rb') as f:
        model = pickle.load(f)

    df = pd.DataFrame([json])
    pred = _predict_db(json, model)[0]
    threat = ""
    if pred > .7:
        threat = 'High'
    elif pred > .005:
        threat = 'Medium'
    else:
        threat = 'Low'
    df['pred'] = pd.Series([pred])
    df['threat'] = pd.Series([threat])

    columns = ['name', 'org_name', 'event_created','pred','threat', 'object_id']
    d = df[columns].iloc[0].to_dict()
    d['pred'] = float(d['pred'].round(4))
    d['event_created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d['event_created']))
    d['object_id'] = int(d['object_id'])
    return d

def insert_one(json, address = 'localhost'):
    """
    input:
        json: json object
        address:string for MongoClient
    output: none

    inserts a version of the json object with prediction into the mongo db at the address
    database name = event_fraud
    table name = predictions
    """
    client = MongoClient(address, 27017)
    db = client['event_fraud']
    table = db['predictions']
    table.insert_one(predict_one(json))

def make_prediction_db(file, address = 'localhost'):

    df = pd.read_csv(file)
    data = pd.read_json('data/data.json')
    df.columns = data.columns
    df = df.drop('acct_type', axis = 1)
    df['ticket_types'] = df['ticket_types'].apply(ast.literal_eval)
    for col in df:
        if df[col].dtype == 'O':
            df[col] = df[col].fillna('')
        else:
            df[col] = df[col].fillna(0)
    for i, row in df.iterrows():
        print(i)
        insert_one(row.to_dict(), address)
