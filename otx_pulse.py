import csv
import re
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import urllib3
urllib3.disable_warnings()

otx = OTXv2("your key",proxy_https="http://192.168.66.102:7890",proxy="http://192.168.66.102:7890")

def validatetitle(title):
  rstr = r"[\/\\\:\*\?\"\<\>\|]" # '/ \ : * ? " < > |'
  new_title = re.sub(rstr, "_", title) # 替换为下划线
  return new_title
all=otx.getall(limit=50,max_page=200000, max_items=1000000,iter=True)
for pulse in all:
    print('Found pulse with id {} and title {}'.format(pulse['id'],
                                                               pulse['name'].encode("utf-8")))
    indicator_data = pulse['indicators']  # Pull indicators from pulse
    event_title = pulse['name']  # Pull title from pulse
    created = pulse['created']  # Pull date/time from pulse
    reference = ''  # Pull reference from pulse if available
    if not reference:
        reference = 'No reference documented'
    else:
        reference = pulse['reference'][0]

    try:
        with open(f"/data/{validatetitle(event_title)}.txt", 'w', encoding="utf-8",newline='') as resultFile:
                wr = csv.writer(resultFile)
                wr.writerow(['##Found pulse with id {} and title {}'.format(pulse['id'],
                                                               pulse['name'].encode("utf-8"))])
                for i in pulse['indicators']:
                    result = [event_title, created, i['type'], i['indicator'], reference]
                    wr = csv.writer(resultFile, dialect='excel')
                    wr.writerow(result)
    except OSError:
        continue