import json

configs = json.load(open('config.json'))

db = configs['db']

server = configs['server']

session = configs['session']

headers = configs['headers']
