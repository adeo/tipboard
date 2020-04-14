# coding: utf-8
from datetime import datetime, timedelta

import requests
import unidecode
# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes


from src.sensors.soti_utils import getWareHouseDevices, getListWareHouses

base_url = "http://velocity-analytics-open.apps.op.acp.adeo.com/index.php?"
token = "8b44ade2c46279b0b4678356b7241803"
warehouses = []


# http://velocity-analytics-open.apps.op.acp.adeo.com/index.php?date=today&expanded=1&filter_limit=-1&format=JSON&idSite=1&method=Events.getAction&module=API&period=day&token_auth=anonymous&segment=city==Evry
# http://velocity-analytics-open.apps.op.acp.adeo.com/index.php?date=today&expanded=1&filter_limit=-1&format=JSON&idSite=1&method=UserCountry.getCity&module=API&period=day&token_auth=anonymous
# http://velocity-analytics-open.apps.op.acp.adeo.com/index.php?date=today&expanded=1&filter_limit=-1&format=JSON&idSite=1&method=Events.getAction&module=API&period=day&token_auth=anonymous&segment=city==Evry


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


def getActionsByWarehouse(site):
    params = dict()
    params['segment'] = 'city==' + site
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


def geCountScansByWarehouse(numsite=None):
    # ['actions]['onScan']['nb_events']
    if numsite is None:
        return getCountScans()['onScan']['nb_events']
    else:
        if numsite not in list(warehouses.keys()):
            return 0
        if 'onScan' not in warehouses[str(numsite)]['actions'].keys():
            return 0
        return warehouses[str(numsite)]['actions']['onScan']['nb_events']


def getCountScans(params=None):
    cols = ('nb_uniq_visitors', 'nb_events')
    params = dict()
    response = basicMatomoRequest(method="Events.getAction", query=params)
    if response.status_code == 200:
        list_of_data_to_display = dict()
        value = dict()
        for k in cols:
            value[k] = 0
        list_of_data_to_display['onScan'] = value
        for data in response.json():
            value = dict()
            if 'label' in data.keys():
                for k in cols:
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


def getListCity():
    whs = dict(zip(getListWareHouses().values(), getListWareHouses().keys()))
    params = dict()
    params['period'] = 'year'
    response = basicMatomoRequest(method=" UserCountry.getCity", query=params)
    if response.status_code == 200:
        list_of_data_to_display = dict()
        for data in response.json():
            value = dict()
            for k in ('city_name', 'nb_actions'):
                value[k] = data[k]
            ville = unidecode.unidecode(value['city_name'])
            value['actions'] = getActionsByWarehouse(value['city_name'])
            if 'segment' in list(data.keys()):
                value['segment'] = data['segment'].split(';')[0]
                list_of_data_to_display[whs[ville]] = value
            else:
                value['segment'] = data['label']
        global warehouses
        warehouses = list_of_data_to_display
        return warehouses
        raise


if __name__ == "__main__":
    getWareHouseDevices()
    getListCity()
    for site in list(warehouses):
        print(f"Site Numero {site}\t- Nombre de Scans : {str(geCountScansByWarehouse(site))}")
    print(f"Tous \t\t\t- Nombre de Scans : {str(geCountScansByWarehouse())}")
