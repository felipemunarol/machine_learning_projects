from utils import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from pandas_profiling import ProfileReport
from typing import List
from dateutil.relativedelta import relativedelta

from fbprophet import Prophet

from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

import keras
from keras.models import Sequential
from keras.layers import Dense

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import shap

print("Starting")

print("Reading Data")
# Leitura dos dados
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
# ProfileReport(train)

print("Preprocessing")
train["datetime"] = pd.to_datetime(train.datetime)
test["datetime"] = pd.to_datetime(test.datetime)

# Index
train.set_index("datetime", inplace=True)
test.set_index("datetime", inplace=True)


cols_2lag = ["temperature", "var1", "windspeed"]
# Limite de lags 4 para melhor explicabilidade do modelo
lags = 4
cols_2ma = ["temperature", "var1", "windspeed"]
# Limite de lags 4 para melhor explicabilidade do modelo
mas = 4

# Features Temporais:
train = date_features(train)

# Lag features
train = shift_cols(train, cols_2lag, lags=lags)

# Ma features
train = ma_cols(train, cols_2ma, mas=mas)

# Fourier Features
# Implement

# Filter outliers
train  = remove_outliers(train)

# Transforma cdados categoricos. Isso ajuda no tratamento de alguns modelos e otimiza o processamento
for c in train.dtypes[train.dtypes == 'object'].index: 
    train[c] = train[c].astype('category')


print("Traning")
print("Baseline")

train_df = train.copy()

SHAP = False
FEATURE_SELECTION = True
APPLY_GRID = False
PLOT_PREDICTION = True
cat_cols =['var2']
PLOT_PREDICTION = True

label = "electricity_consumption"
forbiden = ["ID", "date"]

X = train_df.drop(columns=[label] + forbiden)
y = train_df[label]

X = train_df.drop(columns=[label] + forbiden)
y = train_df[label]


size = len(y)
y_predict = np.array([y.mean()]*size)
mean_absolute_percentage_error(y, y_predict)

if PLOT_PREDICTION:
    # plot_predict(X_valid, y_valid, predict, "LGBM", hist=True, structure_plot_cols=['hour', 'dom', 'dow', 'year'])
    plot_predict(X, y, y_predict, "Mean")


print("Prophet")

X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.20, shuffle=False, random_state=False)
# Testa valores proximos do default
grid = {
    # defalts to 100
    'n_estimators': [10, 20, 30, 40, 100, 200],
    # Taxa de aprendizado muito altas o modelo desce o gradiente muito rapido e pode perder o caminho otimo.
    # Taxas de aprendizado muito pequenas fazem o modelo ficar lento e ir a passos prquenos para o grandiente
    # Colocar em um valor ate o defaults to 0.1
    'learning_rate': [0.01, 0.02, 0.04, 0.08, 0.1],
    # large num_leaves helps improve accuracy but might lead to over-fitting
    'num_leaves': [100, 32, 20, 10],
#     'lambda_l1': 1,  
#     'lambda_l2': 1,
#     'verbose': 100,
#     'min_data_in_leaf': 100,
#     'early_stopping_rounds': [100, 200, 300], 
} 

params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'rmse',
    'verbose': -1,
    'learning_rate': 0.02,
    'n_estimators': 200,
    'num_leaves': 100,
}


if APPLY_GRID:
    print("Starting Grid")
    best_score, best_params = grid_search_tscv(LGBMRegressor(**params), X, y, grid, tscv=10)
    params.update(best_params)
    print(f"Best params {best_params}")
    print("Done")


model = LGBMRegressor(**params)
model.fit(X_train, y_train)
predict = model.predict(X_valid)
mean_absolute_percentage_error(y_valid, predict)

if FEATURE_SELECTION:
    print("start features selector")
    filter_selector = SelectFromModel(model, prefit=True).get_support()
    features = np.array(model.feature_name_)[filter_selector].tolist()
    X_train = X_train[features]
    X_valid = X_valid[features]
    print("Done")

model = LGBMRegressor(**params)
model.fit(X_train, y_train)
predict = model.predict(X_valid)
mean_absolute_percentage_error(y_valid, predict)

if SHAP:
    print("plotting shap")
    plot_shap(model, X_train)

if PLOT_PREDICTION:
    print("plotting predict")
    # plot_predict(X_valid, y_valid, predict, "LGBM", hist=True, structure_plot_cols=['hour', 'dom', 'dow', 'year'])
    plot_predict(X_valid, y_valid, predict, "LGBM")



print("Catboost")
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.20, shuffle=False, random_state=False)

# Testar valores proximos do default
grid = {'n_estimators': [10, 20, 30, 40, 100, 200, 500, 1000], # number of boosting iterations, defalts to 100
        'learning_rate': [0.01, 0.02, 0.04],
#          'num_leaves': [100, 32, 20, 10], # large num_leaves helps improve accuracy but might lead to over-fitting
#         'lambda_l1': 1,  
#         'lambda_l2': 1,
#         'verbose': 100,
#       'min_data_in_leaf': 100,
#         'early_stopping_rounds': [100, 200, 300], 
        } 

params = {
#     'boosting_type': 'Plain',
    'objective': 'MAPE', 'eval_metric': 'MAPE', 'cat_features':cat_cols, 'logging_level': 'Silent',
#   'learning_rate': 0.01, 'n_estimators': 1000
}


if APPLY_GRID:
    print("Starting Grid")
    best_score, best_params = grid_search_tscv(CatBoostRegressor(**params), X, y, grid, tscv=10)
    params.update(best_params)
    print(f"Best paramns {best_params}")
    print("Done")

    
model = CatBoostRegressor(**params)
model.fit(X_train, y_train)
predict = model.predict(X_valid)

mean_absolute_percentage_error(y_valid, predict)

if FEATURE_SELECTION:
    filter_selector = SelectFromModel(model, prefit=True).get_support()
    features = np.array(model.feature_names_)[filter_selector].tolist()
    X_train = X_train[features]
    X_valid = X_valid[features]
    cat_features = train_df.select_dtypes(include=['object']).columns.to_list()
    params.update({'cat_features': cat_features})


model = CatBoostRegressor(**params)
model.fit(X_train, y_train)
predict = model.predict(X_valid)
mean_absolute_percentage_error(y_valid, predict)

if SHAP:
    plot_shap(model, X_train)


if PLOT_PREDICTION:
    print("plotting predict")
    plot_predict(X_valid, y_valid, predict, name_model="Catboost")


print("ANN")

forbiden_ann = ["electricity_consumption", "ID", "date", "var2", "temperature_lag_1", "var1_lag_1", "windspeed_lag_1"]
forbiden_ann = list(set(forbiden_ann + forbiden))

X_ann = train_df.drop(columns=forbiden_ann)

columns_2keep = [c for c in X_ann.columns if ("ma" not in c)]
X_ann = X_ann[columns_2keep]
columns_2keep = [c for c in X_ann.columns if ("lag" not in c)]
X_ann = X_ann[columns_2keep]

X_train, X_valid, y_train, y_valid = train_test_split(X_ann, y, test_size=0.20, shuffle=False, random_state=False)

epochs = 100

X_train, X_valid, y_train = X_train.values, X_valid.values, y_train.values

# Standard Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_valid = sc.fit_transform(X_valid)

# Normalizing the target variables
y_train_scaller = (y_train - min(y_train))/ (max(y_train) - min(y_train))

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 10, kernel_initializer = 'uniform', activation = 'relu', input_dim = X_train.shape[1]))

# Adding the second hidden layer
classifier.add(Dense(units = 5, kernel_initializer = 'uniform', activation = 'relu'))

# # Adding the thirth hidden layer
# classifier.add(Dense(units = 3, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['mae'])

# Fitting the ANN to the training set
classifier.fit(X_train, y_train_scaller, batch_size = 10, epochs = epochs)

# Predicting the Test set results
y_pred = classifier.predict(X_valid)
y_pred = (y_pred * (max(y_train) - min(y_train))) + min(y_train)

predictions = [int(elem) for elem in y_pred]

# MAPE
mean_absolute_percentage_error(y_valid, predictions)

if PLOT_PREDICTION:
    plot_predict(X_valid, y_valid, predictions, name_model="ANN")