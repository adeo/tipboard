import time

from src.sensors.matomo_utils import getDevices, valueFromTypeAction, valueFromAction
from src.sensors.utils import end, sendDataToTipboard
from src.tipboard.app.properties import COLOR_TAB


def updateNormChartTipBoard(bench, tile, isTest=False):
    if "values" not in bench[0]:
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
    data = {'items': list}
    tipboardAnswer = sendDataToTipboard(data=data, tile_template='listing', tile_id=tile, isTest=isTest)
    end(title=f'{tile} -> {tile}', start_time=time.time(), tipboardAnswer=tipboardAnswer, TILE_ID=tile)


def updateCPUTipBoard(isTest=False):
    print(f'CPU function')
    cpu_bench = valueFromTypeAction(["ackleyBenchmark", "bealeBenchmark", "xinSheBenchmark", "facteurPremierBenchmark"])
    print(f'CPU = {cpu_bench}')
    updateNormChartTipBoard(cpu_bench, 'cpu', isTest)
    listing = [
        bench["device"] + " avg: " + str("{0:.2f}".format(bench["avg"]))
        for bench in sorted(cpu_bench, key=lambda i: i['avg'])
    ]
    updateListingTipBoard(listing, 'cpu_list', isTest)


def updateGPUTipBoard(isTest=False):
    print(f'GPU function')
    gpu_bench = valueFromTypeAction(["scroll", "buildParagraph", "bitmapGetPixelsBenchmark", "bitmapGetPixelBenchmark"])
    # print(f'GPU = {gpu_bench}')
    updateNormChartTipBoard(gpu_bench, 'gpu', isTest)
    listing = [
        bench["device"] + " avg: " + str("{0:.2f}".format(bench["avg"]))
        for bench in sorted(gpu_bench, key=lambda i: i['avg'])
    ]
    updateListingTipBoard(listing, 'gpu_list', isTest)


def updateNetworkTipBoard(isTest=False):
    print(f'Network function')
    network_bench = valueFromAction("dowloadFile")
    # print(f'network function result : {network_bench}')
    updateNormChartTipBoard(network_bench, 'network', isTest)
    listing = [
        bench["device"] + " avg: " + str("{0:.2f}".format(bench["avg"]))
        for bench in sorted(network_bench, key=lambda i: i['avg'])
    ]
    updateListingTipBoard(listing, 'network_list', isTest)


def updateDevicesTipBoard(isTest=False):
    list_of_devices = getDevices()
    print(f'devices result : {list_of_devices}')
    updateListingTipBoard(list_of_devices, 'list_devices', isTest)


def updateBatteryTipboard(isTest=False):
    battery_bench = ["Core - X4 - 9 Battery: 4400 mAh",
                     "SM - A505FN - 9 Battery: 4,000 mAh",
                     "ELE - L29 - 10 Battery: 3650 mAh",
                     "Nokia 7.2 - 9 Battery: 3,500 mAh",
                     "MAR - LX1A - 9 Battery: 3340 mAh",
                     "TC52 - 8.1 Battery: 3340 mAh",
                     "SM - A405FN - 9 Battery: 3,100 mAh",
                     "FP3 - 9 Battery: 3,000 mAh",
                     ]
    updateListingTipBoard(battery_bench, 'battery', isTest)


def sonde_bench(isTest=False):
    updateCPUTipBoard(isTest)
    updateGPUTipBoard(isTest)
    updateNetworkTipBoard(isTest)
    updateDevicesTipBoard(isTest)
    updateBatteryTipboard(isTest)
