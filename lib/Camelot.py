#-----Ludens Lee 19.3.12-----
import json
import socket
import time
import re
import os


class Camlann(object):
    def __init__(self):
        pass

    def connect(self):
        bRet = False
        strRet = ""
        try:

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(0.5)
            if self.client.connect_ex((self.zynqIP, self.zynqPort)) == 0:
                bRet = True
                self.ClientExist = True
                self.status = True
            else:
                self.status = False

        except Exception as e:
            bRet = False
            strRet = e
        return bRet

    def sendCMD(self, args):
        bRet = False
        send_bRet = False
        command = ""
        buffer = ''
        size = 1024
        if type(args) == list:
            command = args[0]
        else:
            command = args
        print "sendCMD : {} type:{} args:{}".format(command, type(args), args)
        if not self.status:
            self.connect()
        if self.status:
            try:
                self.client.settimeout(1)
                send = self.client.send("[]{}\r\n".format(command))
                if send <= 0:
                    print "Command Send Error"
                else:
                    send_bRet = True
                    print "Cmd:{} Send ok\r\n".format(command)
                time.sleep(1)
                if send_bRet:
                    if not self.status:
                        self.connect()
                    if self.status:
                        while True:
                            try:
                                self.client.settimeout(3)
                                rev = self.client.recv(size)
                                buffer += str(rev)
                                if buffer[-1] == "\n" and buffer != "":
                                    bRet = True
                                    break
                                if buffer == "":
                                    buffer = "no recv"
                                    break
                            except Exception as e:
                                buffer = e
                                bRet = False
            except Exception as e:
                bRet = False
                buffer = e
        self.LogCollection(command, buffer)
        print "Recv : {}\r\n".format(buffer)
        return bRet, buffer
