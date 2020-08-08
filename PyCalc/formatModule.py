from sys import byteorder

from bitstring import BitArray, CreationError, InterpretError
from enum import Enum


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
    QWORDO = {"byteBased": False, "size": 48, "id": "int"}

class NumBase(Enum):
    DEC = {"base": 10, "mod": None, "prefix": "", "chars": "0123456789.-e"}  # supposed to raise errors if used in wrong places
    OCT = {"base": 8, "mod": 3, "prefix": "0o", "chars": "01234567"}
    HEX = {"base": 16, "mod": 4, "prefix": "0x", "chars": "0123456789abcdef"}
    BIN = {"base": 2, "mod": 1, "prefix": "0b", "chars": "01"}

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
    C2 = None

class ConvertionException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

class Converter:
    def __init__(self, baseIn, baseOut, binFormat, memSize, endianness, signed):
        self.error = None
        self.mem = memSize
        self.baseIn = baseIn
        self.baseOut = baseOut
        self.binFormat = binFormat
        self.signed = signed
        
        if self.mem.value["byteBased"]:
            if endianness == Endian.NATIVE:
                self.endian = self.getNativeEndianness()
            else:
                self.endian = endianness
        else:
            self.endian = Endian.NONBYTE

    @staticmethod
    def getNativeEndianness():
        if byteorder == "big":
            return Endian.BIG
        else:
            return Endian.LITTLE

    @staticmethod
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
                        raise ConvertionException("Unsigned format is not supported for floating point numbers")
                else:
                    raise ConvertionException("C1 and MS formats are not supported for floating point numbers")
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
        except ConvertionException:
            raise
        except CreationError as e:
            raise ConvertionException(e.msg)

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
        try:
            if binFormat == BinFormat.C2:
                return BitArray(strSign + self.mem.value["id"] + endian.value + ":" + str(self.mem.value["size"]) + "=" + str(val))
            else:
                if binFormat == BinFormat.C1:
                    bArr = BitArray(strSign+self.mem.value["id"]+endian.value+":"+str(self.mem.value["size"])+"="+str(val))
                else:
                    bArr = BitArray(strSign+self.mem.value["id"]+":"+str(self.mem.value["size"] - 1)+"="+str(val))

                return self.binBaseSwitcher(bArr, BinFormat.C2, binFormat, endian, signed)
        except CreationError as e:
            raise ConvertionException(str(e))

    def getBinBitArray(self, val, endian, numBase, binFormat):
        # [0b|0x|0o]1234
        try:
            val = str(val)
            binSize = numBase.value["mod"]*len(val)
            bArr = BitArray(numBase.value["prefix"]+val)

            if endian == Endian.LITTLE:
                bArr.byteswap()

            binData = bArr.bin

            if binFormat == BinFormat.C2 or binFormat == BinFormat.C1:
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
        except CreationError as e:
            raise ConvertionException(str(e))

    def toInt(self, val):
        try:
            if self.baseIn == NumBase.DEC:
                bArr = self.getDecBitArray(val, self.endian, self.signed, self.binFormat)
            else:
                bArr = self.getBinBitArray(val, self.endian, self.baseIn, self.binFormat)

            return self.__toInt(bArr, self.endian, self.signed, self.binFormat)
        except ConvertionException as e:
            raise

    def applyFormatting(self, val):
        try:
            bArr = self.getDecBitArray(val, self.endian, self.signed, self.binFormat)  # init with IN parameters
            if self.baseOut == NumBase.DEC:
                return self.__toInt(bArr, self.endian, self.signed, self.binFormat)
            else:
                if self.baseOut == NumBase.BIN:
                    return bArr.bin
                if self.baseOut == NumBase.HEX:
                    return bArr.hex
                if self.baseOut == NumBase.OCT:
                    return bArr.oct
        except ConvertionException as e:
            raise
        except InterpretError as e:
            raise ConvertionException("Use OCT mem size to convert to octal num format")

