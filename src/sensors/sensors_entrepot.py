# coding: utf-8
import os
import threading
from pathlib import Path

import time
import yaml

from src.sensors.matomo_utils import getListCity
from src.sensors.soti_utils import getWareHouseDeviceUsedByModel, getWareHouseDevices, getListWareHouses
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, poolProcessing, waitFinishPool
from src.tipboard.app.properties import BACKGROUND_TAB, COLOR_TAB, user_config_dir

models = ['TC8000', 'WT6000', 'TC52']


#################################################################################################################

def getWarehouseByDeviceBv(dataset, num=None, name=None):
    title = f'{name} - {num}'
    if num is None:
        title = 'Tous les Entrepôts'

    bv = dataset['result']['total']
    ulv = dataset['TC8000']['total']
    llv = dataset['WT6000']['total']
    urv = dataset['TC52']['total']
    lrv = ''

    return {
        'title': title,
        'description': 'Quantité et répartition des terminaux par usage',
        'big-value': str(bv),
        'upper-left-label': 'TC8000',
        'upper-left-value': str(ulv),
        'lower-left-label': 'WT6000',
        'lower-left-value': str(llv),
        'upper-right-label': 'TC52',
        'upper-right-value': str(urv),
        'lower-right-label': '',
        'lower-right-value': str(lrv)
    }


def sondeWareHouseByDevices(num=None, name=None, isTest=False, meta=None, dataset=None):
    TILE_ID = 'bv_wh_bydevices'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'

    data = getWarehouseByDeviceBv(dataset, num=num, name=name)
    push_big_value(num, TILE_ID, data, meta, 'big_value', isTest)


#####################################################################################################################


def getWareHouseScanCount(num=None, name=None, citylist=None):
    description = f"Nombre de scans sur l'entrepôt {name} - {num}"
    if num is None:
        description = 'Nombre de scans sur tous les entrepots'
        value = citylist['ALL']['actions']['onScan']['nb_events']
    else:
        if num not in list(citylist.keys()):
            value = 0
        elif 'onScan' not in citylist[str(num)]['actions'].keys():
            value = 0
        else:
            value = citylist[str(num)]['actions']['onScan']['nb_events']

    # value = str(geCountScansByWarehouse(num))

    return {
        'title': '',
        'description': description,
        'just-value': value
    }


def sondeWareHouseScanCount(num=None, name=None, isTest=False, meta=None, citylist=None):
    TILE_ID = 'jv_whs_scans'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'
    data = getWareHouseScanCount(num, name, citylist)
    push_big_value(num, TILE_ID, data, meta, 'just_value', isTest)


#####################################################################################################################

def getWareHouseNetworkStatus(dataset, num=None, name=None):
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


def sondeWareHouseNetworkStatus(num=None, name=None, isTest=False, meta=None, dataset=None):
    TILE_ID = 'hd_online_wh'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'

    data = getWareHouseNetworkStatus(dataset=dataset, num=num, name=name)
    push_big_value(num, TILE_ID, data, meta, 'half_doughnut_chart', isTest)


#####################################################################################################################
def getWareHouseUsedStatus(dataset, num=None, name=None):
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


def sondeWareHouseUsedStatus(num=None, name=None, isTest=False, meta=None, dataset=None):
    TILE_ID = 'hd_wh_device_used'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'
    data = getWareHouseUsedStatus(dataset=dataset, num=num, name=name)
    push_big_value(num, TILE_ID, data, meta, 'half_doughnut_chart', isTest)


#####################################################################################################################

def getWareHouseDeviceNetWorkUsed(dataset, num=None, name=None):
    ulv = dataset['result']['online']
    llv = dataset['result']['offline']
    urv = dataset['result']['used']
    lrv = dataset['result']['unUsed']
    return {
        'title': '',
        'description': 'Information sur les TC8000 WT6000 et TC52',
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


def sondeWareHouseByNetWorkUsedByDevice(num=None, name=None, isTest=False, meta=None, dataset=None):
    TILE_ID = 'bv_wh'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'
    data = getWareHouseDeviceNetWorkUsed(dataset=dataset, num=num, name=name)
    push_big_value(num, TILE_ID, data, meta, 'big_value', isTest)


#####################################################################################################################


def getWarehouseNetworkByUsage(dataset, num=None, name=None):
    ulv = "🔼 " + str(dataset['TC8000']['online']) + " / " + str(dataset['TC8000']['offline']) + " 🔽"
    llv = "🔼 " + str(dataset['WT6000']['online']) + " / " + str(dataset['WT6000']['offline']) + " 🔽"
    urv = "🔼 " + str(dataset['TC52']['online']) + " / " + str(dataset['TC52']['offline']) + " 🔽"
    lrv = ""
    return {
        'title': '',
        'description': 'Répartition des terminaux En Ligne / Hors Ligne',
        'big-value': "🔼 " + str(dataset['result']['online']) + " / " + str(dataset['result']['offline']) + " 🔽",
        'upper-left-label': 'TC8000:',
        'upper-left-value': ulv,
        'lower-left-label': 'WT6000:',
        'lower-left-value': llv,
        'upper-right-label': 'TC52:',
        'upper-right-value': urv,
        'lower-right-label': '',
        'lower-right-value': lrv
    }


def sondeWareHouseNetWorkByUsage(num=None, name=None, isTest=False, meta=None, dataset=None):
    TILE_ID = 'bv_wh_network'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'

    data = getWarehouseNetworkByUsage(dataset=dataset, num=num, name=name)
    push_big_value(num, TILE_ID, data, meta, 'big_value', isTest)


#####################################################################################################################

def getWareHouseUsedByUsage(dataset, num=None, name=None):
    ulv = "💼 " + str(dataset['TC8000']['used']) + "\t/ " + str(dataset['TC8000']['unUsed']) + " 💤"
    llv = "💼 " + str(dataset['WT6000']['used']) + "\t/ " + str(dataset['WT6000']['unUsed']) + " 💤"
    urv = "💼 " + str(dataset['TC52']['used']) + "\t/" + str(dataset['TC52']['unUsed']) + " 💤"
    lrv = ""
    return {
        'title': '',
        'description': 'Répartition des terminaux Utilisés / Libres',
        'big-value': "💼 " + str(dataset['result']['used']) + " / " + str(dataset['result']['unUsed']) + " 💤",
        'upper-left-label': 'TC8000:',
        'upper-left-value': ulv,
        'lower-left-label': 'WT6000',
        'lower-left-value': llv,
        'upper-right-label': 'TC52:',
        'upper-right-value': urv,
        'lower-right-label': '',
        'lower-right-value': lrv
    }


def sondeWareHouseUsedByUsage(num=None, name=None, isTest=False, meta=None, dataset=None):
    TILE_ID = 'bv_wh_used'
    if num is not None:
        TILE_ID = f'{TILE_ID}_{str(num)}'

    data = getWareHouseUsedByUsage(dataset=dataset, num=num, name=name)
    push_big_value(num, TILE_ID, data, meta, 'big_value', isTest)


#####################################################################################################################
def push_big_value(num, TILE_ID, data, meta, tile_template, isTest):
    if num is None:
        num = "All"
    start_time = time.time()
    print(f'{getTimeStr()} (+) Starting warehouse for sonde {TILE_ID} by device for {num}', flush=True)
    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, data=data, tile_template=tile_template, meta=meta,
                                        isTest=isTest)
    end(title=f'warehouse sonde by device {num} -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer,
        TILE_ID=TILE_ID)


#####################################################################################################################
def createWareHouse(num, name, matomolist):
    workdir = user_config_dir + "warehouse"
    Path(workdir).mkdir(parents=True, exist_ok=True)
    sitefile = workdir + "/" + num + ".yaml"
    if os.path.exists(sitefile):
        print(f'Site {num} - {name} already exists => {sitefile}')
        return
    template = user_config_dir + "/template/warehouse.yaml"

    fileset = open(template, 'rt', encoding="utf-8").read()
    stream = fileset.replace('XXX', num).replace('NNNNNNNN', name)

    yamldata = yaml.load(stream, Loader=yaml.FullLoader)
    if num not in matomolist:
        del yamldata['layout'][0]['row_1_of_2'][0]['col_1_of_2 flip-time-6'][1]
        yamldata['layout'][0]['row_1_of_2'][0]['col_1_of_2'] = yamldata['layout'][0]['row_1_of_2'][0].pop('col_1_of_2 flip-time-6')

    with open(sitefile, 'w', encoding="utf-8") as file:
        yaml.dump(yamldata, file, allow_unicode=True)


#####################################################################################################################
def sondeWarehouse():
    start_time = time.time()
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    print(f'{getTimeStr()} (+) Starting WareHouses sensors', flush=True)

    getWareHouseDevices()

    list_city = getListCity()

    matomolist = list(list_city.keys())
    warehouses = getListWareHouses()

    dataset = getWareHouseDeviceUsedByModel(num=None, path=models)
    multiSondeswarehouse(None, None, dataset, meta)

    pool = poolProcessing()
    for num, name in warehouses.items():
        pool.apply_async(wareHouseProcessing, args=(num, name, meta, matomolist))
        # wareHouseProcessing(num, name, meta, matomolist)
    waitFinishPool(start_time=start_time, pool=pool)
    print(f'{getTimeStr()} (+) Finish WareHouses sensors', flush=True)


###############################################################################################################################

def countScanallwWareHouse():
    start_time = time.time()
    print(f'{getTimeStr()} (+) Starting WareHouses scanner count sensors', flush=True)
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    list_city = getListCity()
    sondeWareHouseScanCount(num=None, name=None, citylist=list_city, meta=meta)
    for num, name in getListWareHouses().items():
        sondeWareHouseScanCount(num=num, name=name, citylist=list_city, meta=meta)
    print(f'{getTimeStr()} (+) Finish WareHouses scanner count sensors --- in {time.time() - start_time} seconds ---', flush=True)


################################################################################################################################
def wareHouseProcessing(num, name, meta, matomolist):
    createWareHouse(num, name, matomolist)
    dataset = getWareHouseDeviceUsedByModel(num=num, path=models)
    multiSondeswarehouse(num, name, dataset, meta)


###############################################################################################################################


def multiSondeswarehouse(num, name, dataset, meta):
    functions = ('sondeWareHouseByDevices', 'sondeWareHouseNetworkStatus',
                 'sondeWareHouseUsedStatus', 'sondeWareHouseByNetWorkUsedByDevice',
                 'sondeWareHouseNetWorkByUsage', 'sondeWareHouseUsedByUsage'
                 )
    threads = []
    for fct in functions:
        th = threading.Thread(target=eval(fct), kwargs={'num': num, 'name': name, 'meta': meta, 'dataset': dataset})
        threads.append(th)
        th.start()
    for t in threads:
        t.join()

    # sondeWareHouseByDevices(num=num, name=name, meta=meta, dataset=dataset)
    # sondeWareHouseNetworkStatus(num=num, name=name, meta=meta, dataset=dataset)
    # sondeWareHouseUsedStatus(num=num, name=name, meta=meta, dataset=dataset)
    # sondeWareHouseByNetWorkUsedByDevice(num=num, name=name, meta=meta, dataset=dataset)
    # sondeWareHouseNetWorkByUsage(num=num, name=name, meta=meta, dataset=dataset)
    # sondeWareHouseUsedByUsage(num=num, name=name, meta=meta, dataset=dataset)


if __name__ == "__main__":
    # sondeWarehouse()
    getWareHouseDevices()
    countScanallwWareHouse()

# def updateNormChartTipBoard(bench, tile, isTest=False):
#     if not "label" in bench[0]:
#         return
#     datasetLength = len(bench)
#     data = dict()
#     data['title'] = dict(display=False)
#     data['datasets'] = list()
#     for index in range(datasetLength):
#         data['datasets'].append(
#             dict(label=bench[index]["label"],
#                  data=bench[index]["nb_visits"],
#                  borderBackgroundColor=COLOR_TAB[index],
#                  borderColor=COLOR_TAB[index]))
#     tipboardAnswer = sendDataToTipboard(data=data, tile_template='norm_chart', tile_id=tile, isTest=isTest)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def updateJustValueTipBoard(bench, tile, isTest=False):
#     data = {
#         'title': "",
#         'description': "",
#         'just-value': bench[0]["nb_visits"]
#     }
#     meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)],
#                 fading_background=False)
#     tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='just_value', meta=meta, isTest=isTest)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def updateBigValueTipBoard(big_value=None, value_of_the_day=None, tile="", isTest=False):
#     data = {
#         "title": "",
#         "description": "Current Month",
#         "big-value": big_value,
#         "upper-left-label": "Today",
#         "upper-left-value": value_of_the_day,
#         "lower-left-label": "",
#         "lower-left-value": "",
#         "upper-right-label": "",
#         "upper-right-value": "",
#         "lower-right-label": "",
#         "lower-right-value": ""
#     }
#     if big_value > 0:
#         meta = dict(big_value_color=BACKGROUND_TAB[2],
#                     fading_background=True)
#     else:
#         meta = dict(big_value_color=BACKGROUND_TAB[0],
#                     fading_background=False)
#     tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='big_value', isTest=isTest, meta=meta)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def updateListingTipBoard(param_list, tile, isTest=False):
#     data = {"items": param_list}
#     tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=tile, isTest=isTest)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def updateLineChartTipBoard(param_list, tile, isTest=False):
#     # data = buildChartUpdateRandomly(nbrLabel=5, data=None)
#     data = param_list
#     tipboardAnswer = sendDataToTipboard(data=data, tile_template='line_chart', tile_id=tile, isTest=isTest)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def updateNbConnectedUsers(isTest=False):
#     list_of_users = getNbUsersConnected()
#     # Pour l'instant on part sur un mode dégradé
#     data = {
#         'title': "",
#         'description': "",
#         'just-value': list_of_users[0]
#     }
#     tile = "list_connected_users"
#     meta = dict(big_value_color=BACKGROUND_TAB[0],
#                 fading_background=False)
#     tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='just_value', meta=meta, isTest=isTest)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def updateSSLError(isTest=False):
#     list_of_SSL_errors = getMatomoActions("ERROR SSL")
#     list_of_SSL_errors_today = getMatomoActionOfTheDay("ERROR SSL")
#     # Faire un updateBigValueTipBoard et envoyer les 2 datas + action
#     updateBigValueTipBoard(list_of_SSL_errors[0]["nb_visits"],
#                            list_of_SSL_errors_today[0]["nb_visits"],
#                            "SSL_errors",
#                            isTest)
#     # updateJustValueTipBoard(list_of_SSL_errors, 'SSL_errors', isTest)
# def updateNbCrash(isTest=False):
#     list_of_crashes = getMatomoActions("CRASH")
#     list_of_crashes_today = getMatomoActionOfTheDay("CRASH")
#     # Faire un updateBigValueTipBoard et envoyer les 2 datas + action
#     try:
#         nb_of_crash_monthly = list_of_crashes[0]["nb_visits"]
#     except:
#         nb_of_crash_monthly = 0
#     try:
#         nb_of_crash_today = list_of_crashes_today[0]["nb_visits"]
#     except:
#         nb_of_crash_today = 0
#     updateBigValueTipBoard(nb_of_crash_monthly,
#                            nb_of_crash_today,
#                            "Crashes",
#                            isTest)
# def updateLoadedProfiles(isTest=False):
#     list_of_profiles = getProfiles()
#     updateListingTipBoard(list_of_profiles, 'list_loaded_profiles', isTest)
# def updateNbOfDevices(isTest=False):
#     nb_of_devices = getNbOfDevices()
#     data = {
#         'title': "",
#         'description': "",
#         'just-value': nb_of_devices
#     }
#     tile = "nb_of_Devices"
#     meta = dict(big_value_color=BACKGROUND_TAB[1],
#                 fading_background=False)
#     tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='just_value', meta=meta, isTest=isTest)
#     end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)
# def sonde_kiosk():
#     updateNbConnectedUsers()
#     updateSSLError()
#     updateNbCrash()
#     updateLoadedProfiles()
#     updateNbOfDevices()
#     sonde_matomoDayActivity()
