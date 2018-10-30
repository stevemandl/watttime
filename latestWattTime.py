#!/usr/bin/python
"""
 latestWattTime.py
 prints out latest marginal carbon emission reading from wattime api
"""

from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth

# globals
username  = "CornellCEP"
password  = "xxxxxxxxx"
loginURL  = 'https://api2.watttime.org/v2/login/'
dataURL   = 'https://api2.watttime.org/v2/data/'
basicAuth = HTTPBasicAuth(username, password)

# main()
def main():
    try:
        # login and get token
        resp = requests.get( loginURL, auth=basicAuth )
        if resp.status_code != 200:
            raise Exception('Status %s getting %s' % (resp.status_code, loginURL))

        #extract token from login response
        token = resp.json()['token']

        # print(token)
        #build authorization header
        authHeader = { 'Authorization': token }

        # compute five minutes ago
        fiveMinAgo = (datetime.utcnow() + timedelta(minutes=-5)).isoformat()

        # form the request payload
        payload = { 'ba': 'NYISO_CENTRAL',
                    'starttime': fiveMinAgo }

        # make the REST call
        resp = requests.get(dataURL, auth=basicAuth, headers=authHeader, params=payload)
        if resp.status_code != 200:
            raise Exception('Status %s getting %s' % (resp.status_code, dataURL))

        #decode it
        raw = resp.json()

        #filter out the non-carbon emission datatypes
        filtered = filter(lambda x: x["datatype"] == "MOER", raw)

        # print it out
        print([{"point_time": x["point_time"], "value": x["value"]} for x in filtered])


    except Exception as e:
        print str(e)
    finally:
        pass

if __name__ == '__main__':
    main()

