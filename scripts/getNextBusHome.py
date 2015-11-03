#!/usr/bin/python
import urllib2
import json
import collections
import datetime

from dateutil.relativedelta import relativedelta

import dateutil.parser
import pytz

response = urllib2.urlopen('https://api.tfl.gov.uk/Line/u4/Arrivals?stopPointId=490006702N&app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&ids=u4')
html=response.read()
parsed=json.loads(html)

#for i in parsed["places"][0]["children"]:
#	print json.dumps(i["commonName"],indent=5,sort_keys=True)

#orderedparsed= collections.OrderedDict(sorted(parsed.timeToStation()))

parsed.sort()
utc = pytz.UTC
timenow = utc.localize(datetime.datetime.utcnow())
print
for i in parsed:
	#print str(datetime.timedelta(seconds=i["timeToStation"])) + " left"
	print i["timeToLive"]

	relative = relativedelta(dateutil.parser.parse(i["timeToLive"]),timenow) 
	print str(relative.minutes)+ " minute(s), " + str(relative.seconds) + " second(s)"
	print
#print json.dumps(parsed,indent=5,sort_keys=True)


#print json.dumps(parsed,indent=4,sort_keys=True)
