import base64
import zlib
import binascii
import uu
import quopri
from encodings import idna
import locale

listOfTextEncodings = (
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

listOfBitOperations = (
    "base64",
    "hex",
    "quopri",
    "uu",
    "gzip"
    "idna"
)

def textEncodingBeautifier(idx: int):
    strOut = listOfTextEncodings[idx].replace("_", " ")
    return strOut

def getEncoding(string):
    label = string.replace(" ", "_")
    return label

def toHex(string, encoding):
    if encoding == "hex":
        return binascii.a2b_hex(string)
    if encoding == "base64":
        return binascii.a2b_base64(string)
    if encoding == "quopri":
        return binascii.a2b_qp(string)

def fromHex(byteStr, encoding):
    if encoding == "hex":
        return binascii.b2a_hex(byteStr)
    if encoding == "base64":
        return binascii.b2a_base64(byteStr)
    if encoding == "quopri":
        return binascii.b2a_qp(byteStr)

def gzipCompress(string, level: int = 9):
    return zlib.compress(string, level)

def gzipDecompress(string):
    return zlib.decompress(string)

def base64Encode(string):
    b64Bytes = toHex(string, "base64")
    return base64.b64encode(b64Bytes)

def base64Decode(b64String):
    b64Bytes = base64.b64decode(b64String)
    return fromHex(b64Bytes, "base64")

def uuEncode(fileIn, fileOut, name: str, mode: str, backtick: bool):
    uu.encode(fileIn, fileOut, name=name, mode=mode, backtick=backtick)

def uuDecode(fileIn, fileOut, mode):
    uu.encode(fileIn, fileOut, mode=mode)

def quopriEncode(string, quotetabs: bool = False, header: bool = False):
    qpBytes = toHex(string, "quopri")
    return quopri.encodestring(qpBytes, quotetabs, header)

def quopriDecode(qpString, header=False):
    qpBytes = quopri.decodestring(qpString)
    return fromHex(qpBytes, "quopri")

def toIdnaLabel(string):
    return idna.nameprep(string)

def fromIdnaLabel(string, encoding):
    if encoding == "ascii":
        return idna.ToASCII(string)
    if encoding == "unicode":
        return idna.ToUnicode(string)



