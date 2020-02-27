# coding: utf-8
import json
from statistics import mean

import requests
import urllib.parse

base_url = "http://analytics-kiosk.apps.op.acp.adeo.com/"
token = "b327b86aed12fd5a3023363d421f29a2"


# Paramètres de base d'une requête Matomo
def basicMatomoRequest(method="", query=None):
    if query is None:
        query = {}
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = method
    params["period"] = "month"
    params["date"] = "today"
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
            list_of_users.append(user["label"])
        return list_of_users
    raise


# Récupère le nombre des users ayant actuellement le kiosk installé
# ⚠️ 0 sur la prod, mais 2 sur le matomo de Test
def getNbUsersConnected():
    params = dict()
    params["lastMinutes"] = 30
    response = basicMatomoRequest(method="Live.getCounters", query=params)
    if response.status_code == 200:
        list_of_users = []
        for user in response.json():
            list_of_users.append(user["visitors"])
        return list_of_users
    raise


# Récupère les actions de type SSLError ou Crash passées en param
def getMatomoActionOfTheDay(type_of_data=""):
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = "Events.getAction"
    params["period"] = "day"
    params["date"] = "today"
    params["format"] = "JSON"
    params["idSite"] = "1"
    response = requests.get(base_url, params=params, verify=False)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            if data["label"] == type_of_data:
                list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        if len(response.json()) == 0:
            list_of_data_to_display.append({'label': type_of_data, 'nb_visits': 0})
        return list_of_data_to_display
    raise


def getMatomoActions(type_of_data=""):
    params = dict()
    response = basicMatomoRequest(method="Events.getAction", query=params)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            if data["label"] == type_of_data:
                list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        return list_of_data_to_display
    raise


# Récupère les profils déployés sur les Tablettes
def getProfiles():
    params = dict()
    params["idSubtable"] = 3
    response = basicMatomoRequest(method="Events.getNameFromActionId", query=params)
    if response.status_code == 200:
        list_of_profiles = []
        for profile in response.json():
            if "LOADED" in profile["label"]:
                # Formatage du nom du profil => Nom - nbPages
                profile_to_display = f'{profile["label"].split(" ")[-1]} - {profile["label"].split(" ")[1]}'
                list_of_profiles.append(profile_to_display)
        return list_of_profiles
    raise


# Récupère le nombre de devices connectés avec un Kiosk déployé
def getNbOfDevices():
    params = dict()
    response = basicMatomoRequest(method="UserId.getUsers", query=params)
    if response.status_code == 200:
        data = len(response.json())
        return data
    raise
