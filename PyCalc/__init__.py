from PyCalc.gui.mainWindow import Ui_MainWindow
from PyCalc.gui.inputSettings import Ui_DialogInputSettings
from PyCalc.gui.userFunction import Ui_AddFunctionForm
from PyCalc.gui.stringManager import Ui_StringManager

from PyCalc.formatModule import *
from PyCalc.calculator import *
from PyCalc.colorPicker import *
from PyCalc.stringUtilities import *

from PyQt5.QtWidgets import *

import sys

associatedSettings = {
    "Dec": NumBase.DEC,
    "Oct": NumBase.OCT,
    "Hex": NumBase.HEX,
    "Bin": NumBase.BIN,
    "Integer": DataType.INT,
    "Float": DataType.FLOAT,
    "Double": DataType.DOUBLE,
    "Byte (8 bits)": DataType.BYTE,
    "Word (16 bits)": DataType.WORD,
    "Double Word (32 bits)": DataType.DWORD,
    "Quad Word (64 bits)": DataType.QWORD,
    "Oct Half Word (6 bits)": DataType.HWORDO,
    "Oct Word (12 bits)": DataType.WORDO,
    "Oct Double Word (24 bits)": DataType.DWORDO,
    "Oct Triple Word (36 bits)": DataType.TWORDO,
}

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.optionsDialog = InputSettings(self)
        self.userFunctions = UserFunctions(self)
        self.stringManager = StringManager(self)
        self.colorPicker = QColorEdit(parent=self)
        self.colorPicker.setWindowTitle("Picker")

        self.ui.OKButton.clicked.connect(self.calc)
        self.ui.OldOperationsList.clicked.connect(self.fetchOldOperation)
        self.ui.InputSettingsButton.clicked.connect(lambda: self.optionsDialog.show())
        self.ui.MenuAddFunction.triggered.connect(lambda: self.userFunctions.show())
        self.ui.MenuCalcString.triggered.connect(lambda: self.stringManager.show())
        self.ui.MenuColorPicker.triggered.connect(lambda: self.colorPicker.show())

    def collectArgs(self):
        dictArgs = {}

        if self.ui.EndianBig.isChecked():
            endian = Endian.BIG
        elif self.ui.EndianLittle.isChecked():
            endian = Endian.LITTLE
        else:
            endian = Endian.NATIVE

        if self.ui.FormatC1.isChecked():
            binFormat = BinFormat.C1
        elif self.ui.FormatMS.isChecked():
            binFormat = BinFormat.MS
        else:
            binFormat = BinFormat.C2

        dictArgs["base"] = associatedSettings[self.ui.BaseOutSelector.currentText()]
        dictArgs["signed"] = self.ui.CheckSigned.isChecked()
        dictArgs["mem"] = associatedSettings[self.ui.MemSizeSelector.currentText()]
        dictArgs["endian"] = endian
        dictArgs["binFormat"] = binFormat

        return dictArgs

    def createConverter(self):
        dictOut = self.collectArgs()
        dictIn = self.optionsDialog.collectArgs()

        #  fill the fields that are supposed to be the same
        dictIn["base"] = associatedSettings[self.ui.BaseInSelector.currentText()]
        if dictIn["signed"] is None: dictIn["signed"] = dictOut["signed"]
        if dictIn["endian"] is None: dictIn["endian"] = dictOut["endian"]
        if dictIn["binFormat"] is None: dictIn["binFormat"] = dictOut["binFormat"]

        argsDict = {"out": dictOut, "in": dictIn}

        return Converter(argsDict)

    def calc(self):
        expr = self.ui.TextInput.text()
        converter = self.createConverter()
        c = Calculator(converter)
        res = c.solve(expr)
        if res:
            self.ui.TextResult.setText(res)
            if not any(self.ui.OldOperationsList.item(i).text() == expr for i in range(0, self.ui.OldOperationsList.count(), 1)):
                self.ui.OldOperationsList.addItem(expr)
        else:
            self.ui.TextResult.setText(c.error)

    def fetchOldOperation(self):
        picked = self.ui.OldOperationsList.selectedItems()
        self.ui.TextInput.setText(picked[0].text())

class InputSettings(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(InputSettings, self).__init__(parent)
        self.ui = Ui_DialogInputSettings()
        self.ui.setupUi(self)

        self.ui.BinFormatFollowOutput.clicked.connect(self.manageBinFormatSettings)
        self.ui.EndiannessFollowOutput.clicked.connect(self.manageEndiannessSettings)
        self.ui.SignFollowOutput.clicked.connect(self.manageSignSettings)
        self.ui.buttonBox.accepted.connect(self.onAccepted)
        self.ui.buttonBox.rejected.connect(self.onRejected)

    def collectArgs(self):
        dictArgs = {}

        if self.ui.EndiannessFollowOutput.isChecked():
            endian = None
        elif self.ui.EndianBig.isChecked():
            endian = Endian.BIG
        elif self.ui.EndianLittle.isChecked():
            endian = Endian.LITTLE
        else:
            endian = Endian.NATIVE

        if self.ui.BinFormatFollowOutput.isChecked():
            binFormat = None
        elif self.ui.FormatC1.isChecked():
            binFormat = BinFormat.C1
        elif self.ui.FormatMS.isChecked():
            binFormat = BinFormat.MS
        else:
            binFormat = BinFormat.C2

        if self.ui.SignFollowOutput.isChecked():
            checked = None
        else:
            checked = self.ui.SignYes.isChecked()

        dictArgs["base"] = None  # to be set by the mainwindow since the comboBox is there
        dictArgs["signed"] = checked
        dictArgs["endian"] = endian
        dictArgs["binFormat"] = binFormat

        return dictArgs

    def manageBinFormatSettings(self):
        self.ui.FormatC1.setEnabled(not self.ui.BinFormatFollowOutput.isChecked())
        self.ui.FormatC2.setEnabled(not self.ui.BinFormatFollowOutput.isChecked())
        self.ui.FormatMS.setEnabled(not self.ui.BinFormatFollowOutput.isChecked())

    def manageEndiannessSettings(self):
        self.ui.EndianLittle.setEnabled(not self.ui.EndiannessFollowOutput.isChecked())
        self.ui.EndianBig.setEnabled(not self.ui.EndiannessFollowOutput.isChecked())
        self.ui.EndianNative.setEnabled(not self.ui.EndiannessFollowOutput.isChecked())

    def manageSignSettings(self):
        self.ui.SignYes.setEnabled(not self.ui.SignFollowOutput.isChecked())
        self.ui.SignNo.setEnabled(not self.ui.SignFollowOutput.isChecked())

    def onAccepted(self):
        self.close()

    def onRejected(self):
        self.ui.EndiannessFollowOutput.setChecked(True)
        self.ui.BinFormatFollowOutput.setChecked(True)
        self.ui.SignFollowOutput.setChecked(True)

        # call the functions manually to disable radio buttons
        self.manageEndiannessSettings()
        self.manageBinFormatSettings()
        self.manageSignSettings()
        self.close()

class UserFunctions(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UserFunctions, self).__init__(parent)
        self.ui = Ui_AddFunctionForm()
        self.ui.setupUi(self)

        self.opReference = operations
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
        if any(op == symbol and not operations[op]["userDef"] for op in operations.keys()):
            raise Exception("Base functions cannot be overwritten")
        if symbol in expr:
            raise Exception("Function's symbol cannot be used in its own body")
        if len(varsList) > 0:
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
            argList = []
        expr = self.ui.TextExpr.text().lower()

        try:
            self.sanitizeInput(symbol, expr, argList)

            funcDict = {"userDef": True, "pri": Priority.HIGH, "args": argList, "ltAssoc": False, "calc": expr}

            self.opReference[symbol] = funcDict
            self.updateFunctions()
        except Exception as e:
            self.reportError(str(e))

    def delFunction(self):
        function = self.ui.ListOperations.selectedItems()[0].text()
        del self.opReference[function]
        self.updateFunctions()

    def replaceFunction(self):
        symbolOld = self.ui.ListOperations.selectedItems()[0].text()

        symbol = self.ui.TextSymbol.text()
        argList = self.ui.TextVars.text().split(" ")
        expr = self.ui.TextExpr.text()

        try:
            self.sanitizeInput(symbol, expr, argList)

            funcDict = {"userDef": True, "pri": Priority.HIGH, "args": argList, "ltAssoc": False, "calc": expr}

            if symbol != symbolOld:
                del self.opReference[symbolOld]

            self.opReference[symbol] = funcDict
            self.updateFunctions()
        except Exception as e:
            self.reportError(str(e))

class StringManager(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(StringManager, self).__init__(parent)
        self.ui = Ui_StringManager()
        self.ui.setupUi(self)

        self.ui.FrameIn.hide()
        self.ui.FrameOut.hide()
        self.__initEncodingList()

        self.ui.CheckReadFromFile.clicked.connect(lambda: self.ui.FrameIn.setVisible(self.ui.CheckReadFromFile.isChecked()))
        self.ui.CheckWriteToFile.clicked.connect(lambda: self.ui.FrameOut.setVisible(self.ui.CheckWriteToFile.isChecked()))
        self.ui.FileButtonIn.clicked.connect(lambda: self.__connectAndShowDialog("in"))
        self.ui.FileButtonOut.clicked.connect(lambda: self.__connectAndShowDialog("out"))
        self.ui.ConvertButton.clicked.connect(self.convert)

        self.fileDialog = QFileDialog(self)
        self.fileDialog.setFileMode(QFileDialog.AnyFile)

        self.pathIn = None
        self.pathOut = None

    def __initEncodingList(self):
        for i in range(0, len(listOfTextEncodings), 1):
            self.ui.FormatBoxInput.addItem(textEncodingBeautifier(i))
            self.ui.FormatBoxOutput.addItem(textEncodingBeautifier(i))

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

    def writeFile(self):
        file = open(self.pathOut, "w")
        file.write(self.ui.TextOut.toPlainText())
        file.close()

    def convert(self):
        try:
            encodingIn = getEncoding(self.ui.FormatBoxInput.currentText())
            encodingOut = getEncoding(self.ui.FormatBoxOutput.currentText())

            if self.ui.CheckReadFromFile.isChecked():
                self.readFile()

            text = self.ui.TextIn.toPlainText()
            bytesIn = text.encode(encodingIn, "replace")
            textOut = bytesIn.decode(encodingOut, "replace")
            self.ui.TextOut.setText(textOut)
            if self.ui.CheckWriteToFile.isChecked():
                self.writeFile()
        except Exception as e:
            self.ui.TextOut.setText(str(e))


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
