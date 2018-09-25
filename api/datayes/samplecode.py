# -*- coding: utf-8 -*-
import os
import json
import requests
CURR_PATH = os.path.split(os.path.abspath(__file__))[0]

if __name__ == "__main__":
    with open(os.path.join(CURR_PATH,'../../tokens/datayes.json'),'r') as f:
        ak = f.readline()
        ak = json.loads(ak)['token']
        print(ak)
        url='https://api.wmcloud.com/data/v1/api/equity/getEqu.json?field=&ticker=000001&secID=&equTypeCD=&listStatusCD='
        headers = {"Authorization": "Bearer " + ak}
        result=requests.get(url,headers=headers).json()
        print(result)

