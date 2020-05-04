import time, random
from src.sensors.utils import end, sendDataToTipboard, getTimeStr
from src.tipboard.app.properties import BACKGROUND_TAB


def executeScriptToGetData():
    """ Simulate some actions for text tile exemple """
    return {
        'title': 'Sensors title',
        'description': 'Sensors description',
        'just-value': random.randrange(0, 100)
    }


def sonde10(isTest=False):
    TILE_ID = 'jv_ex'
    print(f'{getTimeStr()} (+) Starting sensors 10', flush=True)
    start_time = time.time()
    data = executeScriptToGetData()
    meta = dict(big_value_color=BACKGROUND_TAB[random.randrange(0, 3)],
                fading_background=random.choice([False, True]))
    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, data=data, tile_template='just_value', meta=meta, isTest=isTest)
    end(title=f'sensors10 -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
