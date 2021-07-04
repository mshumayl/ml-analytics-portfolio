# %%
%%time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from collections import Counter
import imblearn

file = '../input/uci-semcom/uci-secom.csv'
data = pd.read_csv(file)

#Missing values heatmap
def plot_missing_values(dataframe):    
    sns.heatmap(dataframe.isnull(), yticklabels=False, cbar=False, cmap='magma')
    plt.title('Missing Values')
    plt.show()

#Remove columns with more than 50% missing values
def remove_null_columns(dataframe):
    threshold_null = len(dataframe) * 0.5
    dataframe_less_null = dataframe.dropna(thresh=threshold_null, axis=1)
    
    return dataframe_less_null

#Impute missing values with mean
def impute_missing_values(dataframe):
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(data.drop('Time', axis=1))
    imputed = imp.transform(data.drop('Time', axis=1))
    df = pd.DataFrame(imputed)
    
    df['Time'] = data['Time']
    df['Time'] = pd.to_datetime(df['Time'])
    
    return df

#Plot sensor active times
def plot_active_time():
    ax = data.plot(x='Time', y=0, figsize=(15,5), legend=False, style='.', alpha=0.1)
    for y in np.arange(562):
        
        data.plot(x='Time', y=y, legend=False, style='.', ax=ax, alpha=0.1)
        plt.ylabel('Value')

    plt.title('Active Time for All Sensors')
    plt.show()

#Feature-target split
def split_feature_target(dataframe):
    X = dataframe.drop(['Time', 562], axis=1)
    y = dataframe[562]
    
    return X, y

#SMOTE resampling to combat class imbalance
def SMOTE_resampling(inX, iny):
    oversample = imblearn.over_sampling.SMOTE()
    outX, outy = oversample.fit_resample(inX, iny)
    
    counter_before = Counter(iny)
    counter_after = Counter(outy)
    
    print('Before SMOTE resampling, the class ratio is:',counter_before)
    print('After SMOTE resampling, the class ratio is:',counter_after)
    
    return outX, outy

#Encode target to prepare for XGBoost model
def encode_target(y):
    encoder = LabelEncoder()
    encoder.fit(y)
    y_encoded = encoder.transform(y)
    
    return y_encoded

#Scale features
def scale_features(features):
    scaler = QuantileTransformer()
    scaled_features = pd.DataFrame(scaler.fit_transform(features))
    
    return scaled_features

#Create model
def create_XGB(X_train_scaled, y_train):
    XGB = XGBClassifier(use_label_encoder=False, tree_method='gpu_hist', eval_metric='auc', learning_rate=0.02, n_estimators=1000, objective='binary:logistic')
    XGB.fit(X_train_scaled, y_train)
    
    return XGB

#Evaluate model
def evaluate_model(model, X_test, y_test):
    #No skill prediction
    ns_probs = [0 for _ in range(len(y_test))]
  
    #Predict probabilities for the model
    model_probs = model.predict_proba(X_test)

    #Keep probabilities for the positive outcome only
    model_probs = model_probs[:, 1]

    #Calculate scores
    ns_auc = roc_auc_score(y_test, ns_probs)
    model_auc = roc_auc_score(y_test, model_probs)

    #Summarize scores
    print('No Skill: ROC AUC=%.3f' % (ns_auc))
    print('Model: ROC AUC=%.3f' % (model_auc))

    #Calculate ROC curves
    ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
    model_fpr, model_tpr, _ = roc_curve(y_test, model_probs)

    #Plot the ROC curve for the model and the noskill
    plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
    plt.plot(model_fpr, model_tpr, marker='.', label='Model')
    
    plt.show()
    
data = remove_null_columns(data)
data = impute_missing_values(data)
X, y = split_feature_target(data)
X, y = SMOTE_resampling(X, y)
y = encode_target(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
X_train_scaled = pd.DataFrame(scale_features(X_train))   
XGB = create_XGB(X_train_scaled, y_train)

folds = 3
param_comb = 20

skf = StratifiedKFold(n_splits=folds, shuffle=True)

params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 5, 7, 10],
        'learning_rate': [0.01, 0.02, 0.05]    
        }

random_search = RandomizedSearchCV(XGB, param_distributions=params, n_iter=param_comb, scoring='roc_auc', n_jobs=10, cv=skf.split(X_train_scaled, y_train), verbose=3)
random_search.fit(X_train_scaled, y_train)

evaluate_model(random_search, X_test, y_test)
# %%
