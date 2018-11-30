#!/usr/bin/python
"""
 test.py
 tests wattime api
"""
import datetime
import requests
from requests.auth import HTTPBasicAuth

# globals
username  = "CornellCEP"
password  = "CEPCornell2019"
loginURL  = 'https://api2.watttime.org/v2/login/'
dataURL   = 'https://api2.watttime.org/v2/data/'
basicAuth = HTTPBasicAuth(username, password)

# main()
def main():
    try:
        resp = requests.get( loginURL, auth=basicAuth )
        if resp.status_code != 200:
            raise Exception('%s %s' % (url, resp.status_code))
        #extract token from login response
        token = resp.json()['token']
        # print(token)
        #build authorization header
        authHeader = { 'Authorization': token }
        fiveMinAgo = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-5)).isoformat()
        payload = {
                'ba': 'NYISO_CENTRAL',
                'starttime': fiveMinAgo }
        resp = requests.get(dataURL, auth=basicAuth, headers=authHeader, params=payload)
        raw = resp.json()
        filtered = filter(lambda x: x["datatype"] == "MOER", raw)
        print([{"point_time": x["point_time"], "value": x["value"]} for x in filtered])


    except Exception as e:
        print str(e)
    finally:
        pass

if __name__ == '__main__':
    main()

