# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(323, 485)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.OldOperationsList = QtWidgets.QListWidget(self.centralwidget)
        self.OldOperationsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.OldOperationsList.setUniformItemSizes(True)
        self.OldOperationsList.setObjectName("OldOperationsList")
        self.verticalLayout.addWidget(self.OldOperationsList)
        self.TextResult = QtWidgets.QLineEdit(self.centralwidget)
        self.TextResult.setReadOnly(True)
        self.TextResult.setClearButtonEnabled(False)
        self.TextResult.setObjectName("TextResult")
        self.verticalLayout.addWidget(self.TextResult)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BaseOutSelector = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BaseOutSelector.sizePolicy().hasHeightForWidth())
        self.BaseOutSelector.setSizePolicy(sizePolicy)
        self.BaseOutSelector.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BaseOutSelector.setObjectName("BaseOutSelector")
        self.BaseOutSelector.addItem("")
        self.BaseOutSelector.addItem("")
        self.BaseOutSelector.addItem("")
        self.BaseOutSelector.addItem("")
        self.horizontalLayout.addWidget(self.BaseOutSelector)
        self.MemSizeSelector = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MemSizeSelector.sizePolicy().hasHeightForWidth())
        self.MemSizeSelector.setSizePolicy(sizePolicy)
        self.MemSizeSelector.setObjectName("MemSizeSelector")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.MemSizeSelector.addItem("")
        self.horizontalLayout.addWidget(self.MemSizeSelector)
        self.CheckSigned = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckSigned.setCheckable(True)
        self.CheckSigned.setChecked(True)
        self.CheckSigned.setTristate(False)
        self.CheckSigned.setObjectName("CheckSigned")
        self.horizontalLayout.addWidget(self.CheckSigned)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_4.addWidget(self.line_2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.EndianLittle = QtWidgets.QRadioButton(self.centralwidget)
        self.EndianLittle.setObjectName("EndianLittle")
        self.GroupEndianness = QtWidgets.QButtonGroup(MainWindow)
        self.GroupEndianness.setObjectName("GroupEndianness")
        self.GroupEndianness.addButton(self.EndianLittle)
        self.horizontalLayout_2.addWidget(self.EndianLittle)
        self.EndianBig = QtWidgets.QRadioButton(self.centralwidget)
        self.EndianBig.setObjectName("EndianBig")
        self.GroupEndianness.addButton(self.EndianBig)
        self.horizontalLayout_2.addWidget(self.EndianBig)
        self.EndianNative = QtWidgets.QRadioButton(self.centralwidget)
        self.EndianNative.setChecked(True)
        self.EndianNative.setObjectName("EndianNative")
        self.GroupEndianness.addButton(self.EndianNative)
        self.horizontalLayout_2.addWidget(self.EndianNative)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_5.addWidget(self.line_3)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_5.addWidget(self.line_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.FormatMS = QtWidgets.QRadioButton(self.centralwidget)
        self.FormatMS.setObjectName("FormatMS")
        self.GroupBinFormat = QtWidgets.QButtonGroup(MainWindow)
        self.GroupBinFormat.setObjectName("GroupBinFormat")
        self.GroupBinFormat.addButton(self.FormatMS)
        self.horizontalLayout_6.addWidget(self.FormatMS)
        self.FormatC1 = QtWidgets.QRadioButton(self.centralwidget)
        self.FormatC1.setObjectName("FormatC1")
        self.GroupBinFormat.addButton(self.FormatC1)
        self.horizontalLayout_6.addWidget(self.FormatC1)
        self.FormatC2 = QtWidgets.QRadioButton(self.centralwidget)
        self.FormatC2.setChecked(True)
        self.FormatC2.setObjectName("FormatC2")
        self.GroupBinFormat.addButton(self.FormatC2)
        self.horizontalLayout_6.addWidget(self.FormatC2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.InputSettingsButton = QtWidgets.QToolButton(self.centralwidget)
        self.InputSettingsButton.setObjectName("InputSettingsButton")
        self.horizontalLayout_3.addWidget(self.InputSettingsButton)
        self.BaseInSelector = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BaseInSelector.sizePolicy().hasHeightForWidth())
        self.BaseInSelector.setSizePolicy(sizePolicy)
        self.BaseInSelector.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BaseInSelector.setObjectName("BaseInSelector")
        self.BaseInSelector.addItem("")
        self.BaseInSelector.addItem("")
        self.BaseInSelector.addItem("")
        self.BaseInSelector.addItem("")
        self.horizontalLayout_3.addWidget(self.BaseInSelector)
        self.TextInput = QtWidgets.QLineEdit(self.centralwidget)
        self.TextInput.setObjectName("TextInput")
        self.horizontalLayout_3.addWidget(self.TextInput)
        self.OKButton = QtWidgets.QPushButton(self.centralwidget)
        self.OKButton.setObjectName("OKButton")
        self.horizontalLayout_3.addWidget(self.OKButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 323, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.MenuAddFunction = QtWidgets.QAction(MainWindow)
        self.MenuAddFunction.setObjectName("MenuAddFunction")
        self.MenuCalcOffset = QtWidgets.QAction(MainWindow)
        self.MenuCalcOffset.setObjectName("MenuCalcOffset")
        self.MenuCalcString = QtWidgets.QAction(MainWindow)
        self.MenuCalcString.setObjectName("MenuCalcString")
        self.SetClassic = QtWidgets.QAction(MainWindow)
        self.SetClassic.setObjectName("SetClassic")
        self.SetDark = QtWidgets.QAction(MainWindow)
        self.SetDark.setObjectName("SetDark")
        self.MenuColorPicker = QtWidgets.QAction(MainWindow)
        self.MenuColorPicker.setObjectName("MenuColorPicker")
        self.menuFile.addAction(self.MenuAddFunction)
        self.menuFile.addAction(self.MenuCalcOffset)
        self.menuFile.addAction(self.MenuCalcString)
        self.menuFile.addAction(self.MenuColorPicker)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyCalc"))
        self.BaseOutSelector.setItemText(0, _translate("MainWindow", "Dec"))
        self.BaseOutSelector.setItemText(1, _translate("MainWindow", "Oct"))
        self.BaseOutSelector.setItemText(2, _translate("MainWindow", "Hex"))
        self.BaseOutSelector.setItemText(3, _translate("MainWindow", "Bin"))
        self.MemSizeSelector.setItemText(0, _translate("MainWindow", "Integer"))
        self.MemSizeSelector.setItemText(1, _translate("MainWindow", "Float"))
        self.MemSizeSelector.setItemText(2, _translate("MainWindow", "Double"))
        self.MemSizeSelector.setItemText(3, _translate("MainWindow", "Byte (8 bits)"))
        self.MemSizeSelector.setItemText(4, _translate("MainWindow", "Word (16 bits)"))
        self.MemSizeSelector.setItemText(5, _translate("MainWindow", "Double Word (32 bits)"))
        self.MemSizeSelector.setItemText(6, _translate("MainWindow", "Quad Word (64 bits)"))
        self.MemSizeSelector.setItemText(7, _translate("MainWindow", "Oct Half Word (6 bits)"))
        self.MemSizeSelector.setItemText(8, _translate("MainWindow", "Oct Word (12 bits)"))
        self.MemSizeSelector.setItemText(9, _translate("MainWindow", "Oct Double Word (24 bits)"))
        self.MemSizeSelector.setItemText(10, _translate("MainWindow", "Oct Triple Word (36 bits)"))
        self.CheckSigned.setText(_translate("MainWindow", "Signed"))
        self.label.setText(_translate("MainWindow", "Endianness"))
        self.EndianLittle.setText(_translate("MainWindow", "Little"))
        self.EndianBig.setText(_translate("MainWindow", "Big"))
        self.EndianNative.setText(_translate("MainWindow", "Native"))
        self.label_2.setText(_translate("MainWindow", "Binary Format"))
        self.FormatMS.setText(_translate("MainWindow", "MS"))
        self.FormatC1.setText(_translate("MainWindow", "C1"))
        self.FormatC2.setText(_translate("MainWindow", "C2"))
        self.InputSettingsButton.setText(_translate("MainWindow", "..."))
        self.BaseInSelector.setItemText(0, _translate("MainWindow", "Dec"))
        self.BaseInSelector.setItemText(1, _translate("MainWindow", "Oct"))
        self.BaseInSelector.setItemText(2, _translate("MainWindow", "Hex"))
        self.BaseInSelector.setItemText(3, _translate("MainWindow", "Bin"))
        self.OKButton.setText(_translate("MainWindow", "OK"))
        self.menuFile.setTitle(_translate("MainWindow", "Tools"))
        self.MenuAddFunction.setText(_translate("MainWindow", "Add custom function..."))
        self.MenuCalcOffset.setText(_translate("MainWindow", "Offset calculator..."))
        self.MenuCalcString.setText(_translate("MainWindow", "String encoding..."))
        self.SetClassic.setText(_translate("MainWindow", "Light"))
        self.SetDark.setText(_translate("MainWindow", "Dark"))
        self.MenuColorPicker.setText(_translate("MainWindow", "Color picker..."))
