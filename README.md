# ios-tools
Python scripts for iOS stuff

### signed.py
Check for signing status
Based on [iNeal](https://api.ineal.me/tss/docs) and [IPSW.me](https://ipsw.me/api/ios/docs/2.1/Firmware) APIs

`usage: ./signed.py <device>`

example :
```
$ ./signed.py iPhone8,1
signed firmwares for iPhone8,1:
11.2.6 - 15D100
```

### ipsw-dl.py
Download and IPSW file

`usage: ./ipsw-dl.py <model> [version]`
example :
```
$ ./ipsw-dl.py iPhone8,1 11.1.2
[+] build ID : 15B202
[+] IPSW : iPhone_4.7_11.1.2_15B202_Restore.ipsw
[+] URL : http://appldnld.apple.com/ios11.1.2/091-46844-20171116-4F99614A-C9C7-11E7-8C47-8AE0F451CBCD/iPhone_4.7_11.1.2_15B202_Restore.ipsw
[+] size : 2711452941
[################################] 397609/2647904 - 00:02:03
done
```
### scrapkeys.py
Python script used to grab iOS Firmware keys on https://www.theiphonewiki.com
![demo](screen.png)

`usage: ./scrap.py -c [codename] -d [device] -i [version]`

You need :
- **Codename** of the iOS version
- **Device** model
- **iOS** version

eg : `python scrap.py -c Dubois -i 10.2.1 -d iPad4,7` <br>
You can use build ID instead of iOS version for betas.

I'm still looking for a way to not use codename, feel free to contribute. 

### Dependencies
- Python [2.7](https://python.org) and pip
- mechanize
- BeautifulSoup4

Twitter : [matteyeux](https://twitter.com/matteyeux)
