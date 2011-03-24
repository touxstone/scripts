try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
import getopt
import sys
import string
import time
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom

class SMS(object):
    def __init__(self, user, passwd):
        self.user = user.rstrip('@gmail.com')
        self.passwd = passwd
        self.DELAY = 60 * 3 
        self._authenticate()
    
    def _authenticate(self):
        self.service = gdata.calendar.service.CalendarService()
        self.service.email = self.user + '@gmail.com'
        self.service.password = self.passwd
        self.service.source = 'Calendar'
        self.service.ProgrammaticLogin()

    def sendSMS(self, title, content=''):
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=content)        
        
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
                                   time.gmtime(time.time() + self.DELAY))
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
                                 time.gmtime(time.time() + self.DELAY + 60 * 2))
        
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        event.when[0].reminder.append(gdata.calendar.Reminder(minutes=1, method="sms"))
        self.service.InsertEvent(event, '/calendar/feeds/default/private/full')
