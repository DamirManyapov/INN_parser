#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

API_KEY = ""
#API_KEY = ""
BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/{}"
region = "Красноярский"

#query = sys.argv[1]

def suggest(query, resource, count=10):
    url = BASE_URL.format(resource)
    headers = {"Authorization": "Token {}".format(API_KEY), "Content-Type": "application/json"}
    data = {"query": query, "count": count}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


if __name__ == "__main__":
    f = open('value.txt')
    for line in f.readlines():
        line = line.replace("\n", "")
        line = line.split('\t')
        line = '\t'.join([line[0].strip(), line[1].strip()])
        query = (line)
        print('******* --- Ищем Организацию --- *******')
        print(query)
        result = suggest(query, "party", count=5)
        if len(result['suggestions']) == 0:
            query = query.split('\t')[0]
            query = (query + '\t' + region)
            print('******* --- Организацию по ДИРЕКТОРУ НЕ нашли --- *******')
            print('******* --- Делаем доп проверку по региону --- *******')
            result = suggest(query, "party", count=5)
            if len(result['suggestions']) == 0:
                print('******* --- Нет организации --- *******')
                f1 = open("inn.txt", 'a')
                f1.write('НЕТ ОРГАНИЗАЦИИ' + '\n')
                f1.close()
            else:
                print('******* --- Организацию нашли по региону --- *******')
                res = result['suggestions'][0]
                data = res['data']
                value = res['unrestricted_value']
                inn = data['inn']
                okved = data.get('okved') or 'Нет Данных'
                okved_type = data.get('okved_type') or 'Нет Данных'
                status = data['state']['status']
                address = data.get('address')
                if address:
                    address = address['value']
                else:
                    address = 'Нет данных'
                management = data.get('management')
                if management:
                    name = management['name']
                else:
                    name = 'Нет данных'
                print('Организация', value, 'ИНН', inn, 'ОКВЕД', okved, 'Версия ОКВЕД', okved_type, status, 'Директор', name, 'Адресс:', address,)
                f1 = open("inn.txt", 'a')
                f1.write(value + '\t' + inn + '\t' + okved + '\t' + okved_type + '\t' + status + '\t' + name + '\t' + address + '\n')
                f1.close()
        else:
            res = result['suggestions'][0]
            data = res['data']
            value = res['unrestricted_value']
            inn = data['inn']
            okved = data.get('okved') or 'Нет Данных'
            okved_type = data.get('okved_type') or 'Нет Данных'
            status = data['state']['status']
            address = data.get('address')
            if address:
                address = address['value']
            else:
                address = 'Нет данных'
            management = result['suggestions'][0]['data'].get('management')
            management = data.get('management')
            if management:
                name = management['name']
            else:
                name = 'Нет данных'
            print('******* --- Организацию нашли по ДИРЕКТОРУ --- *******')
            print('Организация', value, 'ИНН', inn, 'ОКВЕД', okved, 'Версия ОКВЕД', okved_type, status, 'Директор', name, 'Адресс:', address,)
            f1 = open("inn.txt", 'a')
            f1.write(value + '\t' + inn + '\t' + okved + '\t' + okved_type + '\t' + status + '\t' + name + '\t' + address + '\n')
            f1.close()
