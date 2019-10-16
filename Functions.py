import json
import socket
import time
import re
import os
from lib.Camelot import Camlann
from lib.Avalon import Merlin,Aurther




#-----Ludens Lee 19.3.12-----
import zmq
import time
import json
from lib.Round_Table import Lancelot
from threading import Thread

class RepServer(Thread):
   def __init__(self,Main = None):
       super(RepServer, self).__init__()
       with open("./Config/ui_config.json", "r") as f:
           self.ui_config = json.load(f)

       self.RepPort = str(self.ui_config.get('Config').get("Port").get("REP"))
       self.objLancelot = Lancelot("127.0.0.1",self.RepPort)
       self.bRet,self.strRecv,self.RepSocket = self.objLancelot.bind_b_str_obj("REP")

       self.objTest = Main

   def __del__(self):
       self.RepSocket.close()



   def run(self):
       if self.bRet == True:
            while True:
                self.message = self.RepSocket.recv()
                print("Received: %s" % self.message)
                self.Dict = eval(self.message)
                print self.Dict

                if self.Dict["CMD"]!="":
                    print "Received Cmd: {}".format(self.Dict["CMD"])
                    print "Received Dict: {}".format(self.Dict)
                    self.RepSocket.send(self.message)
                    self.objTest.callFunc(self.Dict["CMD"], self.Dict["Param"])

                else:
                    self.RepSocket.send("no cmd!")

       else:
           print "connect error:{}".format(self.strRecv)
       time.sleep(1)

class PubServer(Thread):
   def __init__(self,Main = None):

       super(PubServer, self).__init__()
       with open("./Config/ui_config.json", "r") as f:
           self.ui_config = json.load(f)
       self.objTest = Main
       self.Vaule = ""
       self._lastPub = ""
       self.PubPort = str(self.ui_config.get('Config').get("Port").get("SUB"))
       self.objLancelot = Lancelot("127.0.0.1",self.PubPort)
       self.bRet,self.strRecv,self.PubSocket = self.objLancelot.bind_b_str_obj("PUB")





   def __del__(self):
       self.PubSocket.close()

   def run(self):
       if self.bRet == True:
            while True:
                  if self.objTest.PubFlag == 1 :
                     self.Vaule = self.objTest.ReturnValue()
                     if self.Vaule != "":
                            time1 = time.time()
                            self.PubSocket.send(self.Vaule)
                            time2 = time.time()
                            print "pub value:{} use time:{}".format(self.Vaule,time2 - time1)
                            self._lastPub = self.Vaule

                            time.sleep(1)
                            self.objTest.PubFlag = 0
       else:
            print "connect error:{}".format(self.strRecv)

       time.sleep(1)


class Functions(Aurther,Camlann):
	def __init__(self):
		super(Functions,self).__init__()
		self.Vaule = ""
		self.status = False
		self.ClientExist = False
		self.strTraceOn = ""
		self.strRecv = ""
		self.PubFlag = 0
		self.FinishFlag = 0
		self.CmdList = []
		self.BeforeBitStatusCmd = ""
		self.RepServer = RepServer(self)
		RepThred = Thread(target=self.RepServer.run, args=())
		RepThred.start()
		self.PubServer = PubServer(self)
		RubThred = Thread(target=self.PubServer.run, args=())
		RubThred.start()


	def __del__(self):
		self.client.close()

	@Merlin("Example")
	def Example(self,args):

		self.FinishFlag = 1
		self.LogCollection("Func Name","Func Name Done")






if __name__ == '__main__':
    objTest = Functions()