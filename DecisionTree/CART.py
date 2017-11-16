from collections import Counter
from itertools import combinations
import numpy as np
def calGeni(dataSet):
    length = len(dataSet)
    count = Counter(dataSet[:][-1])
    Geni = 1
    for key in count:
        prob = count[key]/length
        Geni-=prob*prob
    return Geni
def featureSplit(features):
    length = len(features)
    temp =[]
    for i in range(1,length):
        temp = temp+ list(combinations(features,len(features[:i])))
    comLen = len(temp)
    result = zip(temp[:comLen//2],temp[-1:comLen//2-1:-1])
    return list(result)


def splitData(dataSet,key,vals):
    result = [i[:key]+i[key+1:] for i in dataSet if (i[key] in vals)]
    return result

def findBestFeature(dataSet):
    BestFeature = -1
    BestGeni = 1.0
    BestRight = ()
    BestLeft = ()
    featureNum = len(dataSet[0])
    length = len(dataSet)
    for i in range(featureNum-1):
        feature = [example[i] for example in dataSet]
        for j in featureSplit(feature):
            GeniGain = 0.0
            if (len(j)==0):
                continue
            (left,right) = j
            left_split = splitData(dataSet,i,left)
            prob = len(left_split)/length
            GeniGain += prob * calGeni(left_split)
            right_split = splitData(dataSet,i,right)
            prob = len(left_split)/length
            GeniGain += prob * calGeni(right_split)

            if(GeniGain<=BestGeni):
                BestFeature = i
                BestGeni = GeniGain
                BestLeft = left
                BestRight = right
    return BestFeature,BestLeft,BestRight

def majorityGeni(dataSet):
    value = [i[-1] for i in dataSet]
    count = Counter(value)
    return max(count,key = lambda x:count[x])

def createCART(dataSet,labelName):
    labels = [e[-1] for e in dataSet]
    if (len(set(labels))==1):
        return dataSet[0][-1]
    if (len(dataSet[0])==1):
        return majorityGeni(dataSet)
    feature,left,right= findBestFeature(dataSet)
    if (feature ==-1):
        return majorityGeni(dataSet)
    BestLabel = labelName[feature]
    myTree = {BestLabel:{}}
    del(labelName[feature])
    subLabels = labelName[:]
    myTree[BestLabel]['left'] = createCART(splitData(dataSet,feature,left),subLabels)
    subLabels1 = labelName[:]
    myTree[BestLabel]['right'] = createCART(splitData(dataSet,feature,right),subLabels1)
    return myTree

if __name__ == "__main__"
dataSet = [[2,3,"yes"],
            [2,3,"yes"],
            [2,2,"no"],
            [2,2,"no"],
            [3,2,"no"]]
myTree = createCART(dataSet,["name1","name2"])
print(myTree)
