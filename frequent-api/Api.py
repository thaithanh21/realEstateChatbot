from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from collections import defaultdict

app = Flask(__name__)
CORS(app)


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

@app.route('/recom/v1/posts', methods=['POST'])
def analyze_query():
    b = []
    oviousSet = ['mua:transaction_type', 'bán:transaction_type', 'tp . hcm:addr_city']
    with open('frequentItemsFP.json', 'r', encoding='utf8') as f:
        frequent = json.load(f)
        for i, val in frequent.items():
            for j in val:
                j = list(set(j).difference(set(oviousSet)))
                b.append(j)
    req = request.json
    c = defaultdict(int)
    a = convertToSetInput(req["tags"])
    a = list(set(a).difference(set(oviousSet)))
    for i in b:
        if(set(a).issubset(set(i))):
            for f in set(i).difference(set(a)):
                c[f] += 1
            #print(set(i).difference(set(a)))
    results = sorted(c, key=c.__getitem__, reverse=True)
    if len(results) > 5:
        temp = []
        for n in range(5):
            temp.append(results[n])
        temp = convertToListInput(temp)
        temp = convertion(temp)
        print(temp)
        return jsonify(temp)
    else:
        results = convertToListInput(results)
        results = convertion(results)
        print(results)
        return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)