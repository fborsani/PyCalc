# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserFunction.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddFunctionForm(object):
    def setupUi(self, AddFunctionForm):
        AddFunctionForm.setObjectName("AddFunctionForm")
        AddFunctionForm.resize(544, 244)
        self.gridLayout = QtWidgets.QGridLayout(AddFunctionForm)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(AddFunctionForm)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.TextSymbol = QtWidgets.QLineEdit(AddFunctionForm)
        self.TextSymbol.setObjectName("TextSymbol")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.TextSymbol)
        self.label = QtWidgets.QLabel(AddFunctionForm)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.TextVars = QtWidgets.QLineEdit(AddFunctionForm)
        self.TextVars.setObjectName("TextVars")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.TextVars)
        self.label_3 = QtWidgets.QLabel(AddFunctionForm)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.TextExpr = QtWidgets.QLineEdit(AddFunctionForm)
        self.TextExpr.setObjectName("TextExpr")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.TextExpr)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.ListOperations = QtWidgets.QListWidget(AddFunctionForm)
        self.ListOperations.setObjectName("ListOperations")
        self.gridLayout.addWidget(self.ListOperations, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonDel = QtWidgets.QPushButton(AddFunctionForm)
        self.ButtonDel.setObjectName("ButtonDel")
        self.horizontalLayout.addWidget(self.ButtonDel)
        self.ButtonEdit = QtWidgets.QPushButton(AddFunctionForm)
        self.ButtonEdit.setObjectName("ButtonEdit")
        self.horizontalLayout.addWidget(self.ButtonEdit)
        self.ButtonAdd = QtWidgets.QPushButton(AddFunctionForm)
        self.ButtonAdd.setObjectName("ButtonAdd")
        self.horizontalLayout.addWidget(self.ButtonAdd)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.retranslateUi(AddFunctionForm)
        QtCore.QMetaObject.connectSlotsByName(AddFunctionForm)

    def retranslateUi(self, AddFunctionForm):
        _translate = QtCore.QCoreApplication.translate
        AddFunctionForm.setWindowTitle(_translate("AddFunctionForm", "User Functions"))
        self.label_2.setText(_translate("AddFunctionForm", "Symbol:"))
        self.label.setText(_translate("AddFunctionForm", "Variables:"))
        self.label_3.setText(_translate("AddFunctionForm", "Expression:"))
        self.ButtonDel.setText(_translate("AddFunctionForm", "Delete"))
        self.ButtonEdit.setText(_translate("AddFunctionForm", "Replace"))
        self.ButtonAdd.setText(_translate("AddFunctionForm", "Add"))
