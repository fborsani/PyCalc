import os
import sys

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QDialog, QApplication

import PyCalc.calculator as calc
import PyCalc.formatModule as fm
import PyCalc.stringUtilities as su
from PyCalc.gui.colorPicker import *
from PyCalc.gui.mainWindow import Ui_MainWindow
from PyCalc.gui.stringManager import Ui_StringManager
from PyCalc.gui.userFunction import Ui_AddFunctionForm

STYLEDIR = "./styles/"

dictMem = {
    "Integer": fm.DataType.INT,
    "Float": fm.DataType.FLOAT,
    "Double": fm.DataType.DOUBLE,
    "Byte (8 bits)": fm.DataType.BYTE,
    "Word (16 bits)": fm.DataType.WORD,
    "Double Word (32 bits)": fm.DataType.DWORD,
    "Quad Word (64 bits)": fm.DataType.QWORD,
    "Oct Half Word (6 bits)": fm.DataType.HWORDO,
    "Oct Word (12 bits)": fm.DataType.WORDO,
    "Oct Double Word (24 bits)": fm.DataType.DWORDO,
    "Oct Quad Word (48 bits)": fm.DataType.QWORDO,
}

dictBase = {
    "Dec": fm.NumBase.DEC,
    "Oct": fm.NumBase.OCT,
    "Hex": fm.NumBase.HEX,
    "Bin": fm.NumBase.BIN
}

dictStyles = {}

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.userFunctions = UserFunctions(self)
        self.stringManager = StringManager(self)
        self.colorPicker = QColorEdit(parent=self)
        self.colorPicker.setWindowTitle("Picker")
        self.colorPicker.send.pressed.connect(self.__setColor)

        self.ui.OKButton.clicked.connect(self.calc)
        self.ui.OldOperationsList.clicked.connect(self.fetchOldOperation)
        self.ui.MenuAddFunction.triggered.connect(self.userFunctions.show)
        self.ui.MenuCalcString.triggered.connect(self.stringManager.show)
        self.ui.MenuColorPicker.triggered.connect(self.colorPicker.show)

        self.__initLists()

    def __setColor(self):
        """
        keys and values of dict maintain their relative positions when turned into separated lists.
        Corrispondence between keys index and QComboBox items index is guaranteed because the ComboBox items are
        created by iterating on the dictionary keys list thus guaranteeing the items will always be in the same position
        """

        self.ui.TextInput.setText(self.colorPicker.text())
        idxm = list(dictMem.values()).index(fm.DataType.DWORDO)
        idxb = list(dictBase.values()).index(fm.NumBase.HEX)
        self.ui.MemSizeSelector.setCurrentIndex(idxm)
        self.ui.BaseInSelector.setCurrentIndex(idxb)
        self.ui.CheckSigned.setChecked(True)

    def __initLists(self):
        for i in dictMem.keys():
            self.ui.MemSizeSelector.addItem(i)

        for i in dictBase.keys():
            self.ui.BaseInSelector.addItem(i)
            self.ui.BaseOutSelector.addItem(i)

        for file in os.scandir(STYLEDIR):
            if file.is_file() and file.name.endswith(".css"):
                text = file.name[:file.name.rfind(".css")]
                dictStyles[text] = file
                action = self.ui.menuThemes.addAction(text)
                action.triggered.connect(lambda: self.__applyStyle(action.text()))

    def __applyStyle(self, name):
        with open(dictStyles[name], "r") as f:
            self.setStyleSheet(f.read())
            f.close()

    def __createConverter(self):
        if self.ui.EndianBig.isChecked():
            endian = fm.Endian.BIG
        elif self.ui.EndianLittle.isChecked():
            endian = fm.Endian.LITTLE
        else:
            endian = fm.Endian.NATIVE

        if self.ui.FormatC1.isChecked():
            binFormat = fm.BinFormat.C1
        elif self.ui.FormatMS.isChecked():
            binFormat = fm.BinFormat.MS
        else:
            binFormat = fm.BinFormat.C2

        baseIn = dictBase[self.ui.BaseInSelector.currentText()]
        baseOut = dictBase[self.ui.BaseOutSelector.currentText()]
        memSize = dictMem[self.ui.MemSizeSelector.currentText()]
        signed = self.ui.CheckSigned.isChecked()

        return fm.Converter(baseIn, baseOut, binFormat, memSize, endian, signed)

    def calc(self):
        expr = self.ui.TextInput.text()
        converter = self.__createConverter()
        c = calc.Calculator(converter)
        try:
            res = c.solve(expr)
            self.ui.TextResult.setText(res)
            if not any(self.ui.OldOperationsList.item(i).text() == expr for i in range(0, self.ui.OldOperationsList.count(), 1)):
                self.ui.OldOperationsList.addItem(expr)
        except calc.ConvertionException as e:
            self.ui.TextResult.setText("Conversion error: "+e.msg)
        except calc.ParseException as e:
            self.ui.TextResult.setText("Parse error: "+e.msg)
        except ArithmeticError as e:
            self.ui.TextResult.setText("Math error: "+str(e))
        except RecursionError:
            self.ui.TextResult.setText("Recursion depth excedeed, check custom functions for loops")

    def fetchOldOperation(self):
        picked = self.ui.OldOperationsList.selectedItems()
        self.ui.TextInput.setText(picked[0].text())

class UserFunctions(QDialog):
    def __init__(self, parent=None):
        super(UserFunctions, self).__init__(parent)
        self.ui = Ui_AddFunctionForm()
        self.ui.setupUi(self)

        self.opReference = calc.operations
        self.ui.ButtonAdd.clicked.connect(self.addFunction)
        self.ui.ButtonDel.clicked.connect(self.delFunction)
        self.ui.ButtonEdit.clicked.connect(self.replaceFunction)
        self.ui.ListOperations.clicked.connect(self.insertData)

    @staticmethod
    def sanitizeInput(symbol, expr, varsList):
        if not symbol or symbol == "":
            raise Exception("Missing function symbol")
        if not expr or expr == "":
            raise Exception("Missing function body")
        if any(op == symbol and not calc.operations[op]["userDef"] for op in calc.operations.keys()):
            raise Exception("Base functions cannot be overwritten")
        if symbol in expr:
            raise Exception("Function's symbol cannot be used in its own body")
        if varsList and varsList != "":
            if any(not var.isalnum() or var.isdigit() for var in varsList):
                raise Exception("Function arguments must be alphanumeric and contain at least one letter")
            if symbol in varsList:
                raise Exception("Function's symbol cannot be used as an argument")

    @staticmethod
    def reportError(err):
        print(str(err))  # for logging purposes

        errorDialog = QtWidgets.QMessageBox()
        errorDialog.setIcon(QtWidgets.QMessageBox.Critical)
        errorDialog.setText(str(err))
        errorDialog.setWindowTitle("Error")
        errorDialog.exec_()

    def updateFunctions(self):
        self.ui.ListOperations.clear()

        for key in self.opReference:
            if self.opReference[key]["userDef"]:
                self.ui.ListOperations.addItem(str(key))

    def insertData(self):
        symbol = self.ui.ListOperations.selectedItems()[0].text()
        funcArgsStr = ""
        funcArgsList = self.opReference[symbol]["args"]

        if funcArgsList:
            for i in range(0, len(funcArgsList), 1):
                if i + 1 < len(funcArgsList):
                    funcArgsStr += funcArgsList[i] + " "
                else:
                    funcArgsStr += funcArgsList[i]

        self.ui.TextSymbol.setText(symbol)
        self.ui.TextVars.setText(funcArgsStr)
        self.ui.TextExpr.setText(self.opReference[symbol]["calc"])

    def addFunction(self):
        symbol = self.ui.TextSymbol.text().lower()
        if self.ui.TextVars.text() != "":
            argList = self.ui.TextVars.text().lower().strip().split(" ")
        else:
            argList = None
        expr = self.ui.TextExpr.text().lower()

        try:
            self.sanitizeInput(symbol, expr, argList)

            funcDict = {"userDef": True, "pri": calc.Priority.HIGH, "args": argList, "ltAssoc": False, "calc": expr}

            self.opReference[symbol] = funcDict
            self.updateFunctions()
        except Exception as e:
            self.reportError(str(e))

    def delFunction(self):
        function = self.ui.ListOperations.selectedItems()[0].text()
        del self.opReference[function]
        self.updateFunctions()

    def replaceFunction(self):
        try:
            if self.ui.ListOperations.selectedItems()[0] is None:
                raise Exception("No item selected")

            symbolOld = self.ui.ListOperations.selectedItems()[0].text()

            symbol = self.ui.TextSymbol.text()
            argList = self.ui.TextVars.text().split(" ")
            expr = self.ui.TextExpr.text()
            self.sanitizeInput(symbol, expr, argList)

            funcDict = {"userDef": True, "pri": calc.Priority.HIGH, "args": argList, "ltAssoc": False, "calc": expr}

            if symbol != symbolOld:
                del self.opReference[symbolOld]

            self.opReference[symbol] = funcDict
            self.updateFunctions()
        except Exception as e:
            self.reportError(str(e))

class StringManager(QDialog):
    def __init__(self, parent=None):
        super(StringManager, self).__init__(parent)
        self.ui = Ui_StringManager()
        self.ui.setupUi(self)

        self.ui.FrameIn.hide()
        self.ui.FrameOut.hide()
        self.__initLists()

        self.ui.CheckReadFromFile.clicked.connect(lambda: self.ui.FrameIn.setVisible(self.ui.CheckReadFromFile.isChecked()))
        self.ui.CheckWriteToFile.clicked.connect(lambda: self.ui.FrameOut.setVisible(self.ui.CheckWriteToFile.isChecked()))
        self.ui.FileButtonIn.clicked.connect(lambda: self.__connectAndShowDialog("in"))
        self.ui.FileButtonOut.clicked.connect(lambda: self.__connectAndShowDialog("out"))
        self.ui.ConvertButton.clicked.connect(self.convert)

        self.fileDialog = QFileDialog(self)
        self.fileDialog.setFileMode(QFileDialog.AnyFile)

        self.pathIn = None
        self.pathOut = None

    def __initLists(self):
        for i in range(0, len(su.listOfTextEncodings), 1):
            self.ui.FormatBoxInput.addItem(su.textEncodingBeautifier(i))
            self.ui.FormatBoxOutput.addItem(su.textEncodingBeautifier(i))

        for key in su.bitOperations.keys():
            self.ui.DecodeBox.addItem(key)
            self.ui.EncodeBox.addItem(key)

    def __connectAndShowDialog(self, field):
        self.fileDialog.accepted.connect(lambda: self.__getSelectedFile(field))
        self.fileDialog.show()

    def __getSelectedFile(self, field):
        if field == "in":
            self.pathIn = str(self.fileDialog.selectedFiles()[0])
            self.ui.AddrLineIn.setText(self.pathIn)
        elif field == "out":
            self.pathOut = str(self.fileDialog.selectedFiles()[0])
            self.ui.AddrLineOut.setText(self.pathOut)
        self.fileDialog.disconnect()

    def readFile(self):
        file = open(self.pathIn, "r")
        text = file.read()
        self.ui.TextIn.setText(text)
        file.close()

    def writeFile(self, append=bool):
        if append:
            file = open(self.pathOut, "a")
        else:
            file = open(self.pathOut, "w")
        file.write(self.ui.TextOut.toPlainText())
        file.close()

    def convert(self):
        try:
            encodingIn = su.getEncoding(self.ui.FormatBoxInput.currentText())
            encodingOut = su.getEncoding(self.ui.FormatBoxOutput.currentText())

            if self.ui.CheckReadFromFile.isChecked():
                self.readFile()

            text = self.ui.TextIn.toPlainText()
            textOut = su.convert(text, encodingIn, encodingOut)
            self.ui.TextOut.setText(textOut)
            if self.ui.CheckWriteToFile.isChecked():
                self.writeFile(self.ui.OptAppend.isChecked())
        except Exception as e:
            self.ui.TextOut.setText(str(e))

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
