#import necessary libraries and utilities
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error


#def read_data(url = 'https://github.com/amaysood/Cybersprint/raw/main/loans_clean_schema.csv'):
    #data=pd.read_csv(url)
    #return data

#Fucntion that fetches Dataframe from required csv
def read_data():
    data=pd.read_csv('loans_clean_schema.csv')
    return data

#removing missing values from the dataset
def data_clean(df):
    df.dropna(axis = 0, inplace=True)
    return df
    
#defining fucntion for onehotencode to use later
def onehot_encode(df, column, prefix):
    df = df.copy()
    dummies = pd.get_dummies(df[column], prefix = prefix)
    df = pd.concat([df, dummies], axis = 1)
    df = df.drop(column, axis = 1)
    return df
    
#encoding the categorical data in the dataset to numerical
def data_encoding(data): 
    
    # Converting type of columns to category
    data['emp_title']=data['emp_title'].astype('category')
    
    
    #Assigning numerical values and storing it in another columns
    data['emp_title']=data['emp_title'].cat.codes
    
    #Onehot encoding
    df = onehot_encode(data, 'homeownership', prefix = "ho")
    df = onehot_encode(df, 'loan_purpose', 'lp')

    return df
    
#Scaling the data 
def data_normalization(data):
    #Splitting the data into dependant and independant variables
    y=data['account_never_delinq_percent'].copy()
    X=data.drop('account_never_delinq_percent',axis=1).copy()
    #Scaling
    scaling=StandardScaler()
    X=pd.DataFrame(scaling.fit_transform(X),columns=X.columns)
    #carrying out PCA to reduce dimensionality 
    pca = PCA(n_components=26)
    X = pca.fit_transform(X)
    return X,y


#Preprocessing inputs to train model
def preprocessing_inputs(data):
    df=read_data()
    data=data_clean(df)
    data1=data_encoding(data)
    X,y=data_normalization(data1)
    return X,y

#training the model
def train(data):
    #preprocess inputs
    X,y=preprocessing_inputs(data)
    #split the given dataset into train and test set
    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.9,random_state=42)
    #using Ridge regression with cross validation
    model=Ridge()
    #Adding a Polynomial degree to inputs to eliminate problems with linearity
    poly = PolynomialFeatures(degree=2)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    #Carrying out cross-validation for hyperparameter optimization in Ridge Regression 
    param_grid = {'alpha': np.logspace(-3, 3, 10)}
    grid_search = GridSearchCV(model, param_grid, cv=5)
    grid_search.fit(X_train_poly,y_train)
    #print the best alpha and score
    print('Best alpha:', grid_search.best_params_)
    print('Best score:', grid_search.best_score_)
    #Train Ridge model with best value of alpha
    best_ridge = grid_search.best_estimator_
    best_ridge.fit(X_train_poly, y_train)
    # save the trained model as a pickle file
    with open('model.pickle', 'wb') as f:
        pickle.dump(best_ridge, f)
    return X_test_poly,best_ridge,y_test


#carrying out predictions
def predict(X_test_poly,model,y_test):
    y_pred=model.predict(X_test_poly)
    y_pred=y_pred.clip(None,100)
    #scoring metrics
    R2_score=( r2_score(y_test, y_pred))
    mae_score=( mean_absolute_error(y_test, y_pred))
    mse_score=( mean_squared_error(y_test, y_pred))
    return y_pred,R2_score,mae_score,mse_score

if __name__ == '__main__':
    data=read_data()
    X_test_poly,model,y_test=train(data)
    y_pred=predict(X_test_poly,model,y_test)
    







