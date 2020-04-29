from enum import Enum
from bitstring import BitArray
from sys import byteorder

class DataType(Enum):
    INT = {"byteBased": True, "size": 32, "id": "int"}
    FLOAT = {"byteBased": True, "size": 32, "id": "float"}
    DOUBLE = {"byteBased": True, "size": 64, "id": "float"}
    BYTE = {"byteBased": True, "size": 8, "id": "int"}
    WORD = {"byteBased": True, "size": 16, "id": "int"}
    DWORD = {"byteBased": True, "size": 32, "id": "int"}
    QWORD = {"byteBased": True, "size": 64, "id": "int"}
    HWORDO = {"byteBased": False, "size": 6, "id": "int"}
    WORDO = {"byteBased": False, "size": 12, "id": "int"}
    DWORDO = {"byteBased": False, "size": 24, "id": "int"}
    TWORDO = {"byteBased": False, "size": 36, "id": "int"}

class NumBase(Enum):
    DEC = {"base": 10, "mod": None, "prefix": "", "chars": "0123456789.-e", "reqSpace": False}  # supposed to raise errors if used in wrong places
    OCT = {"base": 8, "mod": 3, "prefix": "0o", "chars": "01234567", "reqSpace": True}
    HEX = {"base": 16, "mod": 4, "prefix": "0x", "chars": "0123456789abcdef", "reqSpace": True}
    BIN = {"base": 2, "mod": 1, "prefix": "0b", "chars": "01", "reqSpace": True}

class Endian(Enum):
    BIG = "be"
    LITTLE = "le"
    NATIVE = "ne"
    NONBYTE = ""

def C2toC1(bArr, signed):
    binStr = bArr.bin

    if binStr[0] == "0" or not signed:
        return bArr

    idx = binStr.rfind("1")

    binStrC1 = binStr[:idx]

    for i in range(idx, len(binStr), 1):
        if binStr[i] == "1":
            binStrC1 += "0"
        else:
            binStrC1 += "1"

    bArr = BitArray(bin=binStrC1)

    return bArr

def C1toC2(bArr, signed):
    binStr = bArr.bin

    if binStr[0] == "0" or not signed:
        return bArr

    idx = binStr.find("0")

    binStrC1 = binStr[:idx]

    for i in range(idx, len(binStr), 1):
        if binStr[i] == "0":
            binStrC1 += "1"
        else:
            binStrC1 += "0"

    bArr = BitArray(bin=binStrC1)

    return bArr

def C1toInt(bArr, signed):
    if bArr.bin[0] == "1":
        bArr.invert()
        val = bArr.uint
        if signed:
            return -val
        return val
    else:
        return bArr.uint

def MStoC2(bArr, signed):
    binStr = bArr.bin

    if binStr[0] == "0" or not signed:
        return bArr

    bArr.invert()
    bArr = C1toC2(bArr, signed)

    return bArr

def C2toMS(bArr, signed):
    return C2toC1(bArr, signed)

def MStoInt(bArr, signed):
    sign = bArr.bin[0]
    if sign == "1":
        bArr.invert()
    val = BitArray(bin=bArr.bin[1:]).uint
    if signed and sign == "1":
        return -val
    else:
        return val

class BinFormat(Enum):
    MS = {"toC2": MStoC2, "fromC2": C2toMS, "toInt": MStoInt}
    C1 = {"toC2": C1toC2, "fromC2": C2toC1, "toInt": C1toInt}
    C2 = 2

def binBaseSwitcher(bArr, baseIn, baseOut, endian, signed):
    if baseIn == baseOut:
        return bArr

    if endian == Endian.LITTLE:
        bArr.byteswap()

    if baseIn == BinFormat.C2:
        bArr = baseOut.value["fromC2"](bArr, signed)
    elif baseOut == BinFormat.C2:
        bArr = baseIn.value["toC2"](bArr, signed)
    else:
        bArr = baseOut.value["fromC2"](baseIn.value["toC2"](bArr, signed), signed)

    if endian == Endian.LITTLE:
        bArr.byteswap()

    return bArr

class Converter:
    def __init__(self, dictArgs):
        self.error = None
        self.mem = dictArgs["out"]["mem"]
        self.baseIn = dictArgs["in"]["base"]
        self.binFormatIn = dictArgs["in"]["binFormat"]
        self.signedIn = dictArgs["in"]["signed"]

        self.baseOut = dictArgs["out"]["base"]
        self.binFormatOut = dictArgs["out"]["binFormat"]
        self.signedOut = dictArgs["out"]["signed"]

        if self.mem.value["byteBased"]:
            self.endianIn = dictArgs["in"]["endian"]
            self.endianOut = dictArgs["out"]["endian"]

            if self.endianIn == Endian.NATIVE: self.endianIn = self.getNativeEndianness()
            if self.endianOut == Endian.NATIVE: self.endianOut = self.getNativeEndianness()

        else:
            self.endianIn = Endian.NONBYTE
            self.endianOut = Endian.NONBYTE

    @staticmethod
    def getNativeEndianness():
        if byteorder == "big":
            return Endian.BIG
        else:
            return Endian.LITTLE

    def isSeparatorRequired(self):
        return self.baseIn.value["reqSpace"]

    def isNum(self, string):
        for c in string:
            if c not in self.baseIn.value["chars"]:
                return False
        return True

    def __toInt(self, bArr, endian, signed, binFormat):
        try:
            if self.mem is DataType.DOUBLE or self.mem is DataType.FLOAT:
                if binFormat == BinFormat.C2:
                    if signed:
                        if endian == Endian.BIG: return bArr.floatbe
                        if endian == Endian.LITTLE: return bArr.floatle
                    else:
                        raise Exception("Unsigned format is not supported for floating point numbers")
                else:
                    raise Exception("C1 and MS formats are not supported for floating point numbers")
            else:
                if binFormat == BinFormat.C2:
                    if signed:
                        if not self.mem.value["byteBased"]: return bArr.int
                        if endian == Endian.BIG: return bArr.intbe
                        if endian == Endian.LITTLE: return bArr.intle
                    else:
                        if not self.mem.value["byteBased"]: return bArr.uint
                        if endian == Endian.BIG: return bArr.uintbe
                        if endian == Endian.LITTLE: return bArr.uintle
                else:
                    if endian == Endian.LITTLE:
                        bArr.byteswap()
                    return binFormat.value["toInt"](bArr, signed)
        except Exception as e:
            self.error = str(e)
            return None

    def getDecBitArray(self, val, endian, signed, binFormat):
        # [u]int[ne|be|le]:[8|16|32|64]=12
        # float[ne|be|le]:[32|64]=12.34
        val = str(val)
        strSign = ""
        if self.mem.value["id"] == "int":
            if "." in val:
                val = val[:val.index(".")]
            if not signed:
                if val[0] == "-":
                    val = val[1:]
                strSign = "u"

        if binFormat == BinFormat.C2:
            return BitArray(strSign + self.mem.value["id"] + endian.value + ":" + str(self.mem.value["size"]) + "=" + str(val))
        else:
            if binFormat == BinFormat.C1:
                bArr = BitArray(strSign+self.mem.value["id"]+endian.value+":"+str(self.mem.value["size"])+"="+str(val))
            else:
                bArr = BitArray(strSign+self.mem.value["id"]+":"+str(self.mem.value["size"] - 1)+"="+str(val))

            return binBaseSwitcher(bArr, BinFormat.C2, binFormat, endian, signed)

    def getBinBitArray(self, val, endian, numBase, binFormat):
        # [0b|0x|0o]1234
        val = str(val)
        binSize = numBase.value["mod"]*len(val)
        bArr = BitArray(numBase.value["prefix"]+val)

        if endian == Endian.LITTLE:
            bArr.byteswap()

        binData = bArr.bin

        if binFormat == BinFormat.C2:
            bArr = BitArray(NumBase.BIN.value["prefix"] + binData[0] * (self.mem.value["size"] - binSize) + binData)
        elif binFormat == BinFormat.C1:
            bArr = BitArray(NumBase.BIN.value["prefix"] + binData[0] * (self.mem.value["size"] - binSize) + binData)
        elif binFormat == BinFormat.MS:
            sign = binData[0]
            binSize += 1
            bArr = BitArray(bin=binData[1:])
            bArr.invert()

            binData = bArr.bin

            bArr = BitArray(NumBase.BIN.value["prefix"] + sign + binData[0] * (self.mem.value["size"] - binSize) + binData)

        if endian == Endian.LITTLE:
            bArr.byteswap()

        return bArr

    def toInt(self, val):
        try:
            if self.baseIn == NumBase.DEC:
                bArr = self.getDecBitArray(val, self.endianIn, self.signedIn, self.binFormatIn)
            else:
                bArr = self.getBinBitArray(val, self.endianIn, self.baseIn, self.binFormatIn)

            return self.__toInt(bArr, self.endianIn, self.signedIn, self.binFormatIn)
        except Exception as e:
            self.error = str(e)
            return None

    def applyFormatting(self, val):
        try:
            bArr = self.getDecBitArray(val, self.endianIn, self.signedIn, self.binFormatIn)  # init with IN parameters
            valOut = self.__toInt(bArr, self.endianOut, self.signedOut, self.binFormatIn)  # get int with OUT parameters but keep binFormat

            if self.baseOut == NumBase.DEC:
                return valOut
            else:
                bArr = self.getDecBitArray(valOut, self.endianIn, self.signedIn, self.binFormatIn)  # get BitArray from int
                bArrOut = binBaseSwitcher(bArr, self.binFormatIn, self.binFormatOut, self.endianOut, self.signedOut)  # apply OUT params to BitArray
                if self.baseOut == NumBase.BIN:
                    return bArrOut.bin
                if self.baseOut == NumBase.HEX:
                    return bArrOut.hex
                if self.baseOut == NumBase.OCT:
                    return bArrOut.oct
        except Exception as e:
            self.error = str(e)
            return None
