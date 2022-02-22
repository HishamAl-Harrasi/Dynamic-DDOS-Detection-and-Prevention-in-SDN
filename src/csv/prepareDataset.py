import pandas as pd

normalData = pd.read_csv("trainingSets/trainingSet2/normalTraffic.csv")
ddosData = pd.read_csv("trainingSets/trainingSet2/ddosTraffic.csv")

normalData["class"] = 0
ddosData["class"] = 1

normalData.to_csv("trainingDataset.csv", header=True, index=False)
ddosData.to_csv("trainingDataset.csv", mode="a", header=False, index=False)


