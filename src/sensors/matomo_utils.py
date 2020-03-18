# coding: utf-8
import json
from statistics import mean

import requests
import urllib.parse

# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes
base_url = "http://analytics-warehouse-open.apps.op.acp.adeo.com/index.php?"
token = "9078307dcbdfcc14e1fe7581bcc53baf"

#https://analytics-warehouse.apps.op.acp.adeo.com/index.php?
# date=today&expanded=1&filter_limit=-1&filter_truncate=5&format=JSON&format_metrics=1&idDimension=2&
# idSite=1&method=CustomDimensions.getCustomDimension&module=API&period=day&reportUniqueId=CustomDimensions_getCustomDimension_idDimension--2&
# token_auth=5b9ca53de3e607a002db2e5cfc40d857

#https://analytics-warehouse.apps.op.acp.adeo.com/index.php?
# date=today&expanded=1&filter_limit=-1&format=JSON&
# format_metrics=1&idSite=1&method=VisitTime.getByDayOfWeek&module=API&period=day&
# token_auth=5b9ca53de3e607a002db2e5cfc40d857


#https://analytics-warehouse.apps.op.acp.adeo.com/index.php?
# date=2020-03-09&expanded=1&filter_limit=-1&
# filter_truncate=5&format=JSON&format_metrics=1&idSite=1
# &method=Events.getAction&module=API&period=day
# &token_auth=5b9ca53de3e607a002db2e5cfc40d857

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

def getNbModelDevice():
    params = dict()
    params["idDimension"]=2
    response = basicMatomoRequest(method="CustomDimensions.getCustomDimension", query=params)
    if response.status_code == 200:
        list_of_data_to_display = []
        for data in response.json():
            list_of_data_to_display.append({k: data[k] for k in ('label', 'nb_visits')})
        return list_of_data_to_display
    raise

print( "Nb device par Model : ")
print(getNbModelDevice())
print(getNbUsersConnected())
print(getNbVisitorByDayOfWeek())
print(getMatomoActions())
