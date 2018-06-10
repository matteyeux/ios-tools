#!/usr/bin/python
import sys
from urllib.request import urlopen
import json
import pprint

def list_signed(device):
	json_file = urlopen("https://api.ineal.me/tss/all/all")
	with open("signed.json",'wb') as output:
		output.write(json_file.read())

	data = json.load(open("signed.json"))
	i = 0
	with open("signed.json"):
		print("signed firmwares for %s:" % device)
		for i in range(0, len(data[device]["firmwares"])):
			if data[device]["firmwares"][i]["signing"] == True :
				print("%s - %s" % (data[device]["firmwares"][i]["version"], data[device]["firmwares"][i]["build"]))
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
