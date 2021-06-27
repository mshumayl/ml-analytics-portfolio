#%% 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
# %%
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
# %%
X_train = train_df.drop('target', axis=1)
Y_train = train_df['target']

X_test = test_df
# %%
%%time

# Encode target
encoder = LabelEncoder()
encoder.fit(Y_train)
encoded_y = encoder.transform(Y_train)

# %%
model = XGBClassifier()
model.fit(X_train, Y_train)
# %%
y_pred = model.predict_proba(X_test)
# %%
preds = pd.DataFrame(y_pred).reset_index()

# %%
my_submission = pd.DataFrame({
    'id': preds['index']+200000,
    'Class_1': preds[0],
    'Class_2': preds[1],
    'Class_3': preds[2],
    'Class_4': preds[3],
    'Class_5': preds[4],
    'Class_6': preds[5],
    'Class_7': preds[6],
    'Class_8': preds[7],
    'Class_9': preds[8],
})
# %%
my_submission.to_csv('SKLearnXGB_TPS062021_Submission.csv', index=False)
# %%
