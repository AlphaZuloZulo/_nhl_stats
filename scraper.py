import scraperwiki
import requests
import lxml.html
import re

def duckint(i):
    try:
        return int(i)
    except ValueError:
        return i

# Blank Python
lookup = ['Name','Team','GP','GS','MIN','W','L','OTL','EGA','GA','GAA','SA','SV','SVP','SO']
num =    [0,1,2,4,6,5,9,11,13,15,17,19,21,23,25]

lstring = ', '.join(lookup)

scraperwiki.sqlite.execute('create table if not exists score (%s)'%lstring)

#url='http://sports.yahoo.com/nhl/stats/byposition?pos=D'
#url='http://sports.yahoo.com/nhl/stats/byposition?pos=D&conference=NHL&year=season_2015&qualified=1'
url='http://sports.yahoo.com/nhl/stats/byposition?pos=G&conference=NHL&year=season_2015&qualified=1'

html=requests.get(url).content
root=lxml.html.fromstring(html)

rows=root.xpath('//tr[@class="ysprow1" or @class="ysprow2"]')
builder=[]
for row in rows:
    data={}
    cells=[cell.text_content().strip() for cell in row.xpath('td[@class="yspscores"]')]
    for i,n in enumerate(num):
        data[lookup[i]]=duckint(cells[n])
    data['Pts']=duckint(row.xpath('descendant-or-self::span[@class="yspscores"]')[0].text_content().strip())
    builder.append(data)
    
scraperwiki.sqlite.save(table_name='score', data=builder, unique_keys=['Name'])
