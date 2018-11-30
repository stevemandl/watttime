#!/usr/bin/python
"""
 lambdaToRDS.py
 lambda function that adds recent data to RDS table
"""
import boto
from datetime import datetime, timedelta
import dateutil.parser
import requests
from requests.auth import HTTPBasicAuth
import pymysql.cursors

# globals
username  = "CornellCEP"
password  = "CEPCornell2019"
loginURL  = 'https://api2.watttime.org/v2/login/'
dataURL   = 'https://api2.watttime.org/v2/data/'
basicAuth = HTTPBasicAuth(username, password)

# handler()
def handler(event, context):
    main()

# main()
def main():
    db = pymysql.connect(
        host="emcstrendmsql.cu1e95kjxvy3.us-east-1.rds.amazonaws.com",
        user="watttime",
        passwd="CEPCornell2019",
        db="trends"
    )

    try:
        cur = db.cursor()
        
        # get last timestamp loaded
        sql = "select max(point_time) from watttime_data"

        cur.execute(sql)

        res = cur.fetchone()
        lastTime = dateutil.parser.parse(res[0])
        print( 'last time: %s' % lastTime)


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

        # form the request payload
        payload = { 'ba': 'NYISO_CENTRAL',
                    'starttime': lastTime }

        # make the REST call
        print("requesting data...")
        resp = requests.get(dataURL, auth=basicAuth, headers=authHeader, params=payload)
        if resp.status_code != 200:
            raise Exception('Status %s getting %s' % (resp.status_code, dataURL))

        #decode it
        print("got raw data!")
        raw = resp.json()

        #filter out the non-carbon emission datatypes
        filtered = filter(lambda x: x["datatype"] == "MOER" and dateutil.parser.parse(x["point_time"]) > lastTime, raw)

        # print it out
        # print([{"point_time": x["point_time"], "value": x["value"]} for x in filtered])

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
        db.close()

if __name__ == '__main__':
    main()

