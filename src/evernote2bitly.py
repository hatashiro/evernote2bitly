from bs4 import BeautifulSoup as bs
import sys

class Link:
    title = ''

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

for link in links:
    print link.title
    print link.url

print len(links)
