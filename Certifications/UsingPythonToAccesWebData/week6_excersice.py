##read the JSON data from that URL using urllib and then parse and extract
##the comment counts from the JSON data, compute the sum of the numbers in the file

import json
from urllib.request import urlopen

url = input("type URL: ")

response = urlopen(url)

data_json = json.loads(response.read())

comments = data_json["comments"]

final_count = 0

for i in comments:
    final_count = i["count"] + final_count

print(final_count)