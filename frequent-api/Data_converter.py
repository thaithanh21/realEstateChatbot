import json
import operator
import pickle
grouptag = {
  "addr_street": 0,
  "addr_district": 0,
  "addr_city": 0,
  "addr_ward": 0,
  "position": 0,
  "area": 0,
  "price": 0,
  "transaction_type": 0,
  "realestate_type": 0,
  "legal": 0,
  "potential": 0,
  "surrounding": 0,
  "surrounding_characteristics": 0,
  "surrounding_name": 0,
  "interior_floor": 0,
  "interior_room": 0,
  "orientation": 0,
  "project": 0
}
veriaty = {
  "addr_street": {},
  "addr_district": {},
  "addr_city": {},
  "addr_ward": {},
  "position": {},
  "area": {},
  "price": {},
  "transaction_type": {},
  "realestate_type": {},
  "legal": {},
  "potential": {},
  "surrounding": {},
  "surrounding_characteristics": {},
  "surrounding_name": {},
  "interior_floor": {},
  "interior_room": {},
  "orientation": {},
  "project": {}
}
# datatest = [{'tags':{'A':['a'],'C':['c'],'T':['t'],'W':['w']}},
#             {'tags':{'C':['c'],'D':['d'],'W':['w']}},
#             {'tags':{'A':['a'],'C':['c'],'T':['t'],'W':['w']}},
#             {'tags':{'A':['a'],'C':['c'],'D':['d'],'W':['w']}},
#             {'tags':{'A':['a'],'C':['c'],'D':['d'],'T':['t'],'W':['w']}},
#             {'tags':{'C':['c'],'D':['d'],'T':['t']}}]
def dataconvertFP(b,retDict = {}):
    sentence = []
    list=[]
    for tags in b:
        a = tags["tags"]
        for tag, value in a.items():
            for item in value:
                list.append(item+':'+tag)
                grouptag[tag] += 1
                if item in veriaty[tag]:
                    veriaty[tag][item] += 1
                else:
                    veriaty[tag][item] = 1
        if frozenset(list) in retDict:
            retDict[frozenset(list)] = retDict[frozenset(list)] + 1
        else:
            retDict[frozenset(list)] = 1
        list = []
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
        for item in list:
            if (frozenset([item]) in retDict):
                temp = retDict[frozenset([item])]
                retDict[frozenset([item])] = temp.union({count})
            else:
                retDict[frozenset([item])] = {count}
        count += 1
        list = []
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
def convertFP(dataRaw,con=False):
    if(con):
        with open('Convert_data_for_Fp.pkl','rb') as file:
            data = pickle.load(file)
            data = dataconvertFP(dataRaw,data)
    else:
        data = dataconvertFP(dataRaw)
    with open('Convert_data_for_Fp.pkl','wb') as file:
        pickle.dump(data,file)

# def genMIS():

dataRaw = []



with open('fullBDS.json', 'r', encoding='utf8') as infile: #change data location
    dataRaw = json.load(infile)
    infile.close()

# convertIT(datatest)
# convertFP(datatest)
convertIT(dataRaw) #unblock to convert data to IT input data
print('done convert IT')
convertFP(dataRaw) #unblock to convert data to FP input data
#
with open('tag_aspect.pkl','wb') as file:
    pickle.dump(veriaty,file)
    file.close()

with open('tag_aspect.txt','w',encoding='UTF=8') as outfile:
    for tag in temp:
        for item in temp[tag]:
            outfile.write("%s\n" % item+":"+tag)
    outfile.close()

# final = 0
# print(temp)
# print(len(temp))
# for item in temp:
#     final += len(temp[item])
#     print(final)
# with open('Tags_num.pkl','rb') as file:
#     temp2 = pickle.load(file)
#     file.close()
# print(temp2)
# trungbinh = 19.651378623972306
# density = (trungbinh/final)*100
# print(density)


