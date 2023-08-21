import os, json, requests
import pandas as pd
import python_cde.cdeconnection as cde
from datetime import datetime
import pytz
#import yagmail
import sys
import argparse

#Execute with:
#python3 multi_cluster_alerter.py --clusters clusters.txt cdpusername cdppwd mysmtpserver 1800 me@myco.com 

def parse_args():

    parser = argparse.ArgumentParser(description="My program!", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--clusters", type=argparse.FileType('r'), help="Filename to be passed")
    parser.add_argument("cdp_user", type=str, help="enter the cdp workload user")
    parser.add_argument("cdp_password", type=str, help="enter the cdp workload password")
    parser.add_argument("smtp", type=str, help="enter the smtp server")
    parser.add_argument("max_job_seconds", type=int, help="enter the max job duration in seconds to qualify a lagger job")
    parser.add_argument("email_sender", type=str, help="enter the notification email sender")
    #parser.add_argument("email_recipient", type=str, help="enter the notification email recipient")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = vars(parser.parse_args())

    return args

def main():

    args = parse_args()

    CLUSTERS = args["clusters"].read().splitlines() # list of JOB API URLs e.g. "https://z4xgdztf.cde-6fr6l74r.go01-dem.ylcu-atmi.cloudera.site/dex/api/v1"
    WORKLOAD_USER = args["cdp_user"] #"cdpusername"
    WORKLOAD_PASSWORD = args["cdp_password"] #"cdppwd"
    MAX_JOB_DURATION_SECONDS = args["max_job_seconds"] #number of seconds between job start and end that qualifies the job as a lagger
    EMAIL_SENDER = args["email_sender"] #me@myco.com
    #EMAIL_RECIPIENT = args["email_recipient"] #mycolleague@myco.com
    SMTP = args["smtp"] #"mysmtphere"

    for CLUSTER in CLUSTERS:
    # Instantiate the Connection to CDE

        JOBS_API_URL = CLUSTER.split(" ")[0]
        EMAIL_RECIPIENT = CLUSTER.split(" ")[1]

        cde_connection = cde.CdeConnection(JOBS_API_URL, WORKLOAD_USER, WORKLOAD_PASSWORD)
        TOKEN = cde_connection.set_cde_token()

        # Poll the CDE Virtual Cluster with Current Jobs and Determine Laggers
        response = cde_connection.list_cde_job_runs(TOKEN)
        print(response.status_code)

        laggers_df, job_duration_seconds = cde_connection.detect_laggers(response, MAX_JOB_DURATION_SECONDS)
        tz_LA = pytz.timezone('America/Los_Angeles')

        if len(laggers_df)>0:
            now = datetime.now(tz_LA)
            cde_vc_name = cde_connection.print_vc_meta(TOKEN)
            cde_connection.smtplib_email_alert(laggers_df, job_duration_seconds, EMAIL_SENDER, EMAIL_RECIPIENT, SMTP, cde_vc_name)
            print("{} PACIFIC STANDARD TIME".format(now))
            print("Executing CDE Alerter for CDE Virtual Cluster {}".format(cde_vc_name))
            print("The CDE Alerter found at least one job taking longer than {} minutes".format(job_duration_seconds/60))
            print("An Email notification was sent to the following recipients: {0}, {1}".format(EMAIL_SENDER, EMAIL_RECIPIENT))
            print("\n")
        else:
            tz_SD = pytz.timezone('America/Los_Angeles')
            now = datetime.now(tz_LA)
            cde_vc_name = cde_connection.print_vc_meta(TOKEN)
            print("{} PACIFIC STANDARD TIME".format(now))
            print("Executing CDE Alerter for CDE Virtual Cluster {0}".format(cde_vc_name))
            print("The CDE Alerter found no jobs taking longer than {} minutes".format(job_duration_seconds/60))
            print("No Email notification sent")
            print("\n")

if __name__ == '__main__':
    main()
