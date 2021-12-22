from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import traceback, json, re

try:
    import config
except:
    pass

def format_eventname(evname):
    backlog_format = re.compile('([A-Z_-]+-[0-9]+) (.*)')
    result = backlog_format.match(evname)
    if result:
        return backlog_format.sub("\\2 (\\1)", evname)
    return evname + " (チケットなし)"

def process_total(evlist):
    try:
        emaillist = config.EMAIL_ADDRESS.split(',')
    except:
        emaillist = None
    
    event_list = {}
    for event in evlist:
        if emaillist:
            valid = False
            for email in emaillist:
                if event['creator']['email'] == email.strip():
                    valid = True
                    break
            if not valid:
                continue
        
        start = datetime.datetime.strptime(
            event['start'].get('dateTime', event['start'].get('date')),
            '%Y-%m-%dT%H:%M:%S+09:00')
        end = datetime.datetime.strptime(
            event['end'].get('dateTime', event['end'].get('date')),
            '%Y-%m-%dT%H:%M:%S+09:00')
        
        eventname = format_eventname(event['summary'])
        if not eventname in event_list:
            event_list[eventname] = end - start
        else:
            event_list[eventname] += end - start
    return event_list


def process_daily(evlist):
    try:
        email = config.EMAIL_ADDRESS
    except:
        email = None
    event_list = {}
    for event in evlist:
        if email:
            if event['creator']['email'] != email:
                continue
        
        start = datetime.datetime.strptime(
            event['start'].get('dateTime', event['start'].get('date')),
            '%Y-%m-%dT%H:%M:%S+09:00')
        end = datetime.datetime.strptime(
            event['end'].get('dateTime', event['end'].get('date')),
            '%Y-%m-%dT%H:%M:%S+09:00')
        
        target_date = start - datetime.timedelta(hours=6)
        target_date_str = datetime.datetime.strftime(target_date, '%Y-%m-%d')
        
        if not target_date_str in event_list:
            event_list[target_date_str] = {}
        
        
        eventname = format_eventname(event['summary'])
        if not eventname in event_list[target_date_str]:
            event_list[target_date_str][eventname] = end - start
        else:
            event_list[target_date_str][eventname] += end - start
    return event_list

def print_events(evlist):
    try:
        for k, v in evlist.items():
            print('{} : {:.2f} 時間'.format( k, v.total_seconds() / 3600.00 ) )
    except:
        for k1, v1 in evlist.items():
            print('■ ' + datetime.datetime.strptime(k1, '%Y-%m-%d').strftime('%Y年%m月%d日') )
            for k2, v2 in v1.items():
                print('{} : {:.2f} 時間'.format( k2, v2.total_seconds() / 3600.00 ) )
            print('')