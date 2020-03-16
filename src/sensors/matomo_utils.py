import requests

# ici on enregistre les urls du matomo sur lesquelles on va taper pour les requêtes
base_url = "http://analytics-warehouse-open.apps.op.acp.adeo.com/index.php?"


def get_matomo_request(params={}):

    return requests.get(base_url, params, verify=False)
