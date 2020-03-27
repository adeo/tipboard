# coding: utf-8

import re
import requests
from src.sensors.utils import getTimeStr

# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes
base_url = "http://api-preprod.mobile.leroymerlin.fr/soti/devices/?"
devices = []
models = []
wareHouses = []


def basicSotiRequest(query=None):
    if query is None:
        query = {}
    params = dict()
    params["filter"] = "path[/Leroy_Merlin_France/PROD/ENTREPOT]"
    params.update(query)
    return requests.get(base_url, params=params, verify=False)


def getWareHouseDevices():
    params = dict()
    response = basicSotiRequest(query=params)
    p = re.compile('^.*/[0,4]00_.*$')
    if response.status_code == 200:
        list_of_devices = []
        json_response = response.json()
        for data in json_response['Result']:
            if not p.match(data['path']) and 'Fake' not in data['path']:
                q = re.compile('^.*/([0-9]{3})_-_(.*)$')
                if q.match(data['path']):
                    m = q.search(data['path'])
                    list_of_devices.append(
                        {
                            'serial': data['serial'],
                            'model': data['model'],
                            'online': data['online'],
                            'lastContact': data['lastContact'],
                            'lastContactUnix': data['lastContactUnix'],
                            'num': m.group(1),
                            'nom': m.group(2).replace('_', ' ')

                        })
        return list_of_devices
    raise


def getAllDevicesOnLine():
    data = dict()
    onLine = 0
    offline = 0
    for device in devices:
        if device['online'] == True:
            onLine += 1
        else:
            offline += 1
    data['online'] = onLine
    data['offline'] = offline
    return data


def getAllDevicesByModel():
    return getCountFilter('model')


def getDevicesAllWareHouse():
    return devices.__len__()
    raise


def getCountDevicesByWareHouse():
    return sortedDict(getCountFilter('nom'))


def getCountFilter(colname):
    data = dict()
    for device in devices:
        col = device[colname]
        if col in data:
            data[col] = data[col] + 1
        else:
            data[col] = 1
    return data


def sortedDict(data):
    result = dict()
    for element in sorted(data.keys()):
        result[element] = data[element]
    return result


def getListWareHouses():
    return wareHouses


def listeData(listDevices):
    for data in listDevices:
        print(data)


def getDevices():
    print(f'{getTimeStr()} (+) Generate list of Device')
    global devices
    devices = getWareHouseDevices()


# devices = getWareHouseDevices()
# devicesByWareHouse = getWareHouseDevices()
#getDevices()

if __name__ == "__main__":
    print("__main__")
    #getDevices
    print(devices)
    # listeData(devices)
    # print(getDevicesAllWareHouse())
    # print(getCountDevicesByWareHouse())
    # print(getAllDevicesByModel())
    # print(getCountDevicesByWareHouse())
