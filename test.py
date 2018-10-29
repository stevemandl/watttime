#!/usr/bin/python
"""
 test.py
 tests wattime api
"""

# globals
username = "sjm34"
password = "sjm34sjm34"

import requests
from requests.auth import HTTPBasicAuth

def main():
    try:
        url = 'https://api2.watttime.org/v2/login/'
        resp = requests.get(url, auth=HTTPBasicAuth(username, password))
        if resp.status_code != 200:
            raise ApiError('%s %s' % (url, resp.status_code))
        print(resp.json())
    except Exception, e:
        print str(e)
    finally:
        pass

if __name__ == '__main__':
    main()

