#!/usr/bin/python
import sys
import urllib2
import json
import pprint

def list_signed(device):
	url = "https://api.ipsw.me/v4/device/" + device
	json_file = urllib2.urlopen(url)
	with open("signed.json",'wb') as output:
		output.write(json_file.read())

	data = json.load(open("signed.json"))
	i = 0
	with open("signed.json"):
		print("signed firmwares for %s:" % device)
		for i in range(0, len(data["firmwares"])):
			if data["firmwares"][i]["signed"] == True :
				print("%s - %s" % (data["firmwares"][i]["version"], data["firmwares"][i]["buildid"]))
			i+=1

def usage(tool):
	print("usage: %s <device>" % tool)

if __name__ == '__main__':
	argc = len(sys.argv)
	if argc < 2:
		usage(sys.argv[0])
		sys.exit(-1)
	elif argc == 2:
			device = sys.argv[1]
	else :
		usage(sys.argv[0])
		sys.exit(-1)
	list_signed(device)
