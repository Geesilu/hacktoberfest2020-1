# -*- coding: utf-8 -*-
"""Wine logistic regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19QShB8M_xy0rwMQyeYZ30XLfjBLTKF12
"""

import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random
import math
from statistics import mean

# loading the data
wine = datasets.load_wine()
print(wine.DESCR)
df = pd.DataFrame(
    data=np.c_[wine["data"], wine["target"]], columns=wine["feature_names"] + ["target"]
)
X = pd.DataFrame(wine.data)
Y = pd.DataFrame(wine.target)
print("ORIGINAL DATA:")
print(df)
print(X, Y)

# normalize the dataset
for column in X.columns:
    X[column] = (X[column] - X[column].min()) / (X[column].max() - X[column].min())

print(X)
# One-vs-All
df = X.copy()
df["target"] = Y

# 1st
def logistic_regression(dataset, learning_rate, rho, epoch):

    rows = len(dataset.axes[0])
    cols = len(dataset.axes[1])
    X = dataset.iloc[:, :-1]
    Y = dataset.iloc[:, -1]

    X.insert(0, "DEFAULT", 1, True)
    X_arr = X.to_numpy()
    Y_arr = Y.to_numpy()

    # X_arr=np.append(X_arr,0, axis=0)
    w = []
    for i in range(cols):
        w.append(random.uniform(-0.3, 0.3))

    w = np.array(w)
    J_w = 0
    J_w_in = 0
    diff_J = 0
    l = learning_rate
    m = len(X_arr)
    for i in range(epoch):

        h_x = 1 / (1 + np.exp(-(np.dot(X_arr, w))))
        for k in range(m):
            J_w_in = (
                J_w_in
                + Y_arr[k] * math.log(h_x[k])
                + (1 - Y_arr[k]) * math.log(1 - h_x[k])
            )

        J_w_in = -J_w_in / m

        for j in range(len(w)):
            for k in range(m):

                diff_J = (h_x[k] - Y_arr[k]) * X_arr[k][j]
            w[j] = w[j] - (l * diff_J) / m

        h_x = 1 / (1 + np.exp(-(np.dot(X_arr, w))))
        for k in range(m):
            J_w = (
                J_w
                + Y_arr[k] * math.log(h_x[k])
                + (1 - Y_arr[k]) * math.log(1 - h_x[k])
            )

        J_w = -J_w / m
        # if(abs(J_w-J_w_in)>rho):
        # break
    return w


# k-fold crossvalidation
k = []
for i in range(5):
    fold = df.sample(frac=0.2)
    df = df.drop(fold.index)
    k.append(fold)

print(k)

acc = []
test = []
train = []
validation = []
pred_Y = []
w = []
l = 0
for i in range(len(k)):
    frames = []
    for j in range(len(k)):
        if i != j:
            frames.append(k[j])
        else:
            test = k[j]
    train = pd.concat(frames)

    # For class_0
    y0 = train["target"].copy()
    y1 = test["target"].copy()

    train["target"].replace({0.0: 1.0, 1.0: 0.0, 2.0: 0.0}, inplace=True)
    test["target"].replace({0.0: 1.0, 1.0: 0.0, 2.0: 0.0}, inplace=True)

    train.drop("target", axis="columns", inplace=True)
    test.drop("target", axis="columns", inplace=True)

    train["target"] = y0
    test["target"] = y1

    # Training 1st Model
    w0 = logistic_regression(train, 0.2, 0.001, 10)

    # For class_1
    y0 = train["target"].copy()
    y1 = test["target"].copy()

    train["target"].replace({0.0: 0.0, 1.0: 1.0, 2.0: 0.0}, inplace=True)
    test["target"].replace({0.0: 0.0, 1.0: 1.0, 2.0: 0.0}, inplace=True)

    train.drop("target", axis="columns", inplace=True)
    test.drop("target", axis="columns", inplace=True)

    train["target"] = y0
    test["target"] = y1

    # Training 2nd Model
    w1 = logistic_regression(train, 0.2, 0.001, 10)

    # For class_2
    y0 = train["target"].copy()
    y1 = test["target"].copy()

    train["target"].replace({0.0: 0.0, 1.0: 0.0, 2.0: 1.0}, inplace=True)
    test["target"].replace({0.0: 0.0, 1.0: 0.0, 2.0: 1.0}, inplace=True)

    train.drop("target", axis="columns", inplace=True)
    test.drop("target", axis="columns", inplace=True)

    train["target"] = y0
    test["target"] = y1

    # Training 3rd Model
    w2 = logistic_regression(train, 0.2, 0.001, 10)

    w = [w0, w1, w2]
    print("Accuracy for ", (i + 1), " fold: ")
    print(performance(test, w)[1])
    acc.append(performance(test, w)[1])

print("Overall Accuracy: ", mean(acc))
max_value = max(acc)
max_index = acc.index(max_value)
test = k[max_index]
pred_Y = performance(test, w)[0]
print("Class-wise Accuracy: ", confusion(test, pred_Y)[0])
print("Class-wise Precision: ", confusion(test, pred_Y)[1])
print("Class-wise Recall: ", confusion(test, pred_Y)[2])


def performance(dataset, weights):
    X = dataset.iloc[:, :-1]
    Y = dataset.iloc[:, -1]

    X.insert(0, "DEFAULT", 1, True)
    X_arr = X.to_numpy()
    Y_arr = Y.to_numpy()
    Y_predict = np.zeros(len(Y_arr))

    h1 = 1 / (1 + np.exp(-(np.dot(X_arr, weights[0]))))
    h2 = 1 / (1 + np.exp(-(np.dot(X_arr, weights[1]))))
    h3 = 1 / (1 + np.exp(-(np.dot(X_arr, weights[2]))))
    h = [h1, h2, h3]
    for i in range(len(h1)):
        m_a_x = float("-inf")
        pred = 0.0
        for j in range(len(h)):
            if m_a_x < h[j][i]:
                m_a_x = h[j][i]
                pred = j

        Y_predict[i] = pred
    count = 0

    for i in range(np.size(Y_predict)):
        if Y_predict[i] == Y_arr[i]:
            count = count + 1

    return Y_predict, (count / np.size(Y_predict)) * 100


from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


def confusion(dataset, Y_pred):
    X = dataset.iloc[:, :-1]
    Y = dataset.iloc[:, -1]

    X.insert(0, "DEFAULT", 1, True)
    X_arr = X.to_numpy()
    Y_arr = Y.to_numpy()
    cm = confusion_matrix(Y_arr, Y_pred)
    p = precision_score(Y_arr, Y_pred, average=None, zero_division=1)
    r = recall_score(Y_arr, Y_pred, average=None, zero_division=1)

    # Now the normalize the diagonal entries

    cm = cm.astype("float") / cm.sum(axis=1)

    return cm.diagonal() * 100, p, r
