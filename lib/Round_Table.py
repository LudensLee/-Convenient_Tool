import zmq

class Lancelot:

    def __init__(self,ip,Port):
        self.ip = str(ip)
        self.Port = str(Port)
        self.strRecv = ""


    def connect_b_str_obj(self,type):
        self.bRet = False
        ConnectType = None
        if "REQ" in str(type).upper():
            ConnectType = zmq.REQ
        if "SUB" in str(type).upper():
            ConnectType = zmq.SUB
        if ConnectType == None:
            self.strRecv = "Type Error"
        else:
            try:
                self.Context = zmq.Context()
                self.Socket = self.Context.socket(ConnectType)
                self.Socket.connect("tcp://{}:{}".format(self.ip,self.Port))
                self.bRet = True
                self.strRecv = "{} Connect OK".format(str(type))
            except Exception as e:
                self.strRecv = e
                self.bRet = False
        return self.bRet,self.strRecv,self.Socket


    def bind_b_str_obj(self,type):
        self.bRet = False
        ConnectType = None
        if "REP" in str(type).upper():
            ConnectType = zmq.REP
        if "PUB" in str(type).upper():
            ConnectType = zmq.PUB
        if ConnectType == None:
            self.strRecv = "Type Error"
        else:
            try:
                self.Context = zmq.Context()
                self.Socket = self.Context.socket(ConnectType)
                self.Socket.bind("tcp://{}:{}".format(self.ip,self.Port))
                self.bRet = True
                self.strRecv = "{} Connect OK".format(str(type))
            except Exception as e:
                self.strRecv = e
                self.bRet = False
        return self.bRet,self.strRecv,self.Socket





