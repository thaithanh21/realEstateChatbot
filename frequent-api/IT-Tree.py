import json
import pickle
from math import exp
import time
start_time = time.time()

data = {
    frozenset({'A'}): {1, 3, 4, 5},
    frozenset({'C'}): {1, 2, 3, 4, 5, 6},
    frozenset({'D'}): {2, 4, 5, 6},
    frozenset({'T'}): {1, 3, 5, 6},
    frozenset({'W'}): {1, 2, 3, 4, 5},
}
data_raw = {

}

class treeNode:
    def __init__(self, nameValue, transaction, parentNode):
        self.name = nameValue
        self.tid = transaction
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {}


    # increments the count variable with a given amount
    def tidre(self, newset):
        return self.tid

    # display tree in text. Useful for debugging
    def disp(self, ind=1):
        print('  ' * ind, self.name, ' ', self.tid)
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(dataSet, minSup=1):  # create IT-tree from dataset but don't mine
    with open('current.pkl', 'rb') as file:
        curr = pickle.load(file)
    start = set(range(1,curr))
    retTree = treeNode('Null Set', start, None)  # create tree
    eclat = []
    for items, trans in dataSet.items():  # seccond pass the dataset to get the transaction set
        if (len(trans) >= minSup):
            eclat.append(items)
            retTree.children[items] = treeNode(items, trans, retTree)
    enumerate_frequent(retTree, eclat, minSup)
    return retTree  # return tree and header table


def enumerate_frequent(reTree, treeNodelist, minSup):
    for i in range(len(treeNodelist)):
        children = []
        for j in range(i + 1, len(treeNodelist)):
            X = treeNodelist[j].union(treeNodelist[i])
            tidi = reTree.children[treeNodelist[i]].tid
            tidj = reTree.children[treeNodelist[j]].tid
            T = tidi.intersection(tidj)
            if (len(T) >= minSup):
                reTree.children[treeNodelist[i]].children[X] = treeNode(X, T, reTree)
                children.append(X)
        if children:
            enumerate_frequent(reTree.children[treeNodelist[i]], children, minSup)
        #print(children)

def minSupcal(itemsetNum):
    c = 0.000
    return itemsetNum*(exp(-0.4*itemsetNum-0.2)+c)


with open('Convert_data_for_It.pkl', 'rb') as file:
    data = pickle.load(file)
    file.close()


# MINSUP = minSupcal(count)
# print(MINSUP)

myTree = createTree(data,333)
#myTree = createTree(data,5)
#print('create tree in ' + str(time.time() - start))

results = []
def traverse(treeNode):
    results.append(list(treeNode.name))
    for child in treeNode.children.values():
        traverse(child)
def mineTree(treeNode):
    for child in treeNode.children.values():
        traverse(child)
    with open('treeIT_00014.txt', 'w', encoding='UTF=8') as outfile:
        for items in results:
            outfile.write("%s\n" % items)
        outfile.close()
    jsondata = {
        'frequent':results
    }
    # with open('frequentItemsIT.json', 'w', encoding='utf8') as outfile:
    #     json.dump(jsondata, outfile, ensure_ascii=False)
    #     outfile.close()

mineTree(myTree)
print('done in ' + str(time.time() - start_time))

#27s create tree
#done in 1377s

#0.0012 in 1583s

#0.0014 in 1150s
