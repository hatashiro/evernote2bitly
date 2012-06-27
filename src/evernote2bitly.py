from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import requests
import sys
import os
import time

class Link:
    title = ''
    url = ''
    created = ''

def evtime2epoch(evdatetime):
    evdate = evdatetime.split('T')[0][:8]
    evtime = evdatetime.split('T')[1][:6]

    year = int(evdate[0:4])
    month = int(evdate[4:6])
    day = int(evdate[6:8])

    hour = int(evtime[0:2])
    minute = int(evtime[2:4])
    second = int(evtime[4:6])

    return int(time.mktime(dt(year, month, day, hour, minute, second).timetuple()))

# standby
evernotefile = sys.argv[1]
xml = file(evernotefile).read()
soup = bs(xml)

# make link list
links = list()
for note in soup.find_all('note'):
    link = Link()
    link.title = note.title.string
    link.url = bs(note.content.string).find('en-note').a['href']
    link.created = note.created.string
    links.append(link)

# sort by created datetime
links = sorted(links, key=lambda link: link.created)


# get oauth token
bitly_id = raw_input('bitly account id > ')
bitly_pw = raw_input('bitly password > ')
access_token = requests.post('https://api-ssl.bitly.com/oauth/access_token', auth=(bitly_id, bitly_pw)).text
print access_token

# save url
for link in links:
    print '----'
    print link.title
    print link.url
    print '----'

    params = {'access_token':access_token, 'longUrl':link.url, 'title':link.title, 'user_ts':str(evtime2epoch(link.created))}
    r = requests.get('https://api-ssl.bitly.com/v3/user/link_save', params=params)

# print result
print 'Total '+str(len(links))+' link(s) saved.'
