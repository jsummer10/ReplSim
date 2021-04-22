"""
Project     : Replacement Policy Simulation
File name   : ANN.py
Authors     : Jake Summerville, Henry Lee,
              Martin Lopez, Fausto Sanchez
Creation    : 04/19/21
Description : This file contains the development of a neural net
              the Neural Net is a recurrent neural net with supervised learning
              called long short-term memory learn sequences
"""

import pandas as pd
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import concat
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from sklearn.preprocessing import MinMaxScaler
from keras.optimizers import SGD
import math
from sklearn.metrics import mean_squared_error

os.chdir("../output/")


# ----------------------------------------------------------------------
#     import the cache data replacement information
#     convert hexadecimal into int for LSTM friendly processing
# ----------------------------------------------------------------------


def ConvertData():
    # -----------------------------------------------------------------
    #     converts replacement policy results into int for processing in
    #     neural net
    # ------------------------------------------------------------------

    df = pd.read_excel('replacement_policy_data.xlsx', index_col=None, engine='openpyxl', header=0)
    df['cache_addr'] = df['cache_addr'].apply(lambda x: int(x, 16))
    df.to_csv('data_int_replacement.csv', index=False)

    # -----------------------------------------------------------------
    # plot to help us visualize the data
    # this should plot our predicted replacement policy over time
    # -----------------------------------------------------------------


def Plot_Predictions(test, predicted):
    plt.plot(test, color='red', label='Real Policy Replacement')
    plt.plot(predicted, color='blue', label='Predicted Replacement Policy')
    plt.title('Replacement Policy Prediction')
    plt.xlabel('Hits')
    plt.ylabel('Replacement Policy Prediction')
    plt.legend()
    plt.show()

    # -----------------------------------------------------------------
    #     Calculate the Root Mean Square Error
    # -----------------------------------------------------------------


def Return_RMSE(test, predicted):
    rmse = math.sqrt(mean_squared_error(test, predicted))
    print("The root mean squared error is {}.".format(rmse))


def Train_Replacement_Policy():
    dataset = pd.read_csv("data_int_replacement.csv", index_col='policy')
    dataset.head()
    # -------------------------------------------------------------------
    #      Checking for missing values by checking the index rows of
    #      the training set and the test set. We are looking at testing and training
    #      what we should move into L1 Cache
    # -------------------------------------------------------------------

    training_set = dataset[:'class'].iloc[:1].values
    print(training_set)
    test_set = dataset['class':].iloc[:1].values
    print(test_set)

    # -------------------------------------------------------------------
    #     We chose to train on our Hit attribute under class and then test
    #     on our miss rates. Without any machine learning we see that
    #     our cache replacement policy is < 50% and thus we believe we can test
    #     our data set based on these two classes
    #     p = Hit rates
    #     (1-p) = miss rates
    # -------------------------------------------------------------------

    dataset["class"].plot(figsize=(16, 4), legend=True)
    plt.legend(['Training set Hits', 'Test set Misses'])
    plt.title('L1 Smart Cache')
    plt.show()
    # --------------------------------------------------------------------
    #      scale our training set
    # --------------------------------------------------------------------

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # --------------------------------------------------------------------
    #     Long Short-Term Memory stores long term memory state
    #     Need to create data structure for each element of the training set
    #     we have a total of 10,002 values within our data set (could potentially be more)
    #     we choose 100 timesteps or 100 previous training sets
    # --------------------------------------------------------------------

    X_train = []
    y_train = []
    for i in range(100, 10002):
        X_train.append(training_set_scaled[i - 100:i, 0])
        y_train.append(training_set_scaled[i, 0])
        X_train, y_train = np.array(X_train), np.array(y_train)

    # --------------------------------------------------------------------
    #     Long Short-Term Memory (LSTM) architecture
    #     we have four LSTM layers
    #     we have one output layer
    # --------------------------------------------------------------------

    regressor = Sequential()
    # First LSTM layer with Dropout regularisation
    # regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))
    # Second LSTM layer
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))
    # Third LSTM layer
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))
    # Fourth LSTM layer
    regressor.add(LSTM(units=50))
    regressor.add(Dropout(0.2))
    # The output layer
    regressor.add(Dense(units=1))

    # --------------------------------------------------------------------
    #     Long Short-Term Memory (LSTM) architecture is a Recurrent Neural Net (RNN)
    # --------------------------------------------------------------------

    # Compiling the RNN
    regressor.compile(optimizer='rmsprop', loss='mean_squared_error')
    # Fitting to the training set
    regressor.fit(X_train, y_train, epochs=50, batch_size=32)

    # --------------------------------------------------------------------
    #     Get test set ready as the training set
    #     we get the first 100 entries of the test set have 100 previous values
    # --------------------------------------------------------------------

    dataset_total = pd.concat((dataset["class"][:'Hit'], dataset["class"]['Miss':]), axis=0)
    inputs = dataset_total[len(dataset_total) - len(test_set) - 100:].values
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)
    # Preparing X_test and predicting the prices
    X_test = []
    for i in range(100, 500):
        X_test.append(inputs[i - 100:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_cache_result = regressor.predict(X_test)
        predicted_cache_result = sc.inverse_transform(predicted_cache_result)
    # Visualizing the results for LSTM
    Plot_Predictions(test_set, predicted_cache_result)
    # evaluate model
    Return_RMSE(test_set, predicted_cache_result)


def main():
    ConvertData()

    # Train_Replacement_Policy()


if __name__ == '__main__':
    main()
