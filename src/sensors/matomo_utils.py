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
            if "LOADED" in profile["label"]:
                # Formatage du nom du profil => Nom - nbPages
                profile_name = profile["label"].split(' ')[-1]
                profile_nb_pages = profile["label"].split(' ')[1]
                profile_to_display = f'{profile_name} - {profile_nb_pages}'
                list_of_profiles.append(profile_to_display)
        return list_of_profiles
    raise


def getNbOfDevices():
    params = dict()
    response = basicMatomoRequest(method="UserId.getUsers", query=params)
    if response.status_code == 200:
        data = len(response.json())
        return data
    raise


def getWeeklyDatas():
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = "VisitTime.getByDayOfWeek"
    params["period"] = "day"
    params["date"] = "today"
    params["format"] = "JSON"
    params["idSite"] = "2"
    response = requests.get(base_url, params=params, verify=False)
    average_day = {
        'title': {},
        'legend': {'display': True},
        'labels': [],
        'datasets': [{
            'label': "Utilisation du Kiosk",
            'data': [],
            'backgroundColor': 'rgba(66, 165, 245, 0.8)',
            'borderColor': 'rgba(66, 165, 245, 0.8)'
        }]
    }
    if response.status_code == 200:
        for day in response.json():
            if day["day_of_week"] is not 6 or day["day_of_week"] is not 7:
                average_day['labels'].append(day["label"])
                average_day["datasets"][0]["data"].append(int(day["nb_visits"]))
        return average_day
    raise



