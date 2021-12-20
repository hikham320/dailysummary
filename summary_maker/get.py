from __future__ import print_function
import datetime

def retrieve_events(service, date_from=None, date_to=None):
    if type(date_from) != datetime.datetime and date_from != None:
        raise TypeError('date_from must be datetime.datetime object or None. type was: ' + str(type(date_from)))
    if type(date_to) != datetime.datetime and date_to != None:
        raise TypeError('date_to must be datetime.datetime object or None. type was: ' + str(type(date_to)))

    if date_from == None:
        date_from = datetime.datetime.now() - datetime.timedelta(hours=6)
    if date_to == None:
        date_to = date_from
    date_to += datetime.timedelta(days=1)
    
    time_min = date_from.strftime('%Y-%m-%d') + 'T06:00:00.000000+0900'
    time_max = date_to.strftime('%Y-%m-%d') + 'T05:59:59.999999+0900'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        maxResults=65535,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    evlist = []
    time_min_datetime = datetime.datetime.strptime( time_min, '%Y-%m-%dT%H:%M:%S.%f+0900')
    for event in events:
        start = datetime.datetime.strptime(
            event['start'].get('dateTime', event['start'].get('date')),
            '%Y-%m-%dT%H:%M:%S+09:00'
        )
        if start < time_min_datetime:
            continue
        evlist.append(event)
    
    return evlist