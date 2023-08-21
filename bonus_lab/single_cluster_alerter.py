#pip3 install -r requirements.txt

import os, json, requests
import pandas as pd
import python_cde.cdeconnection as cde
from datetime import datetime
import pytz
#import yagmail
import sys

#Execute with:
#python3 alerter.py https://z4xgdztf.cde-6fr6l74r.go01-dem.ylcu-atmi.cloudera.site/dex/api/v1 cdpusername cdppwdhere mysmtphere 1800 me@myco.com mycolleague@myco.com

def main(args):

    # Setting variables for script
    JOBS_API_URL = args[1] #"https://z4xgdztf.cde-6fr6l74r.go01-dem.ylcu-atmi.cloudera.site/dex/api/v1"
    WORKLOAD_USER = args[2] #"cdpusername"
    WORKLOAD_PASSWORD = args[3] #"cdppwd"
    SMTP = args[4] #"mysmtphere"
    MAX_JOB_DURATION_SECONDS = int(args[5]) #number of seconds between job start and end that qualifies the job as a lagger
    EMAIL_SENDER = args[6] #me@myco.com
    EMAIL_RECIPIENT = args[7] #mycolleague@myco.com

    # Instantiate the Connection to CDE
    cde_connection = cde.CdeConnection(JOBS_API_URL, WORKLOAD_USER, WORKLOAD_PASSWORD)
    TOKEN = cde_connection.set_cde_token()

    # Poll the CDE Virtual Cluster with Current Jobs and Determine Laggers
    response = cde_connection.list_cdejob_runs(TOKEN)
    print(response.status_code)

    laggers_df, job_duration_seconds = cde_connection.detect_laggers(response, MAX_JOB_DURATION_SECONDS)
    tz_LA = pytz.timezone('America/Los_Angeles')

    if len(laggers_df)>0:
        cde_connection.smtplib_email_alert(laggers_df, job_duration_seconds, EMAIL_SENDER, EMAIL_RECIPIENT, SMTP)
        now = datetime.now(tz_LA)
        print("The CDE Alerter executed at {0} PACIFIC STANDARD TIME and found at least one job taking longer than {1} minutes".format(now, job_duration_seconds/60))
        print("An Email was sent to the following recipients: {0}, {1}".format(EMAIL_SENDER, EMAIL_RECIPIENT))
    else:
        now = datetime.now(tz_LA)
        print("The CDE Alerter executed at {0} PACIFIC STANDARD TIME and found no jobs taking longer than {1} minutes".format(now, job_duration_seconds/60))

if __name__ == '__main__':
    main(sys.argv)
