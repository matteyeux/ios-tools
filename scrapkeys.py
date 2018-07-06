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

def parse_iphonewiki(url2parse):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	html = br.open(url2parse).read()
	soup = BeautifulSoup(html, 'html.parser')

	keypage = list()
	keypage = ["keypage-rootfs-key", "keypage-updateramdisk-iv", "keypage-updateramdisk-key", 
		"keypage-restoreramdisk-iv", "keypage-restoreramdisk-key", "keypage-applelogo-iv", 
		"keypage-applelogo-key", "keypage-batterycharging0-iv", "keypage-batterycharging0-key",
		"keypage-batterycharging1-iv", "keypage-batterycharging1-key", "keypage-batteryfull-iv",
		"keypage-batteryfull-key", "keypage-batterylow0-iv", "keypage-batterylow0-key",
		"keypage-batterylow1-iv", "keypage-batterylow1-key", "keypage-devicetree-iv",
		"keypage-devicetree-key", "keypage-glyphplugin-iv", "keypage-glyphplugin-key",
		"keypage-ibec-iv", "keypage-ibec-key", "keypage-iboot-iv", "keypage-iboot-key",
		"keypage-ibss-iv", "keypage-ibss-key", "keypage-kernelcache-iv",
		"keypage-kernelcache-key", "keypage-llb-iv", "keypage-llb-key",
		"keypage-recoverymode-iv", "keypage-recoverymode-key",
		"keypage-sepfirmware-iv", "keypage-sepfirmware-key"]
	
	for i in range(0, len(keypage)) :
		for hit in soup.findAll(attrs={'id' : keypage[i]}):
			bl = keypage[i]
			print(bl[8:] + ":\n\t" + colors.GREEN + hit.text + colors.ENDG)

# Used to 'convert' version -> build ID
# I just parse firmwares.json on api.ipsw.me
def version2build(model, version):
	json_file = urllib2.urlopen("https://api.ipsw.me/v4/device/" + model)
	with open(model, 'wb') as output:
		output.write(json_file.read())

	data = json.load(open(model))

	i = 0
	ios_version = data["firmwares"][i]["version"]
	with open(model):
		while ios_version != version :
			ios_version = data["firmwares"][i]["version"]
			buildid = data["firmwares"][i]["buildid"]
			i += 1
	os.remove(model)
	return buildid

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

	if argc <= 5:
		usage(argv[0])
		sys.exit(-1)

	for i in range(0,argc):
		if argv[i] == "-i":
			ios_v = argv[i + 1]
			check = 1
		elif argv[i] == "-b" :
			build = argv[i + 1]
		elif argv[i] == "-d" :
			device = argv[i + 1]
		elif argv[i] == "-c":
			codename = argv[i + 1]

	if check == 1: 
		build = version2build(device, ios_v)

	print("[+] build ID : " + build)

	if codename == None:
		codename = get_codename(device, ios_v, build)

	url = "https://www.theiphonewiki.com/wiki/" + codename + "_" + build +  "_" + "(" + device + ")"
	print("[+] grabbing keys from " + url)
	parse_iphonewiki(url)