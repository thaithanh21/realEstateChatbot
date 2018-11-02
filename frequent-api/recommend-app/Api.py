from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from collections import defaultdict

app = Flask(__name__)
CORS(app)
b = []
oviousSet = ['mua:transaction_type', 'bán:transaction_type', 'tp . hcm:addr_city']
with open('frequentItemsFP.json', 'r', encoding='utf8') as f:
    frequent = json.load(f)
    for i, val in frequent.items():
        for j in val:
            j = list(set(j).difference(set(oviousSet)))
            b.append(j)

@app.route('/')
def index():
    return "Index API"


def convertToSetInput(a):
    list = []
    for i in a:
        list.append(i['content']+':'+i['type'])
    return list

def convertToListInput(a):
    list = []
    for i in a:
        dic = {}
        con, tag = i.split(':')
        dic['content'] = con
        dic['type'] = tag
        list.append(dic)
    return list

def convertion(list):
    results = {}
    for i in list:
        results[i['type']] = []
    for i in list:
        results[i['type']].append(i['content'])
    return results

def findinrule(a):
    c = defaultdict(int)
    for i in b:
        if(set(a).issubset(set(i))):
            for f in set(i).difference(set(a)):
                c[f] += 1
    return c

def permutation(loi,results,per,count = 1):
    res = []
    for i in results:
        for j in loi:
            if(type(i)==str):
                i = set({i})
            temp = i.union({j})
            if(len(temp)==count):
                res.append(temp)
    res = [set(x) for x in set(tuple(x) for x in res)]
    if(count<per):
        count+=1
        return permutation(loi,res,per,count)
    else:
        return res

def fixlogic(loi):
    result = []
    best = 0
    for j in range(1,len(loi)):
        per = permutation(loi,loi,j)
        for i in per:
            print(i)
            temp = list(set(loi).difference(i))
            print(temp)
            c = findinrule(temp)
            print(c)
            sumup = 0
            for key,val in c.items():
                sumup+=val
            if(sumup > best):
                result = c
                best = sumup
                print(best)
                bad = i
        if(result and bad):
            break
    return result,bad


@app.route('/recom/v1/posts', methods=['POST'])
def analyze_query():
    req = request.json
    num = req["numre"]
    bad = []
    a = convertToSetInput(req["tags"])
    a = list(set(a).difference(set(oviousSet)))
    print(a)
    c = findinrule(a)
    if(not c):
        c , bad = fixlogic(a)
        bad = convertToListInput(bad)
    results = sorted(c, key=c.__getitem__, reverse=True)
    if len(results) > num:
        temp = []
        for n in range(num):
            temp.append(results[n])
        temp = convertToListInput(temp)
        temp = convertion(temp)
        if(bad):
            temp["bad_aspect"] = bad
        print(temp)
        return jsonify(temp)
    else:
        results = convertToListInput(results)
        results = convertion(results)
        if(bad):
            results["bad_aspect"] = bad
        print(results)
        return jsonify(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5400)