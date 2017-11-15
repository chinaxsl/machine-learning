from collections import Counter
import numpy as np
from math import log
#������ũ��  ����label����feature�����
def calShonnon(dataSet):
    length = len(dataSet)
    labels = dataSet[:,-1]
    count = Counter(labels)
    Ent = 0
    for key in count:
        prob = count[key]/length
        Ent -= prob * log(prob,2)
    return Ent

def splitData(dataSet,feature,val):
    results = [np.append(i[:feature],i[feature+1:]) for i in dataSet if i[feature] == val]
    return np.array(results)


def findBestFeature(dataSet):
    bestFeature = -1
    bestEnt = 0
    length = len(dataSet.T)
    beforeEnt = calShonnon(dataSet)
    for i in range(length):
        afterEnt = 0
        feature = dataSet[:,i]
        count = Counter(feature)
        for key in count:
            afterEnt += calShonnon(splitData(dataSet,i,key))
        current = beforeEnt - afterEnt
        if(current>bestEnt):
            bestFeature = i
            bestEnt= current
    return bestFeature
               
               
def majorityEnt(dataSet):
    #ͶƱʱdataSetֻʣ�����һ�������ͱ�ǩ
    values = dataSet[:,1]
    count = Counter(value)
    return max(count,key=lambda x:count[x])
    
def createID3Tree(dataSet):
    if(len(set(dataSet[:,-1]))==1):
        return dataSet[0,-1]
    if(len(dataSet.T)== 1):
        return majorityEnt(dataSet)
    bestFeature = findBestFeature(dataSet)
    myTree = {str(bestFeature):{}}
    featureVals = set(dataSet[:,bestFeature])
    for val in featureVals:
        myTree[str(bestFeature)][val] = createID3Tree(splitData(dataSet,bestFeature,val))
    return myTree


if __name__ =="__main__"               
dataSet = [[2,2,"yes"],
            [2,2,"yes"],
            [2,3,"no"],
            [3,2,"no"],
            [3,2,"no"]]
dataSet = np.array(dataSet,'str')
myTree = createID3Tree(dataSet)
print(myTree)