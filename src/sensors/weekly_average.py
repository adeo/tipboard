# -*- coding: utf-8 -*-
import datetime, requests, time
from src.tipboard.app.utils import getTimeStr
from src.sensors.utils import end, sendDataToTipboard

NB_DAYS = 7
NB_HOURS = 24

# Here we set the range and then its automaticated generated inside the tile's labels
START_HOUR = 4
END_HOUR = 21

MATOMO_URL = "http://analytics-kiosk.apps.op.acp.adeo.com/"
token = "b327b86aed12fd5a3023363d421f29a2"


# We want to have the average actions done per hour on a week period
def getAverageWeek(week):
    indexHour = 0
    averageWeek = list()
    timeHour = 0
    # Go through hours
    while indexHour < len(week[0]):
        indexDay = 0
        averageActions = 0
        # Go through days to get actions per hour per day
        while indexDay < len(week):
            hour = week[indexDay][indexHour]
            averageActions = averageActions + hour[1]
            timeHour = hour[0]
            indexDay = indexDay + 1
        # Divide nb of actions by nb of days
        # for hour " + str(indexHour) + " is: " + str(averageActions) + " / " + str(len(week)) + " = " + str(
        # averageActions / len(week)))
        averageActions = averageActions / len(week)
        averageWeek.append(averageActions)
        indexHour = indexHour + 1
    return averageWeek


def getInfosForWeek():
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(days=1)
    rcx = 0
    indexRes = 0
    res = list()
    while rcx < NB_DAYS:
        dayOfWeek = (yesterday - timedelta(days=rcx)).weekday()
        day = (yesterday - timedelta(days=rcx)).strftime('%Y-%m-%d')
        if dayOfWeek is not 6:  # not sunday i guess
            resme = getInfosForDay(day)
            res.append(list())
            if not resme:
                for hour in range(0, 24):
                    resme.append({'label': hour,
                                  'nb_uniq_visitors': 0,
                                  'nb_visits': 0,
                                  'nb_actions': 0,
                                  'nb_users': 0,
                                  'max_actions': 0,
                                  'sum_visit_length': 0,
                                  'bounce_count': 0,
                                  'nb_visits_converted': 0,
                                  'segment': 'visitLocalHour==' + str(hour)
                                  })
            if resme is not None:
                index = 0
                actions = 0
                while index < NB_HOURS:
                    # We want infos between 4h00 and 21h00
                    try:
                        hour = resme[index]
                    except:
                        hour = None
                    if START_HOUR <= index <= END_HOUR and hour is not None:
                        res[indexRes].append([index, hour.get('nb_actions')])
                        actions = actions + hour.get('nb_actions')
                        # " actions for day " + day + " at hour " + str(index) + "h")
                    index = index + 1
                indexRes = indexRes + 1
            else:
                print("(-) Infos for: " + day)
        rcx = rcx + 1
    try:
        return getAverageWeek(res)
    except:
        return None


def getInfosForDay(day):
    MATOMO_SITE_ID = 1
    resme = None
    params = dict()
    params['token_auth'] = token
    params['module'] = "API"
    params['method'] = "VisitTime.getVisitInformationPerLocalTime"
    params["period"] = "day"
    params["date"] = day
    params["format"] = "JSON"
    params["idSite"] = "2"
    try:
        resme = requests.get(MATOMO_URL, params=params, verify=False).json()
    except IOError:
        print("(-) Matomo error while retrieving " + day + " data")
    return resme


def getInfosForToday():
    resme = getInfosForDay("today")
    rcx = 0
    visitors = 0
    visits = 0
    actions = 0
    today = list()
    now = datetime.datetime.now()
    if resme is not None:
        while rcx < len(resme):
            try:
                hour = resme[rcx]
                visitors = visitors + hour.get('nb_uniq_visitors')
                visits = visits + hour.get('nb_visits')
                actions = actions + hour.get('nb_actions')
                # We want infos between 6h00 and 21h00
                if START_HOUR <= rcx <= END_HOUR and now.hour is not rcx:
                    today.append(hour.get('nb_actions'))
                    # actions for today at hour " + str(rcx) + "h")
            except:
                today.append(0)
            rcx = rcx + 1
    else:
        print("(-) Matomo non contactable")
        return None
    return today


def executeScript():
    datasets = dict()
    # Get average actions / hour for last week including yesterday but not Sundays between 6h and 21h
    datasets['averageWeek'] = getInfosForWeek()
    # Get actions / hout for today between 6h and 21h
    datasets['today'] = getInfosForToday()
    if not datasets['today']:
        datasets['today'] = []
    if not datasets['averageWeek']:
        datasets['averageWeek'] = []
    labels = list()
    for x in range(START_HOUR, END_HOUR + 1):
        labels.append(x)
    data = {
        'title': {'text': f'Numbers of Actions: {START_HOUR}h <-> {END_HOUR}h', 'color': '#FFFFFF', 'display': True},
        'legend': {'display': False},
        'labels': labels,
        # X-axis
        'datasets': [
            {
                'label': 'Moyenne',
                'data': datasets["averageWeek"],  # values
                'backgroundColor': 'rgba(66, 165, 245, 0.8)',
                'borderColor': 'rgba(66, 165, 245, 0.8)'
            },
            {
                'label': "Aujourd'hui",
                'data': datasets["today"],  # values
                'backgroundColor': 'rgba(114, 191, 68, 0.8)',
                'borderColor': 'rgba(114, 191, 68, 0.8)'
            }
        ]}
    return data


def sonde_matomoDayActivity(isTest=False):
    start_time = time.time()
    TILE_ID = 'average_use'
    data = executeScript()
    tipboardAnswer = sendDataToTipboard(tile_id=TILE_ID, tile_template='line_chart', isTest=isTest, data=data)
    end(title=f'{TILE_ID} -> {TILE_ID}', start_time=start_time, tipboardAnswer=tipboardAnswer, TILE_ID=TILE_ID)
