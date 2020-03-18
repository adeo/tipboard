import random
import time

from src.sensors.soti_utils import getDevicesAllWareHouse
from src.sensors.utils import end, sendDataToTipboard, getTimeStr, buildChartUpdateRandomly
from src.tipboard.app.properties import BACKGROUND_TAB

def updateAllDeviceCount():
    """ Simulate some actions for text tile exemple """
    return {
        'title': 'Nbre Terminal',
        'description': 'Nombre de terminaux sur tous les entrepots',
        'just-value': getDevicesAllWareHouse()
    }

def updateDeviceAllOnline():
    """ Simulate some actions for text tile exemple """
    labelLenght = random.randrange(2, 8)
    datasetLength = random.randrange(1, 3)
    if labelLenght % 2 != 0:
        datasetLength = 1
    data = dict()
    data['title'] = dict(text=f'{datasetLength} dataset', color='#FFFFFF', display=random.choice([True, False]))
    data['legend'] = dict(display=False if labelLenght > 6 else random.choice([True, False]))
    data['labels'] = [f'Serie {i + 1}' for i in range(labelLenght)]
    data['datasets'] = list()
    for _ in range(datasetLength):
        data['datasets'].append(
            dict(data=[random.randrange(100, 1000) for _ in range(labelLenght)], backgroundColor=COLOR_TAB))
    print(f'{getTimeStr()} (+) Generated {datasetLength} datasets with labels [{data["labels"]}]', flush=True)
    return data

def sonde1(isTest=False):
    TILE_ID = 'bv_alldevices'
    print(f'{getTimeStr()} (+) Starting sensors 1', flush=True)
    start_time = time.time()
    data = 100
    meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)],
                fading_background=random.choice([False, True]))

    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, data=data, tile_template='just_value', meta=meta, isTest=isTest)
    end(title=f'sensors1 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)


def sonde2(isTest=False):
    TILE_ID = 'half_doughnut_online'
    print(f'{getTimeStr()} (+) Starting sensors 17', flush=True)
    start_time = time.time()
    data = buildChartUpdateRandomly(nbrDataset=random.randrange(1, 3), colorTabIndataset=True)
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='half_doughnut_chart', tile_id=TILE_ID, isTest=isTest)
    end(title=f'sensors17 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)



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
