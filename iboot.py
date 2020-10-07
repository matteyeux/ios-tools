#!/usr/bin/python3
"""
Simple script to get the base address of a 64 bits iBoot.
"""
import sys

def usage():
    print(f"usage : {sys.argv[0]} iBoot")


def main():
    if len(sys.argv) != 2:
        usage()
        return 1

    with open(sys.argv[1], 'rb') as iboot:
        iboot.seek(0x280)
        iboot_version = iboot.read(20)

        try:
            print(iboot_version.decode('utf-8'))
        except UnicodeDecodeError:
            print(f"{sys.argv[1]} does not seem decrypted or is not supported")
            return -1

        major_version = iboot_version.decode('utf-8').split('-')[1].split('.')[0]

        # since iOS 14~b1 base address location has changed
        # so we need this check to know where to look at
        if int(major_version) >= 6603:
            iboot.seek(0x300)
        else:
            iboot.seek(0x318)

        iboot_base = iboot.read(5)
        iboot_base_addr = int.from_bytes(iboot_base, byteorder='little')
        print(f"Base address : {hex(iboot_base_addr)}")


if __name__ == '__main__':
    main()
