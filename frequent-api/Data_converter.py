import json
import pickle

import time
start = time.time()

def dataconvertFP(b):
    retDict = {}
    sentence = []
    list=[]
    for tags in b:
        a = tags["tags"]
        for tag, value in a.items():
            for item in value:
                list.append(item+':'+tag)
        sentence.append(list)
        list = []
    for trans in sentence:
        retDict[frozenset(trans)] = 1
    return retDict

def dataconvertIT(b, count=1, retDict={}):
    sentence = []
    list = []
    for tags in b:
        a = tags["tags"]
        for tag, value in a.items():
            for item in value:
                list.append(item + ':' + tag)
        sentence.append(list)
        list = []
    #print(sentence)
    for trans in sentence:
        for item in trans:
            if (frozenset([item]) in retDict):
                temp = retDict[frozenset([item])]
                retDict[frozenset([item])] = temp.union({count})
            else:
                retDict[frozenset([item])] = {count}
        print(count)
        count += 1

    return retDict, count


def convertIT(dataRaw,con=False):

    if (con):
        with open('current.pkl', 'rb') as curr:
            count = pickle.load(curr)
            with open('Convert_data_for_It.pkl', 'rb') as file:
                data = pickle.load(file)
                data, count = dataconvertIT(dataRaw,count,data)
                with open('Convert_data_for_It.pkl', 'wb') as file:
                    pickle.dump(data, file)
                with open('current.pkl', 'wb') as curr:
                    pickle.dump(count, curr)
    else:
        data, count = dataconvertIT(dataRaw)
        with open('Convert_data_for_It.pkl', 'wb') as file:
            pickle.dump(data, file)
        with open('current.pkl', 'wb') as curr:
            pickle.dump(count,curr)

def convertFP(dataRaw):
    data = dataconvertFP(dataRaw)
    with open('Convert_data_for_Fp.pkl','wb') as file:
        pickle.dump(data,file)

dataRaw = []

#with open('fullBDS.json', 'r', encoding='utf8') as infile: #change data location
#    dataRaw = json.load(infile)
#    infile.close()

def firstNode():
    with open('Convert_data_for_It.pkl', 'rb') as file:
        data = pickle.load(file)
        file.close()
    start = set()
    for items, trans in data.items():  # first pass the dataset to get the transaction set
        start = start.union(trans)
    with open('first_node.pkl', 'wb') as file:
        pickle.dump(start,file)
        file.close()



convertFP(dataRaw) #unblock to convert data to FP input data
#firstNode()
#convertIT(dataRaw) #unblock to convert data to IT input data



print('done in ' + str(time.time() - start))
