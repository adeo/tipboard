# coding: utf-8

import re

import requests

# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes
base_url = "http://api-preprod.mobile.leroymerlin.fr/soti/devices/?"


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
            if not p.match(data['path']):
                print(data['path'])
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
                            'nom': m.group(2)

                        })
        return list_of_devices
    raise


def getDevicesAllWareHouse():
    return devices.__len__()
    raise


def getCountDevicesByWareHouse():
    models = []
    list_of_data_to_display = {}
    for device in devices:
        # {'num': 000 , 'nom' : '' devices : [] , models : [{ 'TC8000' : 10 }]}
        if device['model'] not in models:
            models.append(device['model'])
        list_of_data_to_display.setdefault(device['num'], []).append(device)
    return list_of_data_to_display


def listeData(listDevices):
    for data in listDevices:
        print(data)


if __name__ == "__main__":
    devices = getWareHouseDevices()
    # listeData(devices)
    print(getDevicesAllWareHouse())
    print(getCountDevicesByWareHouse())
