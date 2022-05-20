#!/usr/bin/python3

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas as pd


def SVMtraining():
    trainingData = pd.read_csv(
        "csv/trainingSets/finalDatasets/finalDataset.csv")

    X = trainingData.drop("class", axis=1)
    y = trainingData["class"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

    classifier = svm.SVC(kernel="linear")

    classifier.fit(X_train, y_train)

    return classifier


if __name__ == "__main__":
    trainingData = pd.read_csv(
        "csv/trainingSets/finalDatasets/finalDataset.csv")

    X = trainingData.drop("class", axis=1)
    y = trainingData["class"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

    classifier = svm.SVC(kernel="linear")

    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    trafficFeatures = [2.927376486136671, 0.527376486136671, 20]
    featuresTest = pd.DataFrame([trafficFeatures])
    featuresTest.columns = ["srcIPEntropy",
                            "dstIPEntropy", "packetCount"]

    # print(classifier.coef_)
    # print(classifier.predict(featuresTest))
    # print(classification_report(y_test, y_pred))

    cfMatrix = confusion_matrix(y_test, y_pred)
    print(cfMatrix)
    print(ConfusionMatrixDisplay(classifier))
