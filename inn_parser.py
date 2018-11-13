#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

API_KEY = "e61923db5b61157865f98a3584d3250e062e8cab"
BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/{}"

def suggest(query, resource, count=10):
    url = BASE_URL.format(resource)
    headers = {"Authorization": "Token {}".format(API_KEY), "Content-Type": "application/json"}
    data = {"query": query, "count": count}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


if __name__ == "__main__":
    
    f = open('value.txt')
    for line in f.readlines():
        query = (line)
        #print (query)
        result=suggest(query, "party", count=5)
        if len(result['suggestions']) <= 0:
            f1 = open("inn.txt", 'a')
            line = line.replace("\n","")
            f1.write(line + '\t' + 'НЕТ ОРГАНИЗАЦИИ' + '\n')
            f1.close()
        #print (result)
        else:
            value=(result['suggestions'][0]['unrestricted_value'])
            inn=(result['suggestions'][0]['data']['inn'])
        # print(inn)
        # print(value)
        #query = sys.argv[1]

            print('Организация',value, 'ИНН',inn)
            f1 = open("inn.txt", 'a')
            f1.write(value + '\t' + inn + '\n')
            f1.close()
