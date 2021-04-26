"""
Application : ReplSim
File name   : ANN.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/19/21
Description : This file contains the development of a neural net
              the Neural Net is a recurrent neural net with supervised learning
              called long short-term memory learn sequences
"""

# Copyright (c) April 26, 2021 Jacob Summerville, Martin Lopez, Henry Lee
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from keras.optimizers import SGD
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import mean_squared_error


def Plot_Predictions(test, predicted, mlalgo):
    plt.plot(test, color='red', label='Real Policy Replacement')
    plt.plot(predicted, color='blue', label='Predicted Replacement Policy')
    plt.title('Replacement Policy Prediction Using' + mlalgo)
    plt.xlabel('Number of Replaced (Tag + Index)')  # want to predict patterns of memory hits
    plt.ylabel('Tag + Index Values')
    plt.legend()
    #plt.show()


# -----------------------------------------------------------------
# Calculate the Root Mean Square Error
# -----------------------------------------------------------------
def Return_RMSE(test, predicted):
    rmse = math.sqrt(mean_squared_error(test, predicted))
    # print("The root mean squared error is {}.".format(rmse))
    return rmse


def Plot_Train_Test_Data():
    # -------------------------------------------------------------------
    # plot sequence for prediction
    # plot demonstrates predictability and sequence in index + tag
    # -------------------------------------------------------------------
    dataset = pd.read_csv("gen_mem.csv", header=None)
    df = pd.DataFrame(dataset)
    df[1][:1500].plot(figsize=(16, 4), legend=True)
    df[1][1500:].plot(figsize=(16, 4), legend=True)
    plt.legend(['Training Set', 'Test Set'], )
    plt.title('L1 Smart Cache on Simulated Cache for Replacement Policies')
    #plt.show()


def createTempPredictions(predictions):
    original_mem = pd.read_csv("gen_mem.csv", header=None)
    original_mem = pd.DataFrame(original_mem)
    num_of_predictions = len(predictions)
    data_predictions = pd.DataFrame(predictions)
    len_replace_mem_start = len(original_mem) - num_of_predictions
    # print(original_mem[1500:])
    for i in range(0, num_of_predictions):
        new_orig_mem = original_mem.replace(i, data_predictions[0][i])

    data_new_mem = pd.DataFrame(new_orig_mem)
    list_new_mem = data_new_mem[1].values.tolist()
    return list_new_mem


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
    training_set = df[1][:1500].values
    # print(training_set)
    test_set = df[1][1500:].values
    # print(test_set)

    # # --------------------------------------------------------------------
    # scale our training set from zero to 1 for training set
    # scaled training set will be used to train
    # # --------------------------------------------------------------------

    sc = MinMaxScaler(feature_range=(0, 1))
    dataFrame_train = pd.DataFrame(training_set)
    training_set_scaled = sc.fit_transform(dataFrame_train)
    # print("train_set_scaled")
    # print(training_set_scaled.shape)

    # --------------------------------------------------------------------
    # Long Short-Term Memory stores long term memory state
    # Sequence
    # --------------------------------------------------------------------
    X_train = []
    y_train = []

    # --------------------------------------------------------------------
    # ranging from train 1500 of data set
    # 50 time steps and 1 output
    # --------------------------------------------------------------------
    for i in range(0, 1500):
        X_train.append(training_set_scaled[i])
        y_train.append(training_set_scaled[i])
    X_Array = np.array(X_train)
    y_Array = np.array(y_train)

    # --------------------------------------------------------------------
    # Long Short-Term Memory (LSTM) architecture
    # we have four LSTM layers
    # we have one output layer
    # --------------------------------------------------------------------
    # Reshaping X_train for efficient modelling
    X_Array = np.reshape(X_train, (X_Array.shape[0], X_Array.shape[1], 1))

    # print("Train X_array")
    # print(X_Array.shape)

    regressor = Sequential()
    # First LSTM layer with Dropout regularisation
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
    regressor.add(Dense(units=1, activation='sigmoid'))

    # --------------------------------------------------------------------
    # Long Short-Term Memory (LSTM) architecture is a Recurrent Neural Net (RNN)
    # --------------------------------------------------------------------

    # Compiling the RNN
    regressor.compile(optimizer='rmsprop', loss='mean_squared_error')
    # Fitting to the training set
    regressor.fit(X_Array, y_Array, epochs=150, batch_size=200, verbose=0)

    # --------------------------------------------------------------------
    # Get test set ready as the training set
    # we get the first 100 entries of the test set have 100 previous values
    # --------------------------------------------------------------------

    # dataset_total = pd.concat((df[1][:1500], df[1][1500:]), axis=0)
    # data = pd.DataFrame(dataset_total)
    # inputs = data[len(dataset_total) - len(test_set)].values
    # print(inputs)
    # inputs.reshape(-1, 1)

    test_set.reshape((-1, 1))
    dataFrame_test = pd.DataFrame(test_set)
    # print(test_set)
    test_set_scaled = sc.transform(dataFrame_test)
    # print(test_set_scaled)

    # Preparing X_test and predicting the cache index + tag
    # test 500 of data set
    X_test = []
    for i in range(0, len(test_set)):
        X_test.append(test_set_scaled[i])

    X_test_array = np.array(X_test)
    # print("x_test_array scaled")
    # print(X_test_array.shape)
    X_test_array = np.reshape(X_test_array, (X_test_array.shape[0], X_test_array.shape[1], 1))
    # print("reshaped")
    # print(X_test_array.shape)
    predicted_cache_result = regressor.predict(X_test_array)
    # print("Predicted")
    # print(predicted_cache_result)
    predicted_cache_result = sc.inverse_transform(predicted_cache_result)

    # Visualizing the results for LSTM
    lstm_algo = 'Long Short-Term Memory (LSTM)'
    # Plot_Predictions(test_set, predicted_cache_result, lstm_algo)
    # evaluate model
    LSTM_rmse = Return_RMSE(test_set, predicted_cache_result)

    # The GRU architecture
    regressorGRU = Sequential()
    # First GRU layer with Dropout regularisation
    regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_Array.shape[1], 1), activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    # Second GRU layer
    regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_Array.shape[1], 1), activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    # Third GRU layer
    regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_Array.shape[1], 1), activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    # Fourth GRU layer
    regressorGRU.add(GRU(units=50, activation='tanh'))
    regressorGRU.add(Dropout(0.2))
    # The output layer
    regressorGRU.add(Dense(units=1))
    # Compiling the RNN
    regressorGRU.compile(optimizer=SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=False), loss='mean_squared_error')
    # Fitting to the training set
    regressorGRU.fit(X_Array, y_Array, epochs=150, batch_size=200, verbose=0)

    # Preparing X_test and predicting the prices
    X_test_GRU = []
    for i in range(0, len(test_set)):
        X_test_GRU.append(test_set_scaled[i])
    X_test = np.array(X_test_GRU)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    GRU_predicted = regressorGRU.predict(X_test)
    GRU_predicted = sc.inverse_transform(GRU_predicted)

    # Visualizing the results for LSTM
    gru_algo = 'Gated Recurrent Units (GRU)'
    # Plot_Predictions(test_set, GRU_predicted, gru_algo)
    # evaluate model
    GRU_rmse = Return_RMSE(test_set, GRU_predicted)

    if GRU_rmse < LSTM_rmse:
        print("LSTM Root Mean Square: " + str(LSTM_rmse))
        print("GRU Root Mean Square: " + str(GRU_rmse))
        return GRU_predicted
    else:
        print("LSTM Root Mean Square: " + str(LSTM_rmse))
        print("GRU Root Mean Square: " + str(GRU_rmse))
        return predicted_cache_result


def main():
    os.chdir("../mem/")

    # Plot_Train_Test_Data()
    predictions = Train_Replacement_Policy()
    temp_cache_data = createTempPredictions(predictions)
    return temp_cache_data

if __name__ == '__main__':
    main()

