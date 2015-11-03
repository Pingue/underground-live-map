import urllib2
import json

response = urllib2.urlopen('https://api.tfl.gov.uk/Place?lat=51.5465906&lon=-0.4761759&radius=200&&app_id=cd00a446&app_key=bb862cf9b6f46d80f1c4e2818446b681&includeChildren=True')
html=response.read()
parsed=json.loads(html)

for i in parsed["places"]:
	print json.dumps(i,indent=5,sort_keys=True)



#print json.dumps(parsed["places"],indent=5,sort_keys=True)
#print json.dumps(parsed,indent=4,sort_keys=True)
