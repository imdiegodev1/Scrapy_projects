##The exercise consists of visiting the page "http://py4e-data.dr-chuck.net/comments_1673513.html"
##and obtaining the sum of all the comments in the table.

import urllib.request, urllib.parse, urllib.error #import url library
from bs4 import BeautifulSoup

link = urllib.request.urlopen('http://py4e-data.dr-chuck.net/comments_1673513.html')

soup = BeautifulSoup(link, 'html.parser')


items = [
    item.get_text(strip=True) for item in soup.find_all(class_="comments")
]

x = 0

for i in items:
    x = x + int(i)

print(x)