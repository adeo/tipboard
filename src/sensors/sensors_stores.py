import fileinput
import os
import time
from shutil import copyfile

import requests

from src.sensors.soti_utils import getStoreDeviceUsedByPath, getDevicesStore, getListStores
from src.sensors.utils import getTimeStr, sendDataToTipboard, end
from src.tipboard.app.properties import BACKGROUND_TAB, COLOR_TAB, user_config_dir, TIPBOARD_URL

data = dict()


def sondeStore(first=False):
    if first:
        meta=None
        print(f'{getTimeStr()} (+) Starting first execution stores sensors', flush=True)
    else:
        meta = dict(big_value_color=BACKGROUND_TAB[0],
                    fading_background=False)
        print(f'{getTimeStr()} (+) Starting stores sensors', flush=True)

    getDevicesStore()
    global data
    data = getStoreDeviceUsedByPath(path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    sondeStoresAllDevice()

    #sondeStore5()
    #sondeStore2()
    #sondeStore3()
    #sondeStore4()
    #sondeStore6()
    #sondeStore7()

    LaunchStore(meta=meta)

    sondeStoreGenerate()
    print(f'{getTimeStr()} (+) Finish stores sensors', flush=True)


def LaunchStore(meta=None):
    sondeShopByDevices(meta=meta)
    sondeShopNetworkStatus(meta=meta)
    sondeShopUsedStatus(meta=meta)
    sondeStoreByNetWorkUsedByDevice(meta=meta)
    sondeStoreNetWorkByUsage(meta=meta)
    sondeStoreUsedByUsage(meta=meta)

def getStoresAllDevice():
    return {
        'title': '',
        'description': 'Nombre de terminaux sur tous les magasins',
        'just-value': data['result']['total']
    }


def sondeStoresAllDevice(isTest=False):
    TILE_ID = 'jv_alldevices_shop'
    print(f'{getTimeStr()} (+) Starting sensors store sonde 1', flush=True)
    start_time = time.time()
    data = getStoresAllDevice()
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, data=data, tile_template='just_value', meta=meta,
                                        isTest=isTest)
    end(title=f'store sonde 1-> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def updateNetworkStatus():
    tileData = dict()
    tileData['title'] = {'display': False, 'text': 'OnLine / OffLine'}
    tileData['labels'] = ['En ligne', 'Hors ligne']
    tileData['borderColor'] = '#525252'
    tileData['legend'] = dict(display=True)
    tileData['plugins'] = dict(labels=True)
    tileData['datasets'] = list()
    tileData['datasets'].append(
        dict(label=f'OnLine',
             data=[data['result']['online'], data['result']['offline']],
             backgroundColor=[COLOR_TAB[1], COLOR_TAB[5]],
             borderColor='#525252'))
    tileData['option'] = dict()
    return tileData


def sondeStore2(isTest=False):
    TILE_ID = 'pie_chart_online_shop'
    print(f'{getTimeStr()} (+) Starting store sonde 2', flush=True)
    start_time = time.time()
    data = updateNetworkStatus()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='pie_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'store sonde 2 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def updateDevicesUSed():
    tileData = dict()
    tileData['title'] = {'display': False, 'text': 'Utilisé / Non Utilisé'}
    tileData['labels'] = ['Utilisé', 'Libre']
    tileData['borderColor'] = '#525252'
    tileData['legend'] = dict(display=True)
    tileData['plugins'] = dict(labels=True)
    tileData['datasets'] = list()
    tileData['datasets'].append(
        dict(label=f'OnLine',
             data=[data['result']['used'], data['result']['unUsed']],
             backgroundColor=[COLOR_TAB[1], COLOR_TAB[5]],
             borderColor='#525252'))
    tileData['option'] = {'label': 'false'}
    return tileData


def sondeStore3(isTest=False):
    TILE_ID = 'pie_chart_devise_used'
    print(f'{getTimeStr()} (+) Starting store sonde 3', flush=True)
    start_time = time.time()
    data = updateDevicesUSed()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='pie_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'store sonde 3 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def updateStoresDeviceBv():
    ulv = data['result']['online']
    llv = data['result']['offline']
    urv = data['result']['used']
    lrv = data['result']['unUsed']
    return {
        'title': '',
        'description': 'Information sur les EF500(R) et TC52',
        'big-value': data['result']['total'],
        'upper-left-label': 'Connectés:',
        'upper-left-value': ulv,
        'lower-left-label': 'Non Connectés:',
        'lower-left-value': llv,
        'upper-right-label': 'Utilisés:',
        'upper-right-value': urv,
        'lower-right-label': 'Non Utilisés:',
        'lower-right-value': lrv
    }


def sondeStore4(isTest=False):
    TILE_ID = 'bv_shops'
    print(f'{getTimeStr()} (+) Starting store sonde 4', flush=True)
    start_time = time.time()
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    data = updateStoresDeviceBv()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde 4 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def updateStoresByDeviceBv():
    ulv = data['EF500']['total']
    llv = data['EF500R']['total']
    urv = data['TC52FRONT']['total']
    lrv = data['TC52BACK']['total']
    return {
        'title': '',
        'description': 'Nombre de terminaux par utilisations',
        'big-value': data['result']['total'],
        'upper-left-label': 'EF500:',
        'upper-left-value': ulv,
        'lower-left-label': 'EF500R:',
        'lower-left-value': llv,
        'upper-right-label': 'TC52 Vente:',
        'upper-right-value': urv,
        'lower-right-label': 'TC52 Log:',
        'lower-right-value': lrv
    }


def sondeStore5(isTest=False):
    TILE_ID = 'bv_shops_bydevices'
    print(f'{getTimeStr()} (+) Starting store sonde 5', flush=True)
    start_time = time.time()
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    data = updateStoresByDeviceBv()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde 5 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def updateStoresByDeviceNetworkBv():
    ulv = "🔼 " + str(data['EF500']['online']) + " / " + str(data['EF500']['offline']) + " 🔽"
    llv = "🔼 " + str(data['EF500R']['online']) + " / " + str(data['EF500R']['offline']) + " 🔽"
    urv = "🔼 " + str(data['TC52FRONT']['online']) + " / " + str(data['TC52FRONT']['offline']) + " 🔽"
    lrv = "🔼 " + str(data['TC52BACK']['online']) + " / " + str(data['TC52BACK']['offline']) + " 🔽"
    return {
        'title': '',
        'description': 'Répartition des terminaux En Ligne / Hors Ligne',
        'big-value': "🔼 " + str(data['result']['online']) + " / " + str(data['result']['offline']) + " 🔽",
        'upper-left-label': 'EF500:',
        'upper-left-value': ulv,
        'lower-left-label': 'EF500R:',
        'lower-left-value': llv,
        'upper-right-label': 'TC52 Vente:',
        'upper-right-value': urv,
        'lower-right-label': 'TC52 Log:',
        'lower-right-value': lrv
    }


def sondeStore6(isTest=False):
    TILE_ID = 'bv_shops_network'
    print(f'{getTimeStr()} (+) Starting store sonde 6', flush=True)
    start_time = time.time()
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    data = updateStoresByDeviceNetworkBv()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde 6 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def updateStoresByDeviceUsedBv():
    ulv = "💼 " + str(data['EF500']['used']) + "\t/ " + str(data['EF500']['unUsed']) + " 💤"
    llv = "💼 " + str(data['EF500R']['used']) + "\t/ " + str(data['EF500R']['unUsed']) + " 💤"
    urv = "💼 " + str(data['TC52FRONT']['used']) + "\t/" + str(data['TC52FRONT']['unUsed']) + " 💤"
    lrv = "💼 " + str(data['TC52BACK']['used']) + "\t/ " + str(data['TC52BACK']['unUsed']) + " 💤"
    return {
        'title': '',
        'description': 'Répartition des terminaux Utilisés / Libres',
        'big-value': "💼 " + str(data['result']['used']) + " / " + str(data['result']['unUsed']) + " 💤",
        'upper-left-label': 'EF500:',
        'upper-left-value': ulv,
        'lower-left-label': 'EF500R:',
        'lower-left-value': llv,
        'upper-right-label': 'TC52 Vente:',
        'upper-right-value': urv,
        'lower-right-label': 'TC52 Log:',
        'lower-right-value': lrv
    }


def sondeStore7(isTest=False):
    TILE_ID = 'bv_shops_used'
    print(f'{getTimeStr()} (+) Starting store sonde 7', flush=True)
    start_time = time.time()
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    data = updateStoresByDeviceUsedBv()
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde 7 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)



#######################################################################

def getStoreUsedByUsage(num=None, name=None):
    dataset = getStoreDeviceUsedByPath(num=num, path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    ulv = "💼 " + str(dataset['EF500']['used']) + "\t/ " + str(dataset['EF500']['unUsed']) + " 💤"
    llv = "💼 " + str(dataset['EF500R']['used']) + "\t/ " + str(dataset['EF500R']['unUsed']) + " 💤"
    urv = "💼 " + str(dataset['TC52FRONT']['used']) + "\t/" + str(dataset['TC52FRONT']['unUsed']) + " 💤"
    lrv = "💼 " + str(dataset['TC52BACK']['used']) + "\t/ " + str(dataset['TC52BACK']['unUsed']) + " 💤"
    return {
        'title': '',
        'description': 'Répartition des terminaux Utilisés / Libres',
        'big-value': "💼 " + str(dataset['result']['used']) + " / " + str(dataset['result']['unUsed']) + " 💤",
        'upper-left-label': 'EF500 Vente:',
        'upper-left-value': ulv,
        'lower-left-label': 'EF500R Log:',
        'lower-left-value': llv,
        'upper-right-label': 'TC52 Vente:',
        'upper-right-value': urv,
        'lower-right-label': 'TC52 Log:',
        'lower-right-value': lrv
    }


def sondeStoreUsedByUsage(num=None, name=None, isTest=False, meta=None):
    if num is None:
        TILE_ID = 'bv_shops_used'
    else:
        TILE_ID = 'bv_shops_used_' + str(num)

    print(f'{getTimeStr()} (+) Starting store for sonde {TILE_ID} by device for {num}', flush=True)
    start_time = time.time()
    data = getStoreUsedByUsage(num,name)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde 7 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def getStoresNetworkByUsage(num=None, name=None):
    dataset = getStoreDeviceUsedByPath(num=num, path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    ulv = "🔼 " + str(dataset['EF500']['online']) + " / " + str(dataset['EF500']['offline']) + " 🔽"
    llv = "🔼 " + str(dataset['EF500R']['online']) + " / " + str(dataset['EF500R']['offline']) + " 🔽"
    urv = "🔼 " + str(dataset['TC52FRONT']['online']) + " / " + str(dataset['TC52FRONT']['offline']) + " 🔽"
    lrv = "🔼 " + str(dataset['TC52BACK']['online']) + " / " + str(dataset['TC52BACK']['offline']) + " 🔽"
    return {
        'title': '',
        'description': 'Répartition des terminaux En Ligne / Hors Ligne',
        'big-value': "🔼 " + str(dataset['result']['online']) + " / " + str(dataset['result']['offline']) + " 🔽",
        'upper-left-label': 'EF500 Vente:',
        'upper-left-value': ulv,
        'lower-left-label': 'EF500R Log:',
        'lower-left-value': llv,
        'upper-right-label': 'TC52 Vente:',
        'upper-right-value': urv,
        'lower-right-label': 'TC52 Log:',
        'lower-right-value': lrv
    }

def sondeStoreNetWorkByUsage(num=None, name=None, isTest=False, meta=None):
    if num is None:
        TILE_ID = 'bv_shops_network'
    else:
        TILE_ID = 'bv_shops_network_' + str(num)
    print(f'{getTimeStr()} (+) Starting store for sonde {TILE_ID} by device for {num}', flush=True)
    start_time = time.time()
    data = getStoresNetworkByUsage(num,name)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde for {num}-> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def getStoresDeviceNetWorkUsed(num=None, name=None):
    dataset = getStoreDeviceUsedByPath(num=num, path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    ulv = dataset['result']['online']
    llv = dataset['result']['offline']
    urv = dataset['result']['used']
    lrv = dataset['result']['unUsed']
    return {
        'title': '',
        'description': 'Information sur les EF500(R) et TC52',
        'big-value': dataset['result']['total'],
        'upper-left-label': 'Connectés:',
        'upper-left-value': ulv,
        'lower-left-label': 'Non Connectés:',
        'lower-left-value': llv,
        'upper-right-label': 'Utilisés:',
        'upper-right-value': urv,
        'lower-right-label': 'Non Utilisés:',
        'lower-right-value': lrv
    }


def sondeStoreByNetWorkUsedByDevice(num=None, name=None, isTest=False, meta=None):
    if num is None:
        TILE_ID = 'bv_shops'
    else:
        TILE_ID = 'bv_shops_' + str(num)

    print(f'{getTimeStr()} (+) Starting store for sonde {TILE_ID} by device for {num}', flush=True)
    start_time = time.time()
    data = getStoresDeviceNetWorkUsed(num, name)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store sonde -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def getStoresByDeviceBv(num=None, name=None):
    dataset = getStoreDeviceUsedByPath(num=num, path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    title = f'{name} - {num}'
    if num is None:
        title='Tous les Magasins'
    bv = dataset['result']['total']
    ulv = dataset['EF500']['total']
    llv = dataset['EF500R']['total']
    urv = dataset['TC52FRONT']['total']
    lrv = dataset['TC52BACK']['total']

    return {
        'title': title,
        'description': 'Quantité et répartition des terminaux par usage',
        'big-value': str(bv),
        'upper-left-label': 'EF500 Vente:',
        'upper-left-value': str(ulv),
        'lower-left-label': 'EF500R Log:',
        'lower-left-value': str(llv),
        'upper-right-label': 'TC52 Vente:',
        'upper-right-value': str(urv),
        'lower-right-label': 'TC52 Log:',
        'lower-right-value': str(lrv)
    }

def sondeShopByDevices(num=None, name=None, isTest=False, meta=None):
    if num is None:
        TILE_ID = 'bv_shops_bydevices'
    else:
        TILE_ID = 'bv_shops_bydevices_' + str(num)

    print(f'{getTimeStr()} (+) Starting store for sonde {TILE_ID} by device for {num}', flush=True)
    start_time = time.time()
    data = getStoresByDeviceBv(num, name)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='big_value', tile_id=TILE_ID, meta=meta, isTest=isTest)
    end(title=f'store  sonde by device {num} -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer,
        TILE_ID=TILE_ID)

def getShopUsedStatus(num=None, name=None):
    dataset = getStoreDeviceUsedByPath(num=num, path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    tileData = dict()
    tileData['title'] = {'display': False, 'text': 'Utilisé / Non Utilisé'}
    tileData['labels'] = ['Utilisé', 'Libre']
    tileData['borderColor'] = '#525252'
    tileData['legend'] = dict(display=True)
    tileData['plugins'] = dict(labels=True)
    tileData['datasets'] = list()
    tileData['datasets'].append(
        dict(label=f'OnLine',
             data=[dataset['result']['used'], dataset['result']['unUsed']],
             backgroundColor=[COLOR_TAB[1], COLOR_TAB[5]],
             borderColor='#525252'))
    tileData['option'] = {'label': 'false'}
    return tileData

def sondeShopUsedStatus(num=None, name=None, isTest=False, meta=None):
    if num is None:
        TILE_ID = 'hd_devise_used'
    else:
        TILE_ID = 'hd_devise_used_' + str(num)

    print(f'{getTimeStr()} (+) Starting store for sonde {TILE_ID} by device for {num}', flush=True)
    start_time = time.time()
    data = getShopUsedStatus(num,name)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='half_doughnut_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'store  sonde by device {num} -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer,
        TILE_ID=TILE_ID)

def getShopNetworkStatus(num=None, name=None):
    dataset = getStoreDeviceUsedByPath(num=num, path=['EF500', 'EF500R', 'TC52BACK', 'TC52FRONT'])
    tileData = dict()
    tileData['title'] = {'display': False, 'text': 'OnLine / OffLine'}
    tileData['labels'] = ['En ligne', 'Hors ligne']
    tileData['borderColor'] = '#525252'
    tileData['legend'] = dict(display=True)
    tileData['plugins'] = dict(labels=True)
    tileData['datasets'] = list()
    tileData['datasets'].append(
        dict(label=f'OnLine',
             data=[dataset['result']['online'], dataset['result']['offline']],
             backgroundColor=[COLOR_TAB[1], COLOR_TAB[5]],
             borderColor='#525252'))
    tileData['option'] = dict()
    return tileData

def sondeShopNetworkStatus(num=None, name=None, isTest=False, meta=None):
    if num is None:
        TILE_ID = 'hd_online_shop'
    else:
        TILE_ID = 'hd_online_shop_' + str(num)

    print(f'{getTimeStr()} (+) Starting store for sonde {TILE_ID} by device for {num}', flush=True)
    start_time = time.time()
    data = getShopNetworkStatus(num, name)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='half_doughnut_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'store  sonde by device {num} -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer,
        TILE_ID=TILE_ID)

def sondeStoreGenerate():
    print(f'{getTimeStr()} (+) Starting generate store', flush=True)
    stores = getListStores()
    for root, dirs, files in os.walk(user_config_dir + "store/."):
        for filename in files:
            if os.path.splitext(filename)[0] not in list(stores.keys()):
                print(f'{getTimeStr()} (+) Delete file : ' + user_config_dir + "store/" + filename, flush=True)
                os.remove(user_config_dir + "store/" + filename)

    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)

    for k, v in stores.items():
        num = str(k)
        nom = str(v)
        createStore(num, nom)
        sondeShopByDevices(num, nom, meta=meta)
        sondeShopNetworkStatus(num, nom , meta=None)
        sondeShopUsedStatus(num, nom , meta=None)
        sondeStoreByNetWorkUsedByDevice(num, nom, meta=meta)
        sondeStoreNetWorkByUsage(num, nom, meta=meta)
        sondeStoreUsedByUsage(num, nom, meta=meta)
    print(f'{getTimeStr()} (+) Finish generate store', flush=True)


def createStore(num, name):
    path = user_config_dir + "store/" + num + ".yaml"
    template = user_config_dir + "/template/store.yaml"
    first = True
    if os.path.exists(path):
        first = False

    copyfile(template, path)
    with fileinput.FileInput(path, inplace=True, backup=False) as file:
        for line in file:
            print(line.replace('XXX', num).replace('NNNNNNNN', name), end='')

    if first:
        sondeShopByDevices(num, name, meta=None)
        sondeStoreByNetWorkUsedByDevice(num, name, meta=None)
        sondeStoreNetWorkByUsage(num, name, meta=None)
        sondeStoreUsedByUsage(num, name, meta=None)

if __name__ == "__main__":
    print("__main__")
    sondeStore()
