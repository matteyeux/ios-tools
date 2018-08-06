#!/usr/bin/python
import sys
import requests
import json
import urllib2
from clint.textui import progress

# extract IPSW filename from URL
def get_filename(url):
	for i in range(len(url)):
		if url[i] == '/':
  			position = i + 1
	return url[position:]

# download file
def dl(url, filename, sizeofile):
	# idk the size of the file
	if sizeofile == 0:
		dl_file = urllib2.urlopen(url)
		with open(filename,'wb') as output:
			output.write(dl_file.read())

	else :
		dl_file = requests.get(url, stream=True)
		with open(filename,'wb') as output:
			for chunk in progress.bar(dl_file.iter_content(chunk_size=1024), expected_size=(sizeofile/1024) + 1):
				if chunk:
					output.write(chunk)
					output.flush()

# download and parse json file
def parse_json(model, version):
	json_file = model + ".json"
	dl("https://api.ipsw.me/v4/device/" + model, json_file, 0)
	
	if version == None:
		data = json.load(open(json_file))
		with open(json_file):
			ios_version = data["firmwares"][0]["version"]
			buildid = data["firmwares"][0]["buildid"]
			url = data["firmwares"][0]["url"]
			size = data["firmwares"][0]["filesize"]

	
	else :
		data = json.load(open(json_file))
		i = 0
		ios_version = data["firmwares"][i]["version"]
		with open(json_file):
			while ios_version != version :
				ios_version = data["firmwares"][i]["version"]
				i += 1
			buildid = data["firmwares"][i]["buildid"]
			url = data["firmwares"][i]["url"]
			size = data["firmwares"][i]["filesize"]

	ipswfile = get_filename(url)
	print("[+] build ID : %s" % buildid)
	print("[+] IPSW : %s" % ipswfile)
	print("[+] URL : %s" % url)
	print("[+] size : %s" % size)
	
	dl(url, ipswfile, size)

def usage(toolname):
	print("usage: %s <model> [version]" % toolname)

if __name__ == '__main__':
	argv = sys.argv
	argc = len(argv)

	# if you don't specify a version
	# this tool will download the latest firmware for your device
	if argc == 2:
		device = argv[1]
		version = None
	elif argc == 3:
		device = argv[1]
		version = argv[2]
	else :
		usage(argv[0])
		sys.exit(-1)

	parse_json(device, version)
