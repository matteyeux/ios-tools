#!/usr/bin/python
# code from https://github.com/kennytm/Miscellaneous/blob/master/ipsw_decrypt.py
import os
import sys
from struct import Struct
import subprocess
#from lzss import decompressor

tag_unpack = Struct('<4s2I').unpack
kbag_unpack = Struct('<2I16s').unpack

def get_image_type(filename):
	with open(filename, 'rb') as file:
		magic = file.read(4)
		if magic != b'3gmI':
			return None

		file.seek(12, os.SEEK_CUR)
		while True:
			tag = file.read(12)
			if not tag:
				break
			(img_type, total_len, data_len) = tag_unpack(tag)
			data_len &= ~15
			return img_type

def decrypt_img3(input, output, key, iv, openssl='openssl'):
	image_type = get_image_type(input)
	if image_type == None:
		print("[e] %s is not an IMG3 file" % input)
		sys.exit(1)

	with open(input, 'rb') as f:
		f.seek(20, os.SEEK_CUR)

		while True:
			tag = f.read(12)
			if not tag:
				break
			(tag_type, total_len, data_len) = tag_unpack(tag)
			data_len &= ~15

			if tag_type == b'ATAD':
				print("[x] decrypting %s to %s..." % (input, output))
				aes_len = str(len(key) * 4)
				# OUCH!
				# Perhaps we an OpenSSL wrapper for Python 3.1
				# (although it is actually quite fast now)
				p = subprocess.Popen([openssl, 'aes-' + aes_len + '-cbc', '-d', '-nopad', '-K', key, '-iv', iv, '-out', output], stdin=subprocess.PIPE)
				bufsize = 16384
				buf = bytearray(bufsize)

				while data_len:
					bytes_to_read = min(data_len, bufsize)
					data_len -= bytes_to_read
					if bytes_to_read < bufsize:
						del buf[bytes_to_read:]
					f.readinto(buf)
					p.stdin.write(buf)
				p.stdin.close()

				if p.wait() != 0 or not os.path.exists(output):
					print("[e] Decryption failed")
				return

			else:
				f.seek(total_len - 12, os.SEEK_CUR)

		print("[w] Nothing was decrypted from %s" % input)
