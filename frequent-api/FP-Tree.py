import pickle
from bson.json_util import loads
import bson
import json
from math import exp
import time
start = time.time()



class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {}
#increments the count variable with a given amount
    def inc(self, numOccur):
        self.count += numOccur
#display tree in text. Useful for debugging
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup=1): #create FP-tree from dataset but don't mine
    headerTable = {}
    #go over dataSet twice
    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    #print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link
    #print 'headerTable: ',headerTable
    retTree = treeNode('Null Set', 1, None) #create tree
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),
                                  key=lambda p: p[0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.append(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases,minSup)
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def minSupcal(itemsetNum):
    c = 0.0006
    return itemsetNum*(exp(-0.4*itemsetNum-0.2)+c)


with open('Convert_data_for_Fp.pkl','rb') as file:
    data = pickle.load(file)
    file.close()
print('data len: ' + str(len(data)))
MINSUP = minSupcal(len(data))
print(MINSUP)
myFPtree, myHeaderTab = createTree(data,MINSUP)
freqItems = []
mineTree(myFPtree,myHeaderTab,minSupcal(len(data)),([]),freqItems)
print(freqItems)
print(myHeaderTab)

def convertToJson(freqItems):
    freqItemsJson = ({})
    temp = ''
    for items in freqItems:
        if(len(items) == 1):
            temp = items[0]
            freqItemsJson[temp] = [items]
        else:
            freqItemsJson[temp].append(items)
    return freqItemsJson


with open('treeFP.txt','w',encoding='UTF=8') as outfile:
    for items in freqItems:
        outfile.write("%s\n" % items)
    outfile.close()
jsonfile = convertToJson(freqItems)
with open('frequentItemsFP.json','w',encoding='utf8') as outfile:
    json.dump(jsonfile,outfile,ensure_ascii=False)
    outfile.close()

print('done in ' + str(time.time() - start))
#2500s ~ 42 min