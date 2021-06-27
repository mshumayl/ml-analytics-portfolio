#%% 

from datetime import time
# mlp for multiclass classification
from numpy import argmax
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras import utils

#%%
# load the dataset
train_df = read_csv('train.csv')
X_test = read_csv('test.csv')

# split into input and output columns
train_df = train_df.drop('id', axis=1)
X, y = train_df.values[:, :-1], train_df.values[:, -1]
# ensure all data are floating point values
X = X.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3)

# determine the number of input features
n_features = X_train.shape[1]

#%%
%%time
model = Sequential()
model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(9, activation='softmax'))
model.add(Dropout(0.05))
# compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# fit the model
model.fit(X_train, y_train, epochs=150, batch_size=1000, verbose=2)

#%%
# evaluate the model
loss, acc = model.evaluate(X_val, y_val, verbose=0)
print('Test Accuracy: %.3f' % acc)

#%%
# make a prediction
X_test = X_test.astype('float32').drop('id', axis=1)

#%%
import pandas as pd
yhat = model.predict(X_test)

preds = pd.DataFrame(yhat).reset_index()

# %%
print('Neural Network Architecture')
utils.plot_model(
    model,
    to_file="model.png",
    show_shapes=True,
    show_dtype=True,
    show_layer_names=True,
    rankdir="LR",
    expand_nested=True,
    dpi=256,
)

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
my_submission.to_csv('MLPNN_TPS062021_Submission.csv', index=False)
# %%
