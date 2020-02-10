# coding: utf-8
import json
from statistics import mean

import requests
import urllib.parse

base_url = "http://benchmark-analytics-open.apps.op.acp.adeo.com/"
token = "0b44547f5f0c9d526b46247c65aeef57"


# logging.basicConfig(level=logging.DEBUG)
def basicMatomoRequest(method="", query=None):
    if query is None:
        query = {}
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = method
    params["period"] = "range"
    params["date"] = "2020-01-13,2020-03-10"
    params["format"] = "JSON"
    params["idSite"] = "1"
    params.update(query)
    return requests.get(base_url, params=params)


def getValueFromActionID(segment, id):
    params = dict()
    params["segment"] = segment
    params["idSubtable"] = id
    response = basicMatomoRequest(method="Events.getNameFromActionId", query=params)
    if response.status_code == 200:
        responsesList = []
        for values in response.json():
            responsesList.append(values["label"])
        return responsesList
    raise


def getActionsIdByCategory(segment):
    params = dict()
    params["segment"] = segment
    response = basicMatomoRequest(method="Events.getAction", query=params)
    # print(f'URL ciblée : {response.url}')
    if response.status_code == 200:
        # print(f'🍔 Model : {segment} || response.json() : {response.json()}')
        for test in response.json():
            print(test["label"])
        idSubList = []
        for action in response.json():
            idSubList.append({k: action[k] for k in ('label', 'idsubdatatable')})
        return idSubList
    raise


def getCategories():
    params = dict()
    response = basicMatomoRequest(method="Events.getCategory", query=params)
    if response.status_code == 200:
        categoryList = []
        for category in response.json():
            categoryList.append({k: category[k] for k in ('label', 'segment')})
        return categoryList
    raise


def valueFromAction(action):
    test = []
    categoryList = getCategories()
    for segment in categoryList:
        x = dict()
        x["device"] = segment["label"]
        print(f'❌  device : {segment["label"]}')
        if segment["label"] == "TC52 - 8.1.0":
            # segment["segment"] = urllib.parse.quote(segment["segment"])
            segment["segment"] = "eventCategory%3D%3DTC52%2520-%25208.1.0"
        idSubList = getActionsIdByCategory(segment["segment"])
        for id in idSubList:
            if id["label"] == action:
                x["values"] = [float(item) for item in getValueFromActionID(segment["segment"], id["idsubdatatable"])]
                x["avg"] = mean(x["values"])
        if "values" in x:
            test.append(x)
    return test


def getDevices():
    return [label["label"] for label in getCategories()]
