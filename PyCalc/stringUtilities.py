import base64
import binascii
import locale
import quopri
import zlib

listOfTextEncodings = (
    "locale",
    "AoB",
    "ascii",
    "big5",
    "big5hkscs",
    "cp037",
    "cp273",
    "cp424",
    "cp437",
    "cp500",
    "cp720",
    "cp737",
    "cp775",
    "cp850",
    "cp852",
    "cp855",
    "cp856",
    "cp857",
    "cp858",
    "cp860",
    "cp861",
    "cp862",
    "cp863",
    "cp864",
    "cp865",
    "cp866",
    "cp869",
    "cp874",
    "cp875",
    "cp932",
    "cp949",
    "cp950",
    "cp1006",
    "cp1026",
    "cp1125",
    "cp1140",
    "cp1250",
    "cp1251",
    "cp1252",
    "cp1253",
    "cp1254",
    "cp1255",
    "cp1256",
    "cp1257",
    "cp1258",
    "cp65001",
    "euc_jp",
    "euc_jis_2004",
    "euc_jisx0213",
    "euc_kr",
    "gb2312",
    "gbk",
    "gb18030",
    "hz",
    "iso2022_jp",
    "iso2022_jp_1",
    "iso2022_jp_2",
    "iso2022_jp_2004",
    "iso2022_jp_3",
    "iso2022_jp_ext",
    "iso2022_kr",
    "latin_1",
    "iso8859_2",
    "iso8859_3",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_11",
    "iso8859_13",
    "iso8859_14",
    "iso8859_15",
    "iso8859_16",
    "johab",
    "koi8_r",
    "koi8_t",
    "koi8_u",
    "kz1048",
    "mac_cyrillic",
    "mac_greek",
    "mac_iceland",
    "mac_latin2",
    "mac_roman",
    "mac_turkish",
    "ptcp154",
    "shift_jis",
    "shift_jis_2004",
    "shift_jisx0213",
    "utf_32",
    "utf_32_be",
    "utf_32_le",
    "utf_16",
    "utf_16_be",
    "utf_16_le",
    "utf_7",
    "utf_8",
    "utf_8_sig"
)

bitOperations = {
    "None": {"encode": lambda s: s, "decode": lambda s: s},
    "Ascii85": {"encode": lambda s: base64.a85encode(s), "decode": lambda s: base64.a85decode(s)},
    "Base16": {"encode": lambda s: base64.b16encode(s), "decode": lambda s: base64.b16decode(s)},
    "Base32": {"encode": lambda s: base64.b32encode(s), "decode": lambda s: base64.b32decode(s)},
    "Base64": {"encode": lambda s: base64.b64encode(s), "decode": lambda s: base64.b64decode(s)},
    "Base85": {"encode": lambda s: base64.b85encode(s), "decode": lambda s: base64.b85decode(s)},
    "GZip": {"encode": lambda s: zlib.compress(s), "decode": lambda s: zlib.decompress(s)},
    "Quopri": {"encode": lambda s: quopri.encodestring(s), "decode": lambda s: quopri.decodestring(s)},
    "U Encoding": {"encode": lambda s: binascii.b2a_uu(s), "decode": lambda s: binascii.a2b_uu(s)}
}

def textEncodingBeautifier(idx: int):
    strOut = listOfTextEncodings[idx].replace("_", " ")
    return strOut

def getEncoding(string):
    label = string.replace(" ", "_")
    return label

def convert(strIn: str, codeIn: str, codeOut: str, opIn: str = "None", opOut: str = "None", err: str = "replace"):
    strIn = bitOperations[opIn]["decode"](strIn)

    if codeIn == "locale":
        vCodeIn = locale.getlocale()[1]
    else:
        vCodeIn = codeIn

    if codeOut == "locale":
        vCodeOut = locale.getlocale()[1]
    else:
        vCodeOut = codeOut

    if codeIn == "AoB":
        bytesIn = bytearray.fromhex(strIn)
    else:
        bytesIn = strIn.encode(vCodeIn, err)

    if vCodeOut == "AoB":
        strOut = str(bytesIn.hex())
    else:
        strOut = bytesIn.decode(vCodeOut, err)

    return bitOperations[opOut]["encode"](strOut)
