import time

from src.sensors.matomo_utils import getUsersConnected, getMatomoActions
from src.sensors.utils import end, sendDataToTipboard
from src.tipboard.app.properties import COLOR_TAB


def updateNormChartTipBoard(bench, tile, isTest=False):
    if not "values" in bench[0]:
        return
    datasetLength = len(bench)
    data = dict()
    data['title'] = dict(display=False)
    data['datasets'] = list()
    for index in range(datasetLength):
        data['datasets'].append(
            dict(label=bench[index]["label"],
                 data=bench[index]["nb_visits"],
                 borderColor=COLOR_TAB[index]))
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='norm_chart', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateListingTipBoard(param_list, tile, isTest=False):
    data = {"items": param_list}
    print(f'Liste des users : {data}')
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateConnectedUsers(isTest=False):
    list_of_users = getUsersConnected()
    # print(list_of_users)
    updateListingTipBoard(list_of_users, 'list_connected_users', isTest)


def updateSSLError(isTest=False):
    list_of_SSL_errors = getMatomoActions("ERROR SSL")
    # print(list_of_SSL_errors)
    updateNormChartTipBoard(list_of_SSL_errors, 'SSL_errors', isTest)


def updateNbCrash(isTest=False):
    list_of_crashes = getMatomoActions("CRASH")
    # print(list_of_crashes)
    updateNormChartTipBoard(list_of_crashes, 'Crashes', isTest)


def sonde_kiosk():
    updateConnectedUsers()
    updateSSLError()
    updateNbCrash()
