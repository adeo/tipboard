# coding: utf-8
from datetime import datetime, timedelta

import requests

# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes
base_url = "http://velocity-analytics-open.apps.op.acp.adeo.com/index.php?"
token = "8b44ade2c46279b0b4678356b7241803"


# http://velocity-analytics-open.apps.op.acp.adeo.com/index.php?date=today&expanded=1&filter_limit=-1&format=JSON&idSite=1&method=Events.getAction&module=API&period=day&token_auth=anonymous

# Paramètres de base d'une requête Matomo
def basicMatomoRequest(method="", query=None):
    if query is None:
        query = {}
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = method
    params["period"] = "day"
    params["date"] = "today"
    params["format"] = "JSON"
    params["idSite"] = "1"
    params.update(query)
    return requests.get(base_url, params=params, verify=False)


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


def getNbVisitorByDayOfWeek():
    params = dict()
    response = basicMatomoRequest(method="VisitTime.getByDayOfWeek", query=params)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        return list_of_data_to_display
    raise


def getMatomoActions(type_of_data=""):
    params = dict()
    response = basicMatomoRequest(method="Events.getAction", query=params)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        return list_of_data_to_display
    raise


def getCountScans():
    params = dict()
    response = basicMatomoRequest(method="Events.getAction", query=params)
    if response.status_code == 200:
        list_of_data_to_display = dict()
        for data in response.json():
            value = dict()
            for k in ('nb_uniq_visitors', 'nb_events'):
                value[k] = data[k]
            list_of_data_to_display[data['label']] = value

        return list_of_data_to_display
    raise


def getCountEventForDays(dateValue=None):
    params = dict()
    if dateValue == None:
        params["date"] = datetime.now()
    else:
        params["date"] = dateValue
    response = basicMatomoRequest(method="Events.getAction", query=params)
    if response.status_code == 200:
        list_of_data_to_display = dict()
        for data in response.json():
            value = dict()
            for k in ('nb_uniq_visitors', 'nb_events'):
                value[k] = data[k]
            list_of_data_to_display[data['label']] = value

        return list_of_data_to_display
    raise


def getNbModelDevice():
    params = dict()
    params["idDimension"] = 2
    response = basicMatomoRequest(method="CustomDimensions.getCustomDimension", query=params)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        return list_of_data_to_display
    raise


def getScanFor7Days():
    list_of_data_to_display = []
    dateValue = datetime.now()
    fromDate = datetime.now() - timedelta(days=7)
    while fromDate <= dateValue:
        events = dict()
        print(fromDate.strftime('%Y-%m-%d'))
        dataEvents = getCountEventForDays(fromDate.strftime('%Y-%m-%d'))
        if 'onScan' in dataEvents:
            print(dataEvents['onScan']['nb_events'])

        events[fromDate.strftime('%Y-%m-%d')] = getCountEventForDays(fromDate.strftime('%Y-%m-%d'))
        print(events)
        list_of_data_to_display.append(events)
        fromDate = fromDate + timedelta(days=1)
    return list_of_data_to_display


print(getScanFor7Days())
