# coding: utf-8
import json
from statistics import mean

import requests
import urllib.parse

base_url = "http://analytics-kiosk.apps.op.acp.adeo.com/"
token = "b327b86aed12fd5a3023363d421f29a2"


def basicMatomoRequest(method="", query=None):
    if query is None:
        query = {}
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = method
    params["period"] = "month"
    params["date"] = "2020-02-25"
    params["format"] = "JSON"
    params["idSite"] = "1"
    params.update(query)
    return requests.get(base_url, params=params, verify=False)


# Récupère les id des devices qui ont le kiosk installé
def getUsersConnected():
    params = dict()
    response = basicMatomoRequest(method="UserId.getUsers", query=params)
    if response.status_code == 200:
        list_of_users = []
        for user in response.json():
            # print(f'🧐 User connected with the Kiosk app : {user["label"]}')
            list_of_users.append(user["label"])
        return list_of_users
    raise


# Récupère le nombre des users ayant actuellement le kiosk installé
def getNbUsersConnected():
    params = dict()
    params["lastMinutes"] = 30
    response = basicMatomoRequest(method="Live.getCounters", query=params)
    if response.status_code == 200:
        list_of_users = []
        for user in response.json():
            # print(f'🧐 Nb of users connected : {user["visitors"]}')
            list_of_users.append(user["visitors"])
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


def getProfiles():
    params = dict()
    params["idSubtable"] = 3
    response = basicMatomoRequest(method="Events.getNameFromActionId", query=params)
    if response.status_code == 200:
        list_of_profiles = []
        for profile in response.json():
            # print(profile["label"])
            if "LOADED" in profile["label"]:
                # print(f'🍔 full data object : {profile}')
                list_of_profiles.append(profile["label"])
        return list_of_profiles
    raise
