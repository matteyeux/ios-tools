"""
Simple snippet I use for Binary Ninja to apply some symbols
This code is for A13 SecureROM but you can use this command below
to generate symbols dict for any 64 bits iOS bootloader
./iBoot64Finder -f securerom.bin | grep locate | sed  's/\[locate_func]: /dict_f[\"/g' | sed 's/ =/"] =/g'
"""
dict_f = dict()

dict_f["_uart_init"] = 0x100002bec
dict_f["_image_load"] = 0x100001ca0
dict_f["_image4_load"] = 0x1000059dc
dict_f["_Img4DecodeInit"] = 0x100013d30
dict_f["_image_load_file"] = 0x10000af0c
dict_f["_image4_get_partial"] = 0x100004f28
dict_f["_Img4DecodeGetPayload"] = 0x100013260
dict_f["_image_create_from_memory"] = 0x10000b060
dict_f["_Img4DecodeEvaluateDictionaryProperties"] = 0x100013c14
dict_f["_Img4DecodeGetPropertyBoolean"] = 0x1000138ac
dict_f["_Img4DecodeGetPropertyData"] = 0x100013928
dict_f["_platform_quiesce_hardware"] = 0x100008aa8
dict_f["_platform_get_nonce"] = 0x1000077bc
dict_f["_platform_disable_keys"] = 0x1000073a8
dict_f["_DERParseSequence"] = 0x100015014
dict_f["_DERDecodeSeqInit"] = 0x100014ec0
dict_f["_DERDecodeSeqNext"] = 0x100014f7c
dict_f["_DERParseInteger"] = 0x100014dc4
dict_f["_DERImg4DecodePayload"] = 0x100012e14
dict_f["_DERImg4DecodeRestoreInfo"] = 0x100012bd0
dict_f["_DERImg4DecodeFindInSequence"] = 0x100012a8c
dict_f["_usb_core_start"] = 0x10000e154
dict_f["_usb_core_init"] = 0x10000df9c
dict_f["_mmu_kvtop"] = 0x100000548
dict_f["_memalign"] = 0x100010114
dict_f["_calloc"] = 0x10000fe68
dict_f["_strlen"] = 0x100011bd0
dict_f["_malloc"] = 0x10000fc90
dict_f["_memcpy"] = 0x100011770
dict_f["_memset"] = 0x1000119a0
dict_f["_bzero"] = 0x100011920
dict_f["_free"] = 0x10000fef4
dict_f["_panic"] = 0x100008f90
dict_f["_tlbi"] = 0x100000500

print("starting")
for function in bv.functions:
    for f in dict_f:
        if function.start == dict_f[f]:
            print(f"[i] {f} @ {hex(function.start)}")
            function.name = f
