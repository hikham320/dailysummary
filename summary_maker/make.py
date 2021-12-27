import sys
import auth, init, get, format
import datetime

def make(date1=None, date2=None):
    datetime1 = None
    datetime2 = None
    if date1:
        datetime1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    if date2:
        datetime2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
        
    service = auth.authenticate()
    events = get.retrieve_events(service, datetime1, datetime2)
    
    return events

def daily(date1=None, date2=None):
    events = make(date1, date2)
    format.print_events( format.process_daily( events ) )
    
    
def total(date1=None, date2=None):
    events = make(date1, date2)
    
    print('■ {} -- {}'.format(
        datetime.datetime.strptime(date1, '%Y-%m-%d').strftime('%Y年%m月%d日'),
        datetime.datetime.strptime(date2, '%Y-%m-%d').strftime('%Y年%m月%d日')
    ) )
    format.print_events( format.process_total( events ) )
