import random
import time

from src.sensors.matomo_utils import getUsersConnected, getMatomoActions, getProfiles, getNbUsersConnected
from src.sensors.utils import end, sendDataToTipboard
from src.tipboard.app.properties import COLOR_TAB, BACKGROUND_TAB


def updateNormChartTipBoard(bench, tile, isTest=False):
    print(bench)
    if not "label" in bench[0]:
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
    print(f'🧐 data sent to Tipboard : {data}')
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='norm_chart', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateJustValueTipBoard(bench, tile, isTest=False):
    data = {
        'title': "",
        'description': "",
        'just-value': bench[0]["nb_visits"]
    }
    meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)],
                fading_background=False)
    tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='just_value', meta=meta, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateListingTipBoard(param_list, tile, isTest=False):
    data = {"items": param_list}
    # print(f'Liste des users : {data}')
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateNbConnectedUsers(isTest=False):
    list_of_users = getNbUsersConnected()
    # print(list_of_users)
    # updateJustValueTipBoard(list_of_users, 'list_connected_users', isTest)
    # Pour l'instant on part sur un mode dégradé
    data = {
        'title': "",
        'description': "",
        'just-value': list_of_users[0]
    }
    tile = "list_connected_users"
    meta = dict(big_value_color=BACKGROUND_TAB[0],
                fading_background=False)
    tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='just_value', meta=meta, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateSSLError(isTest=False):
    list_of_SSL_errors = getMatomoActions("ERROR SSL")
    # print(list_of_SSL_errors)
    updateJustValueTipBoard(list_of_SSL_errors, 'SSL_errors', isTest)


def updateNbCrash(isTest=False):
    list_of_crashes = getMatomoActions("CRASH")
    # print(list_of_crashes)
    updateJustValueTipBoard(list_of_crashes, 'Crashes', isTest)


def updateLoadedProfiles(isTest=False):
    list_of_profiles = getProfiles()
    # print(f'Liste des profils : {list_of_profiles}')
    updateListingTipBoard(list_of_profiles, 'list_loaded_profiles', isTest)


def sonde_kiosk():
    updateNbConnectedUsers()
    updateSSLError()
    updateNbCrash()
    updateLoadedProfiles()
