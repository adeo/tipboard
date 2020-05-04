import datetime
import requests
import pprint
import json

export = dict()


def get_store_id():
    sites = []
    a = requests.get('https://apimobility.apps.z2.acp.adeo.com/sites/', verify=False)
    b = a.json()
    for site in b['Result']:
        sites.append(site['id'])
    return sites


def get_all_devices_soti():
    a = requests.get('https://apimobility.apps.z2.acp.adeo.com/soti/devices/', verify=False)
    return a.json()


export = {'EF500R': {'Total': None,
                     'Online': None,
                     'Used': None,
                     'Back': None,
                     'Front': None,
                     'Details': {},
                     },
          'EF500': {'Total': None,
                    'Online': None,
                    'Used': None,
                    'Back': None,
                    'Front': None,
                    'Details': {},
                    },
          'TC52': {'Total': None,
                   'Online': None,
                   'Used': None,
                   'Back': None,
                   'Front': None,
                   'Details': {},
                   }
          }

sites = get_store_id()
sites.sort()

for elt in sites:
    export['EF500R']['Details'][elt] = {
        'Total': None,
        'Online': None,
        'Used': None,
        'Back': {
            'Total': None,
            'Online': None,
            'Used': None
        },
        'Front': {
            'Total': None,
            'Online': None,
            'Used': None
        }
    }

    export['EF500']['Details'][elt] = {
        'Total': None,
        'Online': None,
        'Used': None,
        'Back': {
            'Total': None,
            'Online': None,
            'Used': None
        },
        'Front': {
            'Total': None,
            'Online': None,
            'Used': None
        }
    }

    export['TC52']['Details'][elt] = {
        'Total': None,
        'Online': None,
        'Used': None,
        'Back': {
            'Total': None,
            'Online': None,
            'Used': None
        },
        'Front': {
            'Total': None,
            'Online': None,
            'Used': None
        }
    }


def get_count_by_site(sites, all_devices, export):
    for site in sites:
        count_ef500r_by_site = 0
        count_ef500r_online_by_site = 0
        count_ef500r_online_not_charging_by_site = 0
        count_ef500r_by_site_back = 0
        count_ef500r_online_by_site_back = 0
        count_ef500r_online_not_charging_by_site_back = 0
        count_ef500r_by_site_front = 0
        count_ef500r_online_by_site_front = 0
        count_ef500r_online_not_charging_by_site_front = 0
        count_ef500_by_site = 0
        count_ef500_online_by_site = 0
        count_ef500_online_not_charging_by_site = 0
        count_ef500_by_site_back = 0
        count_ef500_online_by_site_back = 0
        count_ef500_online_not_charging_by_site_back = 0
        count_ef500_by_site_front = 0
        count_ef500_online_by_site_front = 0
        count_ef500_online_not_charging_by_site_front = 0
        count_tc52_by_site = 0
        count_tc52_online_by_site = 0
        count_tc52_online_not_charging_by_site = 0
        count_tc52_by_site_back = 0
        count_tc52_online_by_site_back = 0
        count_tc52_online_not_charging_by_site_back = 0
        count_tc52_by_site_front = 0
        count_tc52_online_by_site_front = 0
        count_tc52_online_not_charging_by_site_front = 0

        for elt in all_devices['Result']:
            if elt['storeId'] == site:
                if 'EF500R' in elt['name']:
                    count_ef500r_by_site = count_ef500r_by_site + 1
                    export['EF500R']['Details'][site]['Total'] = count_ef500r_by_site
                    if '/Leroy_Merlin_France/PROD/MAGASIN/EF500R/' in elt['path']:
                        count_ef500r_by_site_back = count_ef500r_by_site_back + 1
                        export['EF500R']['Details'][site]['Back']['Total'] = count_ef500r_by_site_back
                        if elt['online']:
                            count_ef500r_online_by_site_back = count_ef500r_online_by_site_back + 1
                            export['EF500R']['Details'][site]['Back']['Online'] = count_ef500r_online_by_site_back
                            if not elt['charging']:
                                count_ef500r_online_not_charging_by_site_back = count_ef500r_online_not_charging_by_site_back + 1
                                export['EF500R']['Details'][site]['Back'][
                                    'Used'] = count_ef500r_online_not_charging_by_site_back
                    if '/Leroy_Merlin_France/PROD/MAGASIN/EF500/' in elt['path']:
                        count_ef500r_by_site_front = count_ef500r_by_site_front + 1
                        export['EF500R']['Details'][site]['Front']['Total'] = count_ef500r_by_site_front
                        if elt['online']:
                            count_ef500r_online_by_site_front = count_ef500r_online_by_site_front + 1
                            export['EF500R']['Details'][site]['Front']['Online'] = count_ef500r_online_by_site_front
                            if not elt['charging']:
                                count_ef500r_online_not_charging_by_site_front = count_ef500r_online_not_charging_by_site_front + 1
                                export['EF500R']['Details'][site]['Front'][
                                    'Used'] = count_ef500r_online_not_charging_by_site_front
                    if elt['online']:
                        count_ef500r_online_by_site = count_ef500r_online_by_site + 1
                        export['EF500R']['Details'][site]['Online'] = count_ef500r_online_by_site
                        if not elt['charging']:
                            count_ef500r_online_not_charging_by_site = count_ef500r_online_not_charging_by_site + 1
                            export['EF500R']['Details'][site]['Used'] = count_ef500r_online_not_charging_by_site
                if 'EF500A' in elt['name']:
                    count_ef500_by_site = count_ef500_by_site + 1
                    export['EF500']['Details'][site]['Total'] = count_ef500_by_site
                    if '/Leroy_Merlin_France/PROD/MAGASIN/EF500R/' in elt['path']:
                        count_ef500_by_site_back = count_ef500_by_site_back + 1
                        export['EF500']['Details'][site]['Back']['Total'] = count_ef500_by_site_back
                        if elt['online']:
                            count_ef500_online_by_site_back = count_ef500_online_by_site_back + 1
                            export['EF500']['Details'][site]['Back']['Online'] = count_ef500_online_by_site_back
                            if not elt['charging']:
                                count_ef500_online_not_charging_by_site_back = count_ef500_online_not_charging_by_site_back + 1
                                export['EF500']['Details'][site]['Back'][
                                    'Used'] = count_ef500_online_not_charging_by_site_back
                    if '/Leroy_Merlin_France/PROD/MAGASIN/EF500/' in elt['path']:
                        count_ef500_by_site_front = count_ef500_by_site_front + 1
                        export['EF500']['Details'][site]['Front']['Total'] = count_ef500_by_site_front
                        if elt['online']:
                            count_ef500_online_by_site_front = count_ef500_online_by_site_front + 1
                            export['EF500']['Details'][site]['Front']['Online'] = count_ef500_online_by_site_front
                            if not elt['charging']:
                                count_ef500_online_not_charging_by_site_front = count_ef500_online_not_charging_by_site_front + 1
                                export['EF500']['Details'][site]['Front'][
                                    'Used'] = count_ef500_online_not_charging_by_site_front
                    if elt['online']:
                        count_ef500_online_by_site = count_ef500_online_by_site + 1
                        export['EF500']['Details'][site]['Online'] = count_ef500_online_by_site
                        if not elt['charging']:
                            count_ef500_online_not_charging_by_site = count_ef500_online_not_charging_by_site + 1
                            export['EF500']['Details'][site]['Used'] = count_ef500_online_not_charging_by_site
                if 'TC52' in elt['name']:
                    count_tc52_by_site = count_tc52_by_site + 1
                    export['TC52']['Details'][site]['Total'] = count_tc52_by_site
                    if '/Leroy_Merlin_France/PROD/MAGASIN/TC52BACK/' in elt['path']:
                        count_tc52_by_site_back = count_tc52_by_site_back + 1
                        export['TC52']['Details'][site]['Back']['Total'] = count_tc52_by_site_back
                        if elt['online']:
                            count_tc52_online_by_site_back = count_tc52_online_by_site_back + 1
                            export['TC52']['Details'][site]['Back']['Online'] = count_tc52_online_by_site_back
                            if not elt['charging']:
                                count_tc52_online_not_charging_by_site_back = count_tc52_online_not_charging_by_site_back + 1
                                export['TC52']['Details'][site]['Back'][
                                    'Used'] = count_tc52_online_not_charging_by_site_back
                    if '/Leroy_Merlin_France/PROD/MAGASIN/TC52FRONT/' in elt['path']:
                        count_tc52_by_site_front = count_tc52_by_site_front + 1
                        export['TC52']['Details'][site]['Front']['Total'] = count_tc52_by_site_front
                        if elt['online']:
                            count_tc52_online_by_site_front = count_tc52_online_by_site_front + 1
                            export['TC52']['Details'][site]['Front']['Online'] = count_tc52_online_by_site_front
                            if not elt['charging']:
                                count_tc52_online_not_charging_by_site_front = count_tc52_online_not_charging_by_site_front + 1
                                export['TC52']['Details'][site]['Front'][
                                    'Used'] = count_tc52_online_not_charging_by_site_front
                    if elt['online']:
                        count_tc52_online_by_site = count_tc52_online_by_site + 1
                        export['TC52']['Details'][site]['Online'] = count_tc52_online_by_site
                        if not elt['charging']:
                            count_tc52_online_not_charging_by_site = count_tc52_online_not_charging_by_site + 1
                            export['TC52']['Details'][site]['Used'] = count_tc52_online_not_charging_by_site
    return export


def get_global_count(all_devices, sites, export):
    count_ef500r = 0
    count_ef500r_online = 0
    count_ef500r_online_not_charging = 0
    count_ef500r_back = 0
    count_ef500r_front = 0
    count_ef500 = 0
    count_ef500_online = 0
    count_ef500_online_not_charging = 0
    count_ef500_back = 0
    count_ef500_front = 0
    count_tc52 = 0
    count_tc52_online = 0
    count_tc52_online_not_charging = 0
    count_tc52_back = 0
    count_tc52_front = 0
    for elt in all_devices['Result']:
        if 'EF500R' in elt['name']:
            if '/Leroy_Merlin_France/PROD/MAGASIN/' in elt['path']:
                count_ef500r = count_ef500r + 1
                export['EF500R']['Total'] = count_ef500r
                if '/Leroy_Merlin_France/PROD/MAGASIN/EF500R/' in elt['path']:
                    count_ef500r_back = count_ef500r_back + 1
                    export['EF500R']['Back'] = count_ef500r_back
                if '/Leroy_Merlin_France/PROD/MAGASIN/EF500/' in elt['path']:
                    count_ef500r_front = count_ef500r_front + 1
                    export['EF500R']['Front'] = count_ef500r_front
                if elt['online']:
                    count_ef500r_online = count_ef500r_online + 1
                    export['EF500R']['Online'] = count_ef500r_online
                    if not elt['charging']:
                        count_ef500r_online_not_charging = count_ef500r_online_not_charging + 1
                        export['EF500R']['Used'] = count_ef500r_online_not_charging
        if 'EF500A' in elt['name']:
            if '/Leroy_Merlin_France/PROD/MAGASIN/' in elt['path']:
                count_ef500 = count_ef500 + 1
                export['EF500']['Total'] = count_ef500
                if '/Leroy_Merlin_France/PROD/MAGASIN/EF500R/' in elt['path']:
                    count_ef500_back = count_ef500_back + 1
                    export['EF500']['Back'] = count_ef500_back
                if '/Leroy_Merlin_France/PROD/MAGASIN/EF500/' in elt['path']:
                    count_ef500_front = count_ef500_front + 1
                    export['EF500']['Front'] = count_ef500_front
                if elt['online']:
                    count_ef500_online = count_ef500_online + 1
                    export['EF500']['Online'] = count_ef500_online
                    if not elt['charging']:
                        count_ef500_online_not_charging = count_ef500_online_not_charging + 1
                        export['EF500']['Used'] = count_ef500_online_not_charging
        if 'TC52' in elt['name']:
            if '/Leroy_Merlin_France/PROD/MAGASIN/' in elt['path']:
                count_tc52 = count_tc52 + 1
                export['TC52']['Total'] = count_tc52
                if '/Leroy_Merlin_France/PROD/MAGASIN/TC52BACK/' in elt['path']:
                    count_tc52_back = count_tc52_back + 1
                    export['TC52']['Back'] = count_tc52_back
                if '/Leroy_Merlin_France/PROD/MAGASIN/TC52FRONT/' in elt['path']:
                    count_tc52_front = count_tc52_front + 1
                    export['TC52']['Front'] = count_tc52_front
                if elt['online']:
                    count_tc52_online = count_tc52_online + 1
                    export['TC52']['Online'] = count_tc52_online
                    if not elt['charging']:
                        count_tc52_online_not_charging = count_tc52_online_not_charging + 1
                        export['TC52']['Used'] = count_tc52_online_not_charging
    b = get_count_by_site(sites, all_devices, export)
    return b


all_devices = get_all_devices_soti()
a = get_global_count(all_devices, sites, export)

pprint.pprint(a)

today = datetime.datetime.now()
day = today.strftime("%B-%d-%Y-%H-%M")

with open('D:\Drive partagés\LMFR-RUN MCO DTP\Indicateurs\Mobility\export_stores_' + day + '.json', 'w') as fp:
    json.dump(a, fp)
