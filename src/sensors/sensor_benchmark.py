import time

from src.sensors.matomo_utils import valueFromAction, getDevices
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
            dict(label=bench[index]["device"],
                 data=bench[index]["values"],
                 borderColor=COLOR_TAB[index]))
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='norm_chart', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateListingTipBoard(list, tile, isTest=False):
    data = {"items": list}
    # print(f'Liste des devices testés : {data}')
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateCPUTipBoard(isTest=False):
    cpu_bench = valueFromAction("ackleyBenchmark")
    updateNormChartTipBoard(cpu_bench, 'cpu', isTest)


def updateGPUTipBoard(isTest=False):
    gpu_bench = valueFromAction("scroll")
    updateNormChartTipBoard(gpu_bench, 'gpu', isTest)


def updateNetworkTipBoard(isTest=False):
    network_bench = valueFromAction("dowloadFile")
    updateNormChartTipBoard(network_bench, 'network', isTest)


def updateDevicesTipBoard(isTest=False):
    list_of_devices = getDevices()
    updateListingTipBoard(list_of_devices, 'list_devices', isTest)


def sonde_bench(isTest=False):
    updateCPUTipBoard(isTest)  # OK
    updateGPUTipBoard(isTest)  # OK
    updateNetworkTipBoard(isTest)  # OK
    updateDevicesTipBoard(isTest)
