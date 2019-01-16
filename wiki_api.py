import json
import requests
import pandas as pd
from itertools import islice
import pymongo
import time

conn = 'mongodb://root:ucbmongodb@35.184.4.63:27017'
client = pymongo.MongoClient(conn)

db = client.wikidb

API_URL = 'https://en.wikipedia.org/w/api.php'
headers = {'accept': 'application/json'}
with open('enwiki-20181001-all-titles-sample.txt', 'r') as title_file:
    lines_gen = list(islice(title_file, 10))
    while lines_gen:
        temp_title_param=''
        for line in lines_gen:
            if temp_title_param == '':
                temp_title_param +=  str(line).rstrip()
            else:
                temp_title_param +=  '|' + str(line).rstrip()
        params = {
                'action': 'query',
                'format': 'json',
                'prop': 'info|pageviews',
                'list':'',
                'meta':'',
                'titles':temp_title_param,
            }
        time.sleep(1)
        r = requests.get(API_URL, headers=headers, params=params)
        results = r.json()
        # print(r.status_code)
        # print(json.dumps(results))
        if r.status_code == 200:
            if 'continue' in results:
                print('Not all records were queried')
            elif 'batchcomplete' in results:
                print('batchcomplete is successfull')
            # print(json.dumps(results))
            # print(results['query']['pages'].keys())
            for key in results['query']['pages'].keys():
                temp_doc = results['query']['pages'][key]
                if 'normalized' in results['query']:
                    # print('normalized titles exists')
                    # print(results['query']['normalized'])
                    for n in results['query']['normalized']:
                        if n['to'] == temp_doc['title']:
                            temp_doc['title'] = n['from']
                            temp_doc['normalized_title'] = n['to']
                            break
                # print(temp_doc)
                db.wikipageinfo.insert_one(temp_doc)
        lines_gen = list(islice(title_file, 10))