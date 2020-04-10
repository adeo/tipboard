import glob, os, yaml
import re

from src.tipboard.app.properties import DEBUG, user_config_dir
from src.tipboard.app.utils import getTimeStr


class WrongSumOfRows(Exception):
    pass


def getCols(rows):
    cols = []
    for col in list(rows.values())[0]:
        cols.append(col)
    return cols


def getRows(layout):
    """ Validates and returns number of rows."""
    rows_count = 0
    sum_of_rows = list()
    rows_data = [row for row in layout]
    rows_class = [list(row.keys()) for row in layout]
    for row_class in rows_class:
        splited_class = row_class[0].split('_')  # ex: row_1_of_2
        row = splited_class[1]
        of_rows = int(splited_class[3])
        if rows_count == 0:
            rows_count = int(of_rows)
            sum_of_rows.append(int(row))
        elif not rows_count == of_rows:
            raise WrongSumOfRows('The sum of the lines is incorrect.')
        else:
            sum_of_rows.append(int(row))
    if not sum(sum_of_rows) == rows_count:
        raise WrongSumOfRows('The sum of the lines is incorrect.')
    return rows_data


def analyseCols(tiles_id, tiles_templates, tiles_dict):
    for tile_dict in tiles_dict:
        if tile_dict['tile_id'] not in tiles_id:
            tiles_id.append(tile_dict['tile_id'])
            tiles_templates.append(tile_dict['tile_template'])


def findTilesNames(cols_data):
    """ Find tile_id in all cols of .yaml """
    tiles_templates, tiles_id = list(), list()
    for col_dict in cols_data:
        for tiles_dict in list(col_dict.values()):
            analyseCols(tiles_id, tiles_templates, tiles_dict)
    if DEBUG:
        print(f"{getTimeStr()} (+) Parsing Config file with {len(tiles_id)} tiles parsed "
              f"and {len(tiles_templates)} tiles templates")
    return tiles_templates, tiles_id


def yamlFileToPythonDict(layout_name='layout_config'):
    """ Parse in yaml the .yaml file to return python object """
    config_path = os.path.join(user_config_dir, ''.join([layout_name]))
    try:
        with open(config_path, 'r') as layout_config:
            config = yaml.safe_load(layout_config)
    except FileNotFoundError:
        if ".yaml" not in config_path:
            config_path += ".yaml"
        with open(config_path, 'r') as layout_config:
            config = yaml.safe_load(layout_config)
    return config


def parseXmlLayout(layout_name='layout_config'):
    """ Parse all tiles, cols, rows from a specific .yaml """
    config = yamlFileToPythonDict(layout_name=layout_name)
    rows = [row for row in getRows(config['layout'])]
    cols = [col for col in [getCols(row) for row in rows]]
    cols_data = [colsValue for colsList in cols for colsValue in colsList]
    config['tiles_names'], config['tiles_keys'] = findTilesNames(cols_data)
    return config


def getConfigNames():
    """ Return all configs files' names (without '.yaml' ext.) from user space (.tipboard/) """
    configs_names = list()
    configs_dir = os.path.join(user_config_dir, '**/*.yaml')
    r = re.compile(r".*/Config/(.*)\.yaml")
    for config_path in glob.glob(configs_dir, recursive=True):  # Get all name of different *.yml present in Config/ directory
        config = r.sub("\\1", str(config_path).replace("\\", "/"))
        matches = re.search(r"template/[A-z0-9]+$", config)
        if not matches:
            configs_names.append(config)
        if not configs_names:
            raise Exception(f'No config (.yaml) file found in {os.path.join(user_config_dir, "*.yaml")}')
    return configs_names


def getFlipboardTitle():
    """ Returns title to display as a html title. """
    title = ''
    config_names = getConfigNames()  # get all name of files present in ./Config/*.yaml
    try:
        if len(config_names) == 1:  # if only one file, return the one
            config = parseXmlLayout(config_names[0])
            title = config['details']['page_title']
        else:  # if multiple file, need to have the .yaml displayed for the client
            title = 'Flipboard Mode'
    except KeyError:
        print(f"{getTimeStr()} (+) config {config_names[0]} has no key: details/page_title'", flush=True)
    print(f"TITLE:{title}")
    return title


def getTimeFlipFromLayout(layout_name='layout_config'):
    pass


def getFlipboardTitles():
    config_names = getConfigNames()
    listNameDashboard = list()
    rcx = 1
    for config in config_names:
        print(f'Config : {config}')
        config = parseXmlLayout(config)
        if 'details' in config and 'page_title' in config['details']:
            listNameDashboard.append(config['details']['page_title'])
        else:
            listNameDashboard.append(f'Dashboard {rcx}')
        rcx += 1
    return listNameDashboard
