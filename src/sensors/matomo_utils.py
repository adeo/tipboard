# coding: utf-8
import json
from statistics import mean

import requests
import urllib.parse

base_url = "http://analytics-kiosk.apps.op.acp.adeo.com/"
token = "680f0c1944c34e31313e4120162f0e02"


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
    return requests.get(base_url, params=params, verify=False)


def getUsersConnected():
    params = dict()
    response = basicMatomoRequest(method="UserId.getUsers", query=params)
    if response.status_code == 200:
        list_of_users = []
        for user in response.json():
            print(f'🧐 User connected with the Kiosk app : {user["label"]}')
            list_of_users.append(user["label"])
        return list_of_users
    raise


def getMatomoActions(type_of_data=""):
    params = dict()
    response = basicMatomoRequest(method="Events.getAction", query=params)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            if data["label"] == type_of_data:
                # print(f'🍔 full data object : {data}')
                list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        return list_of_data_to_display
    raise
