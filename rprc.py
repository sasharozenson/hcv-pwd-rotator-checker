#!/usr/bin/env python3

#Alexander Sasha Rozenson #sasharozenson@gmail.com #2020

import requests
import datetime
import smtplib
import config

# Vars
token = config.token
smtp_server = config.smtp_server
vault_api_uri = config.vault_api_uri
mail_from = config.mail_from
mail_to = config.mail_to
error_message = ""
failed_hosts = []
hostslist = []


# Get all host in a secret
def get_hosts():
    try:
        response = requests.request(
            'LIST',
            vault_api_uri + '/metadata/linux',
            headers={'X-Vault-Token': token},
        )
    except requests.exceptions.RequestException as e:
        error_message = str(SystemExit(e))
        send_mail(error_message,"err")
        raise SystemExit(e)
    jd = response.json()['data']['keys']
    for host in jd:
        hostslist.append(host.split("/")[0])
    return hostslist


# Get metadata of a given host
def get_metadata(hostname):
    try:
        response = requests.get(
            vault_api_uri + '/data/linux/' + hostname + '/root_creds',
            headers={'X-Vault-Token': token},
        )
    except requests.exceptions.RequestException as e:
        error_message = str(SystemExit(e))
        send_mail(error_message,"err")
        raise SystemExit(e)
    return response.json()['data']['metadata']['created_time']


# Compare latest password update with current time -24h
def check_last_change_time(hostname):
    last_change_time = get_metadata(hostname).split('.')[0]
    date_time_obj = datetime.datetime.strptime(last_change_time, '%Y-%m-%dT%H:%M:%S')
    yesterday_date_time = datetime.datetime.now() - datetime.timedelta(hours=24)
    if date_time_obj < yesterday_date_time:
        return date_time_obj
    else:
        return True


# Send mail either error occurred during request or rotation problem
def send_mail(suffix, *error):
    sender = [mail_from]
    receivers = [mail_to]

    if error:
        message = "From: Root Rotator Check <" + mail_from + """>
To: """ + mail_to + """
MIME-Version: 1.0
Content-type: text/html
Subject: Root Rotator Checker Error

Please fix the following error ASAP: <br>
""" + suffix

    else:
        message = "From: Root Rotator Check <" + mail_from + """>
To: """ + mail_to + """
MIME-Version: 1.0
Content-type: text/html
Subject: Some of the servers have not changed the password for more than 24h

There is an error with one or more hosts: <br>
""" + suffix

    try:
        smtpObj = smtplib.SMTP(smtp_server, 25)
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")


def main():
    for host in get_hosts():
        result = check_last_change_time(host)
        if result is not True:
            print(f"Checking {host}: Check passed")
        else:
            print(f"{host} is in trouble")
            failed_hosts.append(host)

    if len(failed_hosts) > 0:
        send_mail(str(failed_hosts))


# Main
if __name__ == "__main__":
    main()
