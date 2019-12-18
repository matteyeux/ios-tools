#!/usr/bin/env python

import json
import os
import sys
import re
import requests
from pyquery import PyQuery

wiki = "https://www.theiphonewiki.com"


# eg iPhone9,3
def get_json_data(model):
    url = "https://api.ipsw.me/v4/device/" + model
    print("url : %s" % url)
    resp = requests.get(url=url)
    return resp.json()


def get_firmware_url(json_data, buildid):
    for i in range(0, len(json_data['firmwares'])):
        if json_data['firmwares'][i]['buildid'] == buildid:
            return json_data['firmwares'][i]['url']
    return None


def get_ios_vers(json_data, buildid):
    for i in range(0, len(json_data['firmwares'])):
        if json_data['firmwares'][i]['buildid'] == buildid:
            return json_data['firmwares'][i]['version']
    return None


def get_build_list(json_data):
    builds = []
    for i in range(len(json_data['firmwares'])):
        builds.append(json_data['firmwares'][i]['buildid'])
    return builds


def getFirmwareKeysPage(device, buildnum):
    r = requests.get(wiki+"/w/index.php", params={'search': buildnum+" "+device})
    html = r.text
    link = re.search("\/wiki\/.*_"+buildnum+"_\("+device+"\)",html)
    try:
        pagelink = wiki+link.group()
        return pagelink
    except:
        return None


def getkeys(json_data, device, buildnum):
    rsp = {}
    oldname = None
    pagelink = getFirmwareKeysPage(device, buildnum)
    if pagelink is None:
        return None

    html = requests.get(pagelink).text
    rsp["build"] = buildnum
    rsp["device"] = device
    rsp["download"] = get_firmware_url(json_data, buildnum)

    pq = PyQuery(html)
    images = {}
    for span in pq.items('span.mw-headline'):
        name = span.text()

        if name.lower() == "sep-firmware":
            name = "sepfirmware"

        fname = span.parent().next("* > span.keypage-filename").text()

        name = name.lower().split('\xa0')[0]
        if oldname == name:
            name += "2"

        iv = span.parent().siblings("*>*>code#keypage-"+name.lower()+"-iv").text()
        key = span.parent().siblings("*>*>code#keypage-"+name.lower()+"-key").text()
 
        if "iBEC" in fname or "iBSS" in fname:
            fname_path = "Firmware/dfu/" + fname
        else:
            fname_path = "Firmware/all_flash/" + fname

        if iv != "" and "Unknown" not in iv:
            images[fname_path] = iv + key
        oldname = name
    rsp["images"] = images
    rsp["ios_vers"] = get_ios_vers(json_data, buildnum)
    return json.dumps(rsp, indent=4)


def create_gm_config_file(build_dir, data):
    with open(build_dir + '/gm.config', 'w') as gm:
        gm.write(data)


# this one returns the build dir
# where to create file
def setup_gm_config(device, build):
    device_dir = device
    build_dir = device_dir + "/" + build

    print(device_dir)
    print(build_dir)
    if not os.path.exists(device_dir):
        os.makedirs(device_dir)

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    return build_dir


def does_gm_config_exist(device, build):
    gm_config_path = device + "/" + build + "/gm.config"
    if os.path.isfile(gm_config_path):
        return True
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("wiki.py <device> <build>")
        sys.exit(1)

    keys = None   
    build_list = []
    json_data = get_json_data(sys.argv[1])

    if len(sys.argv) == 2:
        build_list = get_build_list(json_data)
    else:
        build_list.append(sys.argv[2])

    for i in range(len(build_list)):
        if does_gm_config_exist(sys.argv[1], build_list[i]) is False:
            keys = getkeys(json_data, sys.argv[1], build_list[i])

        if keys is not None:
            config_dir = setup_gm_config(sys.argv[1], build_list[i])
            create_gm_config_file(config_dir, keys)
            print(keys)
