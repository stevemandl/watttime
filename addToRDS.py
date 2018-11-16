#!/usr/bin/python
"""
 addToRDS.py
 adds recent data to RDS table
"""

from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
from openpyxl import Workbook
import mysql.connector

# globals
username  = "CornellCEP"
password  = "CEPCornell2019"
loginURL  = 'https://api2.watttime.org/v2/login/'
dataURL   = 'https://api2.watttime.org/v2/data/'
basicAuth = HTTPBasicAuth(username, password)

# main()
def main():
    try:
        # login and get token
        print("getting session token")
        resp = requests.get( loginURL, auth=basicAuth )
        if resp.status_code != 200:
            raise Exception('Status %s getting %s' % (resp.status_code, loginURL))

        #extract token from login response
        token = resp.json()['token']

        print("got token")
        #build authorization header
        authHeader = { 'Authorization': token }

        # compute a day ago
        aDayAgo = (datetime.utcnow() + timedelta(days=-1)).isoformat()

        # form the request payload
        payload = { 'ba': 'NYISO_CENTRAL',
                    'starttime': aDayAgo }

        # make the REST call
        print("requesting data...")
        resp = requests.get(dataURL, auth=basicAuth, headers=authHeader, params=payload)
        if resp.status_code != 200:
            raise Exception('Status %s getting %s' % (resp.status_code, dataURL))

        #decode it
        print("got raw data!")
        raw = resp.json()

        #filter out the non-carbon emission datatypes
        filtered = filter(lambda x: x["datatype"] == "MOER", raw)

        # print it out
        # print([{"point_time": x["point_time"], "value": x["value"]} for x in filtered])

        db = mysql.connector.connect(
            host="emcstrendmsql.cu1e95kjxvy3.us-east-1.rds.amazonaws.com",
            user="watttime",
            passwd="CEPCornell2019",
            database="trends"
        )
        cur = db.cursor()
        sql = "INSERT INTO watttime_data (point_time, point_value, data_type, balancing_authority) VALUES (%s, %s, %s, %s)"
        print("about to insert data into database...")
        row_count=0

        for row in filtered:
            val = (row["point_time"], row["value"], "MOER", payload["ba"])
            cur.execute(sql, val)
            row_count = row_count + 1
        db.commit()
        print("number of records inserted: %d" % row_count)



    except Exception as e:
        print str(e)
    finally:
        pass

if __name__ == '__main__':
    main()

