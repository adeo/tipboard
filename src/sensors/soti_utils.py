# coding: utf-8

import re

import requests

from src.sensors.utils import getTimeStr

# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes
base_url = "http://api-preprod.mobile.leroymerlin.fr/soti/devices/?"
devices = []
storedevices = []
storemodels = []
storepaths = []
models = []
wareHouses = []


def basicSotiRequest(query=None):
    if query is None:
        query = {}
    params = dict()
    params["filter"] = "path[/Leroy_Merlin_France/PROD/ENTREPOT]"
    params.update(query)
    return requests.get(base_url, params=params, verify=False)


def basicSotiRequestStore(query=None):
    # filter=path[/Leroy_Merlin_France/PROD/MAGASIN]&filter=online[true]&filter=charging[false]&filter=model[EF500;TC52]
    if query is None:
        query = {}
    params = dict()
    params["filter"] = ["path[/Leroy_Merlin_France/PROD/MAGASIN]"]
    params.update(query)
    return requests.get(base_url, params=params, verify=False)


def getStoreDevices():
    params = dict()
    response = basicSotiRequestStore(query=params)
    p = re.compile('^.*/[0,4]00_.*$')
    if response.status_code == 200:
        list_of_devices = []
        json_response = response.json()
        for data in json_response['Result']:
            if not p.match(data['path']) and 'Fake' not in data['path'] and '999' not in data['storeId']:
                q = re.compile('^/Leroy_Merlin_France/PROD/MAGASIN/(.*)/([0-9]{3})_-_(.*)$')
                if q.match(data['path']):
                    m = q.search(data['path'])
                    if data['serial'].startswith('EF500R'):
                        data['model'] = 'EF500R'
                    if not data['model'] in storemodels:
                        storemodels.append(data['model'])
                    if not m.group(1) in storepaths:
                        storepaths.append(m.group(1))

                    list_of_devices.append(
                        {
                            'serial': data['serial'],
                            'model': data['model'],
                            'online': data['online'],
                            'charging': data['charging'],
                            'lastContact': data['lastContact'],
                            'lastContactUnix': data['lastContactUnix'],
                            'num': m.group(2),
                            'nom': m.group(3).replace('_', ' '),
                            'path': m.group(1),

                        })
        return list_of_devices
    raise


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


def getAllInfoDevices(devicelist, colname='path', parses=storepaths):
    data = dict()
    for item in parses:
        o = dict()
        o['online'] = []
        o['offline'] = []
        o['used'] = []
        o['unUsed'] = []
        data[item] = o
    data['result'] = o

    for device in devicelist:
        if device[colname] in parses:
            if device['online']:
                data['result']['online'].append(device)
                data[device[colname]]['online'].append(device)
            else:
                data['result']['offline'].append(device)
                data[device[colname]]['offline'].append(device)

            if device['online'] and not device['charging']:
                data['result']['used'].append(device)
                data[device[colname]]['used'].append(device)
            else:
                data['result']['unUsed'].append(device)
                data[device[colname]]['unUsed'].append(device)
    return data


def getAllDevicesByModel():
    return getCountFilter('model')


def getDevicesAllWareHouse():
    return devices.__len__()
    raise


def getStoreDeviceUsedByPath(path):
    o = dict()
    result = dict()
    data = getAllInfoDevices(storedevices, 'path', storepaths)
    o['total'] = 0
    for item in data['result'].keys():
        o[item] = 0
    result['result'] = o

    for i in path:
        v = dict()
        v['total'] = 0
        for item in data[i].keys():
            v[item] = data[i][item].__len__()
            result['result'][item] = v[item] + result['result'][item]
        v['total'] = v['online'] + v['offline']
        result[i] = v
    result['result']['total'] = result['result']['online'] + result['result']['offline']
    return result
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
    print(f'{getTimeStr()} (+) Generate list Devices of WareHouse')
    global devices
    devices = getWareHouseDevices()

def getStoresDevices():
    print(f'{getTimeStr()} (+) Generate list Devices of Stores')
    global storedevices
    storedevices = getDevicesStore()

def getDevicesStore():
    print(f'{getTimeStr()} (+) Generate list Devices of Store')
    global storedevices
    global storemodels
    storedevices = getStoreDevices()


def getDevicesAllStores():
    return storedevices.__len__()
    raise


# devices = getWareHouseDevices()
# devicesByWareHouse = getWareHouseDevices()
# getDevices()

if __name__ == "__main__":
    print("__main__")
    # getDevices
    getDevicesStore()
    # print(getAllInfoDevices(storedevices , 'path' ,['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT']))
    result=getStoreDeviceUsedByPath(['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    print(result)
    # listeData(devices)
    # print(getDevicesAllWareHouse())
    # print(getCountDevicesByWareHouse())
    # print(getAllDevicesByModel())
    # print(getCountDevicesByWareHouse())
