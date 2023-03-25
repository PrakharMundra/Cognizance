import uvicorn
from fastapi import FastAPI
from P2Pdeliquency import data_encoding
from inputs import input
import numpy as np
import pickle
import pandas as pd
app=FastAPI()
pickle_in=open("model.pickle","rb")
regressor=pickle.load(pickle_in)

@app.get('/')
def index():
    return{'message':'Hello'}
@app.get('/Welcome')
def get_name(name:str):
    return{'Welcome to P2P Delinq Prediction': f'{name}'}

@app.post('/predict')
def predict_delinq(data:input):
    data=data.dict()
    data_encoding(data)
    emp_title=data['emp_title']
    emp_length=data['emp_length']
    homeownership=data['homeownership']
    annual_income=data['annual_income']
    debt_to_income=data['debt_to_income']
    delinq_2y=data['delinq_2y']
    earliest_credit_line=data['earliest_credit_line']
    total_credit_lines=data['total_credit_lines']
    open_credit_lines=data['open_credit_lines']
    total_debit_limit=data['total_debit_limit']
    loan_purpose=data['loan_purpose']
    loan_amount=data['loan_amount']
    balance=data['balance']
    pred=regressor.predict([[emp_title,emp_length,homeownership,annual_income,debt_to_income,delinq_2y,earliest_credit_line,total_credit_lines,open_credit_lines,total_debit_limit,loan_purpose,loan_amount,balance]])
    return{'Delinq %':pred}
if __name__=='__main__':
    uvicorn.run(app,host='127.0.0.2',port=8000)
