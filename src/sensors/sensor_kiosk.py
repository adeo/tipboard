import random
import time

from src.sensors.matomo_utils import getUsersConnected, getMatomoActions, getProfiles, getNbUsersConnected, \
    getNbOfDevices, getMatomoActionOfTheDay
from src.sensors.utils import end, sendDataToTipboard
from src.sensors.weekly_average import sonde_matomoDayActivity
from src.tipboard.app.properties import COLOR_TAB, BACKGROUND_TAB


def updateNormChartTipBoard(bench, tile, isTest=False):
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
                 borderBackgroundColor=COLOR_TAB[index],
                 borderColor=COLOR_TAB[index]))
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


def updateBigValueTipBoard(big_value=None, value_of_the_day=None, tile="", isTest=False):
    data = {
        "title": "",
        "description": "Current Month",
        "big-value": big_value,
        "upper-left-label": "Today",
        "upper-left-value": value_of_the_day,
        "lower-left-label": "",
        "lower-left-value": "",
        "upper-right-label": "",
        "upper-right-value": "",
        "lower-right-label": "",
        "lower-right-value": ""
    }
    if big_value > 0:
        meta = dict(big_value_color=BACKGROUND_TAB[2],
                    fading_background=True)
    else:
        meta = dict(big_value_color=BACKGROUND_TAB[0],
                    fading_background=False)
    tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='big_value', isTest=isTest, meta=meta)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateListingTipBoard(param_list, tile, isTest=False):
    data = {"items": param_list}
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateLineChartTipBoard(param_list, tile, isTest=False):
    # data = buildChartUpdateRandomly(nbrLabel=5, data=None)
    data = param_list
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='line_chart', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateNbConnectedUsers(isTest=False):
    list_of_users = getNbUsersConnected()
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
    list_of_SSL_errors_today = getMatomoActionOfTheDay("ERROR SSL")
    # Faire un updateBigValueTipBoard et envoyer les 2 datas + action
    updateBigValueTipBoard(list_of_SSL_errors[0]["nb_visits"],
                           list_of_SSL_errors_today[0]["nb_visits"],
                           "SSL_errors",
                           isTest)
    # updateJustValueTipBoard(list_of_SSL_errors, 'SSL_errors', isTest)


def updateNbCrash(isTest=False):
    list_of_crashes = getMatomoActions("CRASH")
    list_of_crashes_today = getMatomoActionOfTheDay("CRASH")
    # Faire un updateBigValueTipBoard et envoyer les 2 datas + action
    updateBigValueTipBoard(list_of_crashes[0]["nb_visits"],
                           list_of_crashes_today[0]["nb_visits"],
                           "Crashes",
                           isTest)
    # updateJustValueTipBoard(list_of_crashes, 'Crashes', isTest)


def updateLoadedProfiles(isTest=False):
    list_of_profiles = getProfiles()
    updateListingTipBoard(list_of_profiles, 'list_loaded_profiles', isTest)


def updateNbOfDevices(isTest=False):
    nb_of_devices = getNbOfDevices()
    data = {
        'title': "",
        'description': "",
        'just-value': nb_of_devices
    }
    tile = "nb_of_Devices"
    meta = dict(big_value_color=BACKGROUND_TAB[1],
                fading_background=False)
    tipboardAnswer = sendDataToTipboard(tile_id=tile, data=data, tile_template='just_value', meta=meta, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def sonde_kiosk():
    updateNbConnectedUsers()
    updateSSLError()
    updateNbCrash()
    updateLoadedProfiles()
    updateNbOfDevices()
    sonde_matomoDayActivity()
