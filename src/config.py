import json

configs = json.load(open('config.json'))

db = configs['db']

session = configs['session']

