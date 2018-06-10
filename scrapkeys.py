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
			# print(hit.text)

# Used to 'convert' version -> build ID
# I just parse firmwares.json on api.ipsw.me
def version2build(model, version):
	json_file = urllib2.urlopen("https://api.ipsw.me/v2.1/firmwares.json")
	with open("firmwares.json",'wb') as output:
		output.write(json_file.read())

	data = json.load(open("firmwares.json"))

	i = 0
	ios_version = data["devices"][model]["firmwares"][i]["version"]
	with open("firmwares.json"):
		while ios_version != version :
			ios_version = data["devices"][model]["firmwares"][i]["version"]
			buildid = data["devices"][model]["firmwares"][i]["buildid"]
			# print(ios_version)
			# print(buildid)
			i += 1
	os.remove("firmwares.json")
	return buildid

# python scrap.py -c Dubois -i 10.2.1 -d iPad4,7
def usage(toolname):
	print("usage: " + toolname + " -c [codename] -d [device] -i [version]")

if __name__ == '__main__':
	argc = len(sys.argv)
	argv = sys.argv
	check = 0
	if argc != 7:
		usage(argv[0])
		sys.exit(-1)

	for i in range(0,argc):
		if argv[i] == "-c":
			codename = argv[i + 1]
		elif argv[i] == "-i":
			ios_v = argv[i + 1]
			check = 1
		elif argv[i] == "-b" :
			build = argv[i + 1]
		elif argv[i] == "-d" :
			device = argv[i + 1]

	if check == 1: 
		build = version2build(device, ios_v)
	print("[+] build ID : " + build)

	url = "https://www.theiphonewiki.com/wiki/" + codename + "_" + build +  "_" + "(" + device + ")"
	print("[+] grabbing keys from " + url)
	parse_iphonewiki(url)