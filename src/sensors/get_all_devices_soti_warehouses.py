import datetime
import requests
import pprint
import json

export = dict()
sites = ['000', '042', '098', '122', '136', '170', '355', '400', '430', '433', '435', '443', '447', '450', '451', '460']
"""
def get_store_id():
    sites = []
    a = requests.get('https://apimobility.apps.z2.acp.adeo.com/sites/', verify=False)
    b = a.json()
    for site in b['Result']:
        sites.append(site['id'])
    return sites
"""


def get_all_devices_soti():
    a = requests.get('https://apimobility.apps.z2.acp.adeo.com/soti/devices/', verify=False)
    return a.json()


export = {'TC8000': {'Total': None,
                     'Online': None,
                     'Used': None,
                     'Details': {},
                     },
          'WT6000': {'Total': None,
                     'Online': None,
                     'Used': None,
                     'Details': {},
                     },
          'TC52': {'Total': None,
                   'Online': None,
                   'Used': None,
                   'Details': {},
                   }
          }

# sites = get_store_id()
# sites.sort()

for elt in sites:
    export['TC8000']['Details'][elt] = {
        'Total': None,
        'Online': None,
        'Used': None
    }

    export['WT6000']['Details'][elt] = {
        'Total': None,
        'Online': None,
        'Used': None
    }

    export['TC52']['Details'][elt] = {
        'Total': None,
        'Online': None,
        'Used': None
    }


def get_count_by_site(sites, all_devices, export):
    for site in sites:
        count_tc8000_by_site = 0
        count_tc8000_online_by_site = 0
        count_tc8000_online_not_charging_by_site = 0
        count_wt6000_by_site = 0
        count_wt6000_online_by_site = 0
        count_wt6000_online_not_charging_by_site = 0
        count_tc52_by_site = 0
        count_tc52_online_by_site = 0
        count_tc52_online_not_charging_by_site = 0
        for elt in all_devices['Result']:
            if elt['storeId'] == site:
                if 'TC8000' in elt['name']:
                    count_tc8000_by_site = count_tc8000_by_site + 1
                    export['TC8000']['Details'][site]['Total'] = count_tc8000_by_site
                    if elt['online']:
                        count_tc8000_online_by_site = count_tc8000_online_by_site + 1
                        export['TC8000']['Details'][site]['Online'] = count_tc8000_online_by_site
                        if not elt['charging']:
                            count_tc8000_online_not_charging_by_site = count_tc8000_online_not_charging_by_site + 1
                            export['TC8000']['Details'][site]['Used'] = count_tc8000_online_not_charging_by_site
                if 'WT6000' in elt['name']:
                    count_wt6000_by_site = count_wt6000_by_site + 1
                    export['WT6000']['Details'][site]['Total'] = count_wt6000_by_site
                    if elt['online']:
                        count_wt6000_online_by_site = count_wt6000_online_by_site + 1
                        export['WT6000']['Details'][site]['Online'] = count_wt6000_online_by_site
                        if not elt['charging']:
                            count_wt6000_online_not_charging_by_site = count_wt6000_online_not_charging_by_site + 1
                            export['WT6000']['Details'][site]['Used'] = count_wt6000_online_not_charging_by_site
                if 'TC52' in elt['name']:
                    count_tc52_by_site = count_tc52_by_site + 1
                    export['TC52']['Details'][site]['Total'] = count_tc52_by_site
                    if elt['online']:
                        count_tc52_online_by_site = count_tc52_online_by_site + 1
                        export['TC52']['Details'][site]['Online'] = count_tc52_online_by_site
                        if not elt['charging']:
                            count_tc52_online_not_charging_by_site = count_tc52_online_not_charging_by_site + 1
                            export['TC52']['Details'][site]['Used'] = count_tc52_online_not_charging_by_site
    return export


def get_global_count(all_devices, sites, export):
    count_tc8000 = 0
    count_tc8000_online = 0
    count_tc8000_online_not_charging = 0
    count_wt6000 = 0
    count_wt6000_online = 0
    count_wt6000_online_not_charging = 0
    count_tc52 = 0
    count_tc52_online = 0
    count_tc52_online_not_charging = 0
    for elt in all_devices['Result']:
        if 'TC8000' in elt['name']:
            if '/Leroy_Merlin_France/PROD/ENTREPOT/TC8000/' in elt['path']:
                count_tc8000 = count_tc8000 + 1
                export['TC8000']['Total'] = count_tc8000
                if elt['online']:
                    count_tc8000_online = count_tc8000_online + 1
                    export['TC8000']['Online'] = count_tc8000_online
                    if not elt['charging']:
                        count_tc8000_online_not_charging = count_tc8000_online_not_charging + 1
                        export['TC8000']['Used'] = count_tc8000_online_not_charging
        if 'WT6000' in elt['name']:
            if '/Leroy_Merlin_France/PROD/ENTREPOT/WT6000/' in elt['path']:
                count_wt6000 = count_wt6000 + 1
                export['WT6000']['Total'] = count_wt6000
                if elt['online']:
                    count_wt6000_online = count_wt6000_online + 1
                    export['WT6000']['Online'] = count_wt6000_online
                    if not elt['charging']:
                        count_wt6000_online_not_charging = count_wt6000_online_not_charging + 1
                        export['WT6000']['Used'] = count_wt6000_online_not_charging
        if 'TC52' in elt['name']:
            if '/Leroy_Merlin_France/PROD/ENTREPOT/TC52/' in elt['path']:
                count_tc52 = count_tc52 + 1
                export['TC52']['Total'] = count_tc52
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

with open('D:\Drive partagés\LMFR-RUN MCO DTP\Indicateurs\Mobility\export_warehouses_' + day + '.json', 'w') as fp:
    json.dump(a, fp)
