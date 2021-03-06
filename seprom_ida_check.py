# Compare Yui's plugin with the binja one to make sure everything's working
# 
dict_f = {}
dict_f["_bzero"] = 0x240002fd0
dict_f["_ccn_cmp"] = 0x24000ddac
dict_f["_ccn_sub"] = 0x24000eee4
dict_f["_reload_cache"] = 0x2400056bc
dict_f["_DEROiCompare"] = 0x240011174
dict_f["_DERParseInteger"] = 0x240010d44
dict_f["_verify_pkcs1_sig"] = 0x240011fc4
dict_f["_DERParseSequence"] = 0x240010f0c
dict_f["_DERImg4DecodePayload"] = 0x240011450
dict_f["_Img4DecodeGetPayload"] = 0x240011844
dict_f["_verify_chain_signatures"] = 0x240012640
dict_f["_DERImg4DecodeFindInSequence"] = 0x2400111c0
dict_f["_DERDecodeItemPartialBufferGetLength"] = 0x240010a48
dict_f["_Img4DecodeEvaluateDictionaryProperties"] = 0x240011dec
dict_f["_DERImg4DecodeParseManifestProperties"] = 0x240011730
dict_f["_Img4DecodeGetPropertyBoolean"] = 0x240011ab4
dict_f["_Img4DecodeCopyPayloadDigest"] = 0x24001187c
dict_f["__Img4DecodeGetPropertyData"] = 0x240011b8c
dict_f["_DERImg4DecodeFindProperty"] = 0x240011658
dict_f["_DERDecodeSeqContentInit"] = 0x240010e88
dict_f["_DERImg4DecodeProperty"] = 0x240011564
dict_f["_DERParseBitString"] = 0x240010cc8
dict_f["_boot_check_panic"] = 0x240000d18
dict_f["_DERDecodeSeqNext"] = 0x240010ea4
dict_f["_ccdigest_update"] = 0x24000e29c
dict_f["_DERParseBoolean"] = 0x240010d08
dict_f["_Img4DecodeInit"] = 0x240011ee4
dict_f["_ccdigest_init"] = 0x24000e258
dict_f["_DERImg4Decode"] = 0x2400112c8
dict_f["__parse_chain"] = 0x24001247c
dict_f["_image4_load"] = 0x240009b1c
dict_f["_cchmac_init"] = 0x24000e530
dict_f["_ccn_add"] = 0x24000ea50
dict_f["_cc_muxp"] = 0x2400109f4
dict_f["_memcpy"] = 0x240004650
dict_f["_ccn_n"] = 0x240010a14
for function in bv.functions:
    for f in dict_f:
        if f == function.name:
            if dict_f[f] == function.start:
                print(f"good for {f}")
            else:
                log_error(f"bad for {f}")
     
