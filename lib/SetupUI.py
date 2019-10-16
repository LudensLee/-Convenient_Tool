#-----Ludens Lee 19.3.12-----
from DebugToolUI import Ui_cDebugToolUI
from PySide2 import QtWidgets,QtGui,QtCore
import json
import zmq
import time
import os
import sys
import signal
import functools
from lib.Round_Table import Lancelot
from PySide2.QtCore import QThread

class RepClient(QThread):
    _SendSingl = QtCore.Signal(str)
    def __init__(self,Main = None):
        super(RepClient, self).__init__()
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        print "the path :{}".format(dirname)
        with open("./Config/ui_config.json", "r") as f:
            self.ui_config = json.load(f)

        self.objMain = Main
        self.RepPort = str(self.ui_config.get('Config').get("Port").get("REP"))
        self.objLancelot = Lancelot("127.0.0.1", self.RepPort)
        self.bRet, self.strRecv, self.ReqSocket = self.objLancelot.connect_b_str_obj("REQ")


    def run(self):
        if self.bRet == True:

            self.strDictValue = self.objMain.ReturnValue()
            print self.strDictValue
            self.ReqSocket.send(str(self.strDictValue))
            print("REQSend: {}".format(str(self.strDictValue)))
            self.dictValue = {"CMD": "", "Param": ""}
            response = self.ReqSocket.recv()
            print("REQresponse: {}".format(response))
            self._SendSingl.emit(response)
            time.sleep(1)
            self.objMain.SendFlag = 0

        else:
            print "connect error:{}".format(self.strRecv)



class SubClient(QThread):
    _SendSingl = QtCore.Signal(str)
    _ConnectSingl = QtCore.Signal(str)
    def __init__(self,Main = None):
        super(SubClient, self).__init__()
        with open("./Config/ui_config.json", "r") as f:
            self.ui_config = json.load(f)
        self.objMain = Main
        self.string = ""
        self.SubPort = str(self.ui_config.get('Config').get("Port").get("SUB"))
        self.objLancelot = Lancelot("127.0.0.1", self.SubPort)
        self.bRet, self.strRecv, self.SubSocket = self.objLancelot.connect_b_str_obj("SUB")
        self.SubSocket.setsockopt(zmq.SUBSCRIBE, "")


    def run(self):

        if self.bRet == True:
            while True:
                self.string = self.SubSocket.recv()
                print("SUBresponse: {}".format(self.string))
                self._SendSingl.emit(self.string)
                self._ConnectSingl.emit(self.string)
        else:
            print "connect error:{}".format(self.strRecv)






class cTools(QtWidgets.QWidget,Ui_cDebugToolUI):
    def __init__(self,ProcessPid,parent=None):
        super(cTools, self).__init__(parent)
        self.setupUi(self)
        self.ProcessPid = ProcessPid
        print "PID:{}".format(self.ProcessPid)
        self.slot = 2
        self.text = ""
        self.SendFlag = 0
        self.dictValue = {"CMD":"","Param":""}
        self.strCmd = ""
        self.listParams = []
        self.dictLog = {"CMD":"","Param":""}
        self.Controls = []
        self.test = []
        self.id = 0
        self.nFixtureNum = 0
        self.nSlotNum = 0
        self.nVaule = 0
        self.Tree.setEnabled(False)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signalMapper = QtCore.QSignalMapper(self)


        self.RepClient = RepClient(self)
        self.RepClient._SendSingl.connect(self.TraceLog)


        self.SubClient = SubClient(self)
        self.SubClient._SendSingl.connect(self.changeLog)
        self.SubClient._ConnectSingl.connect(self.IpStatus)
       # self.SubClient.
        self.SubClient.start()

        self.ButtonClick()

        self.ConnectStatus.setText("No Connect")
        with open("./Config/ui_config.json", "r") as f:
            self.ui_config = json.load(f)


        print self.ui_config.keys()
        print self.ui_config.get('ItemTable').keys()
        self.strRecv = ""
        self.complete = None
        self.setWindowTitle("Convenient Tool V1.1")


        self.treeWidget.setColumnCount(4)
        self.treeWidget.setAutoFillBackground(1)
        self.treeWidget.setAlternatingRowColors(True)

        self.treeWidget.header().setDefaultAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.InitColumnName()
        self.InitDeviceItem()

        objGroup = self.AddGroup()
        self.InitGroupName()
        self.SetColumnWidth()


        self.createContextMenu()




    def PassWordCheck(self):
        strUser = self.user.text()
        strPassWord = self.password.text()
        if strUser == "admin" and strPassWord == "admin":
            self.Tree.setEnabled(True)
            self.Tree.repaint()
            self.user.setEnabled(False)
            self.user.repaint()
            self.login.setEnabled(False)
            self.user.repaint()
            self.password.setEnabled(False)
            self.user.repaint()
        else:
            reminder = QtWidgets.QMessageBox.warning(self, "",
                                                     "Password Wrong!!",
                                                     )

    def ButtonClick(self):

        self.Connect.clicked.connect(self.connect)
        self.login.clicked.connect(self.PassWordCheck)

        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.close)



    def IpStatus(self,strLog):
        if ":8000" in strLog:

            strZynqIp = "127.0.0.1"
            print "Ip:{}".format(strZynqIp)
            if "Connect OK" in strLog:
                self.ConnectStatus.setText("{} Connect OK".format(strZynqIp))

            if "Connect Error" in strLog:
                self.ConnectStatus.setText("{} Connect Error".format(strZynqIp))

            if "Exception" in strLog:
                self.ConnectStatus.setText("{} Connect Exception".format(strZynqIp))

    def SetColumnName(self,nCol,strName):
        self.treeWidget.headerItem().setText(nCol, QtWidgets.QApplication.translate("cDebugToolUI", strName, None, -1))

    def SetColumnWidth(self):
        self.treeWidget.setColumnWidth(0,200)
        self.treeWidget.setColumnWidth(1,300)
        self.treeWidget.setColumnWidth(2,300)
        self.treeWidget.setColumnWidth(3,300)


    def InitColumnName(self):
        for i in range(1,5):
            strColumnName = self.ui_config.get('Config').get("ColumnName").get("Column{}".format(i))
            self.SetColumnName(i-1,strColumnName)


    def InitGroupName(self):
        listGroupName = []
        listGroupName = self.ui_config.get('ItemTable').keys()
        for i in range(0,len(listGroupName)):
            self.treeWidget.topLevelItem(i).setText(0,QtWidgets.QApplication.translate("cDebugToolUI", listGroupName[i], None, -1))



    def AddGroup(self):
        listGroupName = []
        listItemName = []
        listGroupName = self.ui_config.get('ItemTable').keys()
        for i in range(0, len(listGroupName)):
            objGroup = QtWidgets.QTreeWidgetItem(self.treeWidget, ["", "", "", ""])
            listItemName = self.ui_config.get('ItemTable').get(listGroupName[i])
            print listItemName
            for j in range(0,len(listItemName)):

                self.AddLine(objGroup,
                             listItemName.keys()[j],
                             self.ui_config.get('ItemTable').get(listGroupName[i]).get(listItemName.keys()[j]).get("FunctionName"),
                             self.ui_config.get('ItemTable').get(listGroupName[i]).get(listItemName.keys()[j]).get("Type"),
                             self.ui_config.get('ItemTable').get(listGroupName[i]).get(listItemName.keys()[j]).get("IoTableList"),
                             )

    def AddLine(self,objGroup,strItemName,strCmd,strType,strIoTableList):
        listParam = []
        Item = QtWidgets.QTreeWidgetItem(objGroup, ["", "", "", ""])


        if str(strType).upper() == "LINE":

            SendButton = self.SetSize(QtWidgets.QPushButton(self.treeWidget))
            Param1 = self.SetSize(QtWidgets.QTextEdit(self.treeWidget))
            Param2 = self.SetSize(QtWidgets.QTextEdit(self.treeWidget))
            Param3 = self.SetSize(QtWidgets.QTextEdit(self.treeWidget))

            SendButton.setText(strItemName)
            listControls = []
            listControls.append(Param1)
            listControls.append(Param2)
            listControls.append(Param3)

            SendButton.clicked.connect(lambda: self.SendCmd(strCmd, listControls))

        if str(strType).upper() == "COMBOBOX":
            SendButton = self.SetSize(QtWidgets.QPushButton(self.treeWidget))
            Param1 = self.SetSize(QtWidgets.QComboBox(self.treeWidget))
            Param2 = self.SetSize(QtWidgets.QComboBox(self.treeWidget))
            Param3 = self.SetSize(QtWidgets.QTextEdit(self.treeWidget))
            SendButton.setText(strItemName)
            listControls = []
            listControls.append(Param1)
            listControls.append(Param2)
            listControls.append(Param3)
            dictTable = self.io_table.get(strIoTableList)
            listTable = dictTable.keys()

            print "listTable:{}".format(listTable)
            Param1.clear()
            for strTable in listTable:
                if strTable.upper() != "DISCONNECT":
                    print (strTable)
                    Param1.addItem(str(strTable))
            Param1.setEditable(True)
            Param1.setCurrentIndex(-1)
            Complete = QtWidgets.QCompleter(listTable)
            Param1.setCompleter(Complete)
            Param1.activated.connect(lambda x:self.DisplayRelayConnectTo(listControls))



            SendButton.clicked.connect(lambda: self.SendComboBoxCmd(strCmd, listControls))
        self.treeWidget.setItemWidget(Item, 0, SendButton)
        self.treeWidget.setItemWidget(Item, 1, Param1)
        self.treeWidget.setItemWidget(Item, 2, Param2)
        self.treeWidget.setItemWidget(Item, 3, Param3)


    def SendComboBoxCmd(self,strCmd,listParam):
        self.strCmd = strCmd
        print "cmd:{}".format(strCmd)
        self.listParams = []
        for i in range(0,2):
            Index = listParam[i].currentIndex()
            Name = listParam[i].itemText(Index)
            self.listParams.append(Name)
        strName = listParam[2].toPlainText()
        self.listParams.append(strName)
        print "list:{}".format(self.listParams)
        self.dictValue = {}
        self.dictValue["CMD"] = self.strCmd
        self.dictValue["Param"] = self.listParams
        self.SendFlag = 1
        self.RepClient.start()
        print "cmd:{} param:{} dictValue:{}".format(self.strCmd, self.listParams, self.dictValue)

    def SetSize(self,objControl,nHeight=30,nWidth=100):
        objControl.setFixedHeight(nHeight)
        return objControl


    def InitDeviceItem(self):
        self.nFixtureNum = self.ui_config.get('Config').get("Device").get("FixtureNum")
        self.nSlotNum = self.ui_config.get('Config').get("Device").get("SlotNum")
        for i in range(0,self.nFixtureNum):
            self.Fixture.addItem(str(i+1))
        for i in range(0,self.nSlotNum):
            self.Slot.addItem(str(i+1))

    def SendCmd(self,strCmd,listParam):
        self.strCmd = strCmd
        print "cmd:{}".format(strCmd)
        self.listParams = map(lambda x:x.toPlainText(),listParam)
        print "list:{}".format(self.listParams)
        self.dictValue = {}
        self.dictValue["CMD"] = self.strCmd
        self.dictValue["Param"] = self.listParams
        self.SendFlag = 1
        self.RepClient.start()
        print "cmd:{} param:{} dictValue:{}".format(self.strCmd, self.listParams, self.dictValue)


    def DisplayRelayConnectTo(self,ListParam):
        print "DisplayRelayConnectTo Start"
        param1 = ListParam[0]
        param2 = ListParam[1]
        RelayIndex = param1.currentIndex()
        RelayName = param1.itemText(RelayIndex)
        print "RelayName:{}".format(RelayName)
        param2.clear()
        dictRelayConnectTo = self.io_table.get("RelayTable").get(RelayName)
        print "dictRelayConnectTo:{}".format(dictRelayConnectTo)
        if dictRelayConnectTo !=None:
            listRelayConnectTo = dictRelayConnectTo.keys()

            for strRelayConnectTo in listRelayConnectTo:
                param2.addItem(strRelayConnectTo)

        print dictRelayConnectTo




    def ReturnValue(self):
        print "ReturnCmd:{}".format(self.strCmd)
        if self.strCmd !="":
            self.strCmd = ""
            self.listParams = ""
        else:
            self.dictValue = {"CMD": "", "Param": ""}
        print "ReturnValue:{}".format(self.dictValue)
        return self.dictValue


    def changeLog(self,strLog):
        if "Mordred" in strLog:
            strLog = strLog.replace("Mordred","")
            self.textEdit.append(strLog)
            strRet = "<call {} end>\r\n" \
                     "---------------------------------------------------------------\r\n".format(self.dictLog["CMD"])
            self.textEdit.append(strRet)
            self.cursor()
        else:
            self.textEdit.append(strLog)
            self.cursor()



    def TraceLog(self,strLog):
        if strLog != "no cmd!":
            self.dictLog = eval(strLog)
            strRet = "<call {}>({},{},{})\r\n".format(self.dictLog["CMD"], self.dictLog["Param"][0],self.dictLog["Param"][1],self.dictLog["Param"][2])
            self.textEdit.append(strRet)
            self.cursor()


    def cursor(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.textEdit.setTextCursor(cursor)


    def connect(self):
        FixtureIndex = self.Fixture.currentIndex()
        FixtureName = self.Fixture.itemText(FixtureIndex)
        SlotIndex = self.Slot.currentIndex()
        SlotName = self.Slot.itemText(SlotIndex)
        self.nVaule = (int(FixtureName)-1) * self.nSlotNum + int(SlotName)
        print "nVaule {}".format(self.nVaule)
        self.strCmd = "ChangeIp"
        self.dictValue = {}
        self.dictValue["CMD"] = "ChangeIp"
        self.dictValue["Param"] = [str(self.nVaule),"",""]
        self.SendFlag = 1
        self.RepClient.start()
        print self.dictValue,self.dictValue["Param"][0]

    def createContextMenu(self):
        self.textEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.textEdit.customContextMenuRequested[QtCore.QPoint].connect(self.showContextMenu)
        self.contextMenu = QtWidgets.QMenu(self)
        self.ClearLog = self.contextMenu.addAction("clear")
        self.ClearLog.triggered.connect(self.actionHandler)

    def showContextMenu(self, pos):
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()

    def actionHandler(self):
        self.textEdit.clear()

    def closeEvent(self, event):

        reply = QtWidgets.QMessageBox.question(self,
                                               '',
                                               "Exit?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            os.system("kill -9 {}".format(self.ProcessPid))
            os._exit(0)

        else:
            event.ignore()







