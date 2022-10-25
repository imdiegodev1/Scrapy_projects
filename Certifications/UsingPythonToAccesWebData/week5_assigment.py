##You are to look through all the <comment>
##tags and find the <count> values sum the numbers.
##You can use the following links to test:
##http://py4e-data.dr-chuck.net/comments_1673515.xml
##http://py4e-data.dr-chuck.net/comments_42.xml


import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET

link = input('Enter ul: ')
html = urllib.request.urlopen(link).read().decode()
print('Retrieving', link)
print('Retrieved', len(html), 'characters')


#data calculation
coun = 0
summ = 0
data = ET.fromstring(html)
tags = data.findall('comments/comment')

for tag in tags:
    coun += 1
    summ += int(tag.find('count').text)

print('Count:', coun)
print('Sum:', summ)