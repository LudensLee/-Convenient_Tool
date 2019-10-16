# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DebugToolUI.ui',
# licensing of 'DebugToolUI.ui' applies.
#
# Created: Wed Mar  6 14:18:43 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_cDebugToolUI(object):
    def setupUi(self, cDebugToolUI):
        cDebugToolUI.setObjectName("cDebugToolUI")
        cDebugToolUI.resize(697, 745)
        cDebugToolUI.setWindowTitle("")
        cDebugToolUI.setAutoFillBackground(True)
        cDebugToolUI.setStyleSheet("QGroupBox {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    padding: 0 3px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #FFOECE, stop: 1 #FFFFFF);\n"
"}")
        cDebugToolUI.setWindowFilePath("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(cDebugToolUI)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(cDebugToolUI)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.Tree = QtWidgets.QGroupBox(self.splitter)
        self.Tree.setTitle("")
        self.Tree.setObjectName("Tree")
        self.gridLayout = QtWidgets.QGridLayout(self.Tree)
        self.gridLayout.setObjectName("gridLayout")
        self.lb_Fixture = QtWidgets.QLabel(self.Tree)
        self.lb_Fixture.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_Fixture.setObjectName("lb_Fixture")
        self.gridLayout.addWidget(self.lb_Fixture, 0, 0, 1, 1)
        self.Fixture = QtWidgets.QComboBox(self.Tree)
        self.Fixture.setObjectName("Fixture")
        self.gridLayout.addWidget(self.Fixture, 0, 1, 1, 1)
        self.lb_Slot = QtWidgets.QLabel(self.Tree)
        self.lb_Slot.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_Slot.setObjectName("lb_Slot")
        self.gridLayout.addWidget(self.lb_Slot, 0, 2, 1, 1)
        self.Slot = QtWidgets.QComboBox(self.Tree)
        self.Slot.setObjectName("Slot")
        self.gridLayout.addWidget(self.Slot, 0, 3, 1, 1)
        self.Connect = QtWidgets.QPushButton(self.Tree)
        self.Connect.setObjectName("Connect")
        self.gridLayout.addWidget(self.Connect, 0, 4, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(self.Tree)
        self.treeWidget.setObjectName("treeWidget")
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 5)
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_6.addWidget(self.textEdit, 0, 0, 1, 6)
        self.ConnectStatus = QtWidgets.QLabel(self.groupBox)
        self.ConnectStatus.setText("")
        self.ConnectStatus.setObjectName("ConnectStatus")
        self.gridLayout_6.addWidget(self.ConnectStatus, 1, 0, 1, 2)
        self.lb_User = QtWidgets.QLabel(self.groupBox)
        self.lb_User.setObjectName("lb_User")
        self.gridLayout_6.addWidget(self.lb_User, 2, 0, 1, 1)
        self.user = QtWidgets.QLineEdit(self.groupBox)
        self.user.setObjectName("user")
        self.gridLayout_6.addWidget(self.user, 2, 1, 1, 1)
        self.lb_PW = QtWidgets.QLabel(self.groupBox)
        self.lb_PW.setObjectName("lb_PW")
        self.gridLayout_6.addWidget(self.lb_PW, 2, 2, 1, 1)
        self.password = QtWidgets.QLineEdit(self.groupBox)
        self.password.setObjectName("password")
        self.gridLayout_6.addWidget(self.password, 2, 3, 1, 1)
        self.login = QtWidgets.QPushButton(self.groupBox)
        self.login.setObjectName("login")
        self.gridLayout_6.addWidget(self.login, 2, 4, 1, 2)
        self.horizontalLayout.addWidget(self.splitter)
        self.retranslateUi(cDebugToolUI)
        QtCore.QMetaObject.connectSlotsByName(cDebugToolUI)

    def retranslateUi(self, cDebugToolUI):
        self.lb_Fixture.setText(QtWidgets.QApplication.translate("cDebugToolUI", "Fixture", None, -1))
        self.lb_Slot.setText(QtWidgets.QApplication.translate("cDebugToolUI", "Slot", None, -1))
        self.lb_PW.setText(QtWidgets.QApplication.translate("cDebugToolUI", "Password", None, -1))
        self.lb_User.setText(QtWidgets.QApplication.translate("cDebugToolUI", "User", None, -1))
        self.Connect.setText(QtWidgets.QApplication.translate("cDebugToolUI", "CONNECT", None, -1))
        self.login.setText(QtWidgets.QApplication.translate("cDebugToolUI", "LOGIN", None, -1))
        self.treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("cDebugToolUI", "Item", None, -1))
        self.treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("cDebugToolUI", "Value2", None, -1))
        self.treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("cDebugToolUI", "Value1", None, -1))
        self.treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("cDebugToolUI", "Value3", None, -1))

