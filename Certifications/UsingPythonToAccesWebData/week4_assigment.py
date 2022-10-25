# Find the link at position 18 (the first name is 1). Follow that link.}
# Repeat this process 7 times

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter link: ')
times = int(input('Enter times: '))
line = int(input('Enter position: '))

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
print('Retrieving: %s' % url)

for i in range(0, times):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup('a')
    coun = 0
    pos = 0

    for tag in tags:
        pos += 1
        if pos == line:
            print('Retrieving: %s' % str(tag.get('href', None)))
            url = str(tag.get('href', None))
            pos = 0
            break