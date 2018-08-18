#!/usr/bin/python
import sys
import os
import mechanize
import json
import urllib2
from bs4 import BeautifulSoup

class colors :
	GREEN = '\033[92m'
	ENDG = '\033[0m'

def parse_iphonewiki(url2parse, img_type):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	html = br.open(url2parse).read()
	soup = BeautifulSoup(html, 'html.parser')

	keypage = list()
	keypage =   ["rootfs-key", "updateramdisk-iv", "updateramdisk-key",
				"restoreramdisk-iv", "restoreramdisk-key", "applelogo-iv",
				"applelogo-key", "batterycharging0-iv", "batterycharging0-key",
				"batterycharging1-iv", "batterycharging1-key", "batteryfull-iv",
				"batteryfull-key", "batterylow0-iv", "batterylow0-key",
				"batterylow1-iv", "batterylow1-key", "devicetree-iv",
				"devicetree-key", "glyphcharging-iv", "glyphcharging-key",
				"glyphplugin-iv", "glyphplugin-key",
				"ibec-iv", "ibec-key", "iboot-iv", "iboot-key",
				"ibss-iv", "ibss-key", "kernelcache-iv",
				"kernelcache-key", "llb-iv", "llb-key",
				"recoverymode-iv", "recoverymode-key",
				"sepfirmware-iv", "sepfirmware-key"]
	j = 0
	key = ""
	for i in range(0, len(keypage)):
		for hit in soup.findAll(attrs={'id': "keypage-" + keypage[i]}):
			if img_type == None:
				bl = keypage[i]
				print(bl + ":\n\t %s" % hit.text)
			elif img_type != None and img_type == keypage[i].split('-')[0]:
				j += 1
				key += hit.text
				if j == 2:
					return key
# Used to 'convert' version -> build ID and vice versa
# I just parse firmwares.json on api.ipsw.me
def version_or_build(model, version, build):
	get_buildid = False
	get_version = False
	json_file = urllib2.urlopen("https://api.ipsw.me/v4/device/" + model)
	with open(model, 'wb') as output:
		output.write(json_file.read())

	data = json.load(open(model))

	if build is None:
		get_buildid = True
	elif version is None:
		get_version = True
	i = 0

	with open(model):
		while True:
			if get_buildid is True:
				result = data["firmwares"][i]["buildid"]
				ios_version = data["firmwares"][i]["version"]
				if ios_version == version:
					break

			elif get_version is True:
				buildid = data["firmwares"][i]["buildid"]
				result= data["firmwares"][i]["version"]
				if build == buildid:
					break
			i += 1
	os.remove(model)
	return result

# we need to get the codename of the firmware to access the URL
def get_codename(device, version, build):
	version = version.split('.')[0] + ".x"
	url = "https://www.theiphonewiki.com/wiki/Firmware_Keys/" + version

	br = mechanize.Browser()
	br.set_handle_robots(False)
	html = br.open(url).read()
	soup = BeautifulSoup(html, 'html.parser')

	i = 0
	checker = False
	data = soup.findAll('a')
	device = "(%s)" % device

	for hit in data:

		# some beta may have the same codename, first in first out
		if checker is False:
			try:
				if data[i].get('href').split('_')[1] == build and data[i].get('href').split('_')[2] == device:
					checker = True
					codename = data[i].get('href').split('/')[2].split('_')[0]
					return codename
			except:
				pass
		i += 1

def usage(toolname):
	print("usage: " + toolname + " [args]")
	print(" -d <device>")
	print(" -i <version>")
	print(" -b <build ID>")
	print(" -c <codename>")

if __name__ == '__main__':
	argc = len(sys.argv)
	argv = sys.argv
	check = 0
	codename = None
	ios_v = None
	set_ios_version = None

	if argc <= 5:
		usage(argv[0])
		sys.exit(-1)

	for i in range(0,argc):
		if argv[i] == "-i":
			ios_v = argv[i + 1]
			set_ios_version = True
		elif argv[i] == "-b" :
			build = argv[i + 1]
		elif argv[i] == "-d" :
			device = argv[i + 1]
		elif argv[i] == "-c":
			codename = argv[i + 1]

	if set_ios_version is True:
		build = version2build(device, ios_v)
	else:
		ios_v = version_or_build(device, ios_v, build)

	if codename is None:
		codename = get_codename(device, ios_v, build)

	print("[+] build ID : " + build)

	if codename is None:
		codename = get_codename(device, ios_v, build)

	url = "https://www.theiphonewiki.com/wiki/" + codename + "_" + build +  "_" + "(" + device + ")"
	print("[+] grabbing keys from " + url)
	parse_iphonewiki(url, None)