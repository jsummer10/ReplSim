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
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import mean_squared_error

os.chdir("../mem/")


def Plot_Predictions(test, predicted):
    plt.plot(test, color='red', label='Real Policy Replacement')
    plt.plot(predicted, color='blue', label='Predicted Replacement Policy')
    plt.title('Replacement Policy Prediction')
    plt.xlabel('cache_addr')  # want to predict patterns of memory hits
    plt.ylabel('Replacement Policy Prediction')
    plt.legend()
    plt.show()


# -----------------------------------------------------------------
# Calculate the Root Mean Square Error
# -----------------------------------------------------------------
def Return_RMSE(test, predicted):
    rmse = math.sqrt(mean_squared_error(test, predicted))
    print("The root mean squared error is {}.".format(rmse))


def Train_Replacement_Policy():
    # data set column [0] = address
    # column[1] = index + tag
    dataset = pd.read_csv("gen_mem.csv", header=None)
    df = pd.DataFrame(dataset)
    # print("data set:")
    # print(df.head())
    # -------------------------------------------------------------------
    # Checking for recurring cache addresses to train on to enable replacement policy
    # the training set and the test set. We are looking at testing and training
    # what we can predict the cache addresses and forecast to optimize our cache
    # -------------------------------------------------------------------

    # getting the index + tag
    training_set = df.values
    # print("Training Set:")
    # print(training_set)
    test_set = df.values
    # print("Test Set:)")
    # print(test_set)

    # -------------------------------------------------------------------
    # plot sequence for prediction
    # plot demonstrates predictability and sequence in index + tag
    # -------------------------------------------------------------------
    df[1][:300].plot(figsize=(16, 4), legend=True)
    plt.legend(['Test set Index + Tag'])
    plt.title('L1 Smart Cache')
    # plt.show()

    # # --------------------------------------------------------------------
    # scale our training set from zero to 1 for training set
    # scaled training set will be used to train
    # # --------------------------------------------------------------------

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    # print(training_set_scaled)

    # --------------------------------------------------------------------
    # Long Short-Term Memory stores long term memory state
    # Sequence
    # --------------------------------------------------------------------
    X_train = []
    y_train = []

    # --------------------------------------------------------------------
    # ranging from 28 - length of training set
    # chosen 28 as 28 bits for 2-way associative cache as baseline
    # can choose different number
    # --------------------------------------------------------------------
    for i in range(28, len(training_set)):
        X_train.append(training_set_scaled[i - 28:i, 0])
        y_train.append(training_set_scaled[i, 0])
        X_Array = np.array(X_train)
        y_Array = np.array(y_train)

    # --------------------------------------------------------------------
    # Long Short-Term Memory (LSTM) architecture
    # we have four LSTM layers
    # we have one output layer
    # --------------------------------------------------------------------
    # Reshaping X_train for efficient modelling
    X_Array = np.reshape(X_train, (X_Array.shape[0], X_Array.shape[1], 1))

    regressor = Sequential()
    # # First LSTM layer with Dropout regularisation
    regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_Array.shape[1], 1)))
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
    # Long Short-Term Memory (LSTM) architecture is a Recurrent Neural Net (RNN)
    # --------------------------------------------------------------------

    # Compiling the RNN
    regressor.compile(optimizer='rmsprop', loss='mean_squared_error')
    # Fitting to the training set
    regressor.fit(X_Array, y_Array, epochs=50, batch_size=50)

    # --------------------------------------------------------------------
    # Get test set ready as the training set
    # we get the first 100 entries of the test set have 100 previous values
    # --------------------------------------------------------------------

    # dataset_total = pd.concat((df, df), axis=0)
    # print(len(dataset_total))
    # inputs = dataset_total[len(dataset_total) - len(test_set)].values
    # inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(test_set)

    # Preparing X_test and predicting the cache index + tag
    X_test = []
    for i in range(100, 500):
        X_test.append(inputs[i - 100:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_cache_result = regressor.predict(X_test)
        predicted_cache = sc.inverse_transform(predicted_cache_result)

    # Visualizing the results for LSTM
    Plot_Predictions(test_set, predicted_cache)
    # evaluate model
    Return_RMSE(test_set, predicted_cache)


# def ReplacementPolicyDecision():

def main():
    Train_Replacement_Policy()


if __name__ == '__main__':
    main()
