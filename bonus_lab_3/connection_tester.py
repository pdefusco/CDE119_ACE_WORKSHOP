#pip3 install -r requirements.txt

import os, json, requests
import python_cde.cdeconnection as cde
import sys

def main(args):

    # Setting variables for script
    JOBS_API_URL = args[1] #"https://z4xgdztf.cde-6fr6l74r.go01-dem.ylcu-atmi.cloudera.site/dex/api/v1"
    WORKLOAD_USER = args[2] #"cdpusername"
    WORKLOAD_PASSWORD = args[3] #"cdppwd"

    # Instantiate the Connection to CDE
    cde_connection = cde.CdeConnection(JOBS_API_URL, WORKLOAD_USER, WORKLOAD_PASSWORD)
    TOKEN = cde_connection.set_cde_token()

    # Test ability to create a CDE Resource of type file
    cde_connection.create_cde_resource(TOKEN, "test_resource")

if __name__ == '__main__':
    main(sys.argv)
