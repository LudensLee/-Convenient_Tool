#-----Ludens Lee 19.3.12-----
import inspect
import time

def Merlin(name=None):
    def _(f):
        f._call_name = name or f.__name__
        return f

    return _



class Aurther(object):
    def __init__(self):
        self.__mapFunctions = {}
        self.__RegFunctions()

    def __RegFunctions(self):
        for name, f in inspect.getmembers(
                self, lambda f: callable(f) and hasattr(f, '_call_name')
        ):
            print "reg name:{},Functions:{}".format(name,f)
            self.__mapFunctions[name]=f

    def FindFunc(self,strFuncName,args):
        Vaule = ""
        bRet = False
        if strFuncName not in self.__mapFunctions:
            bRet = False
            Vaule = "Function {} can not found.".format(strFuncName)
            print Vaule
        else:
            bRet = True
            Vaule = "Function {} has been found, now execute.".format(strFuncName)
        return bRet, Vaule


    def HangderFunc(self,strFuncName,args):

        self.__mapFunctions[strFuncName](args)


    def LogCollection(self, strCommand, strResponse):
        for i in range(0,10):
            time.sleep(1)
            if self.PubFlag == 0:
                 print "start trace"
                 NowTime = time.strftime("%H:%M:%S", time.localtime())
                 self.strTraceOn = "    [{}]Command:{}\r\n    [{}]Response:{}\r\n".format(str(NowTime), str(strCommand),                                                                                          str(NowTime), str(strResponse))
                 self.PubFlag = 1
                 if self.FinishFlag == 1:
                     self.strTraceOn += "Mordred"
                     self.FinishFlag = 0
                 break

        print self.strTraceOn

    def callFunc(self, strFuncName, args):
        NowTime = time.strftime("%H:%M:%S", time.localtime())
        bRet, ExecResult = self.FindFunc(strFuncName, args)
        if bRet:
            self.HangderFunc(strFuncName, args)
        else:
            self.strTraceOn = "    [{}]Command:{}\r\n    [{}]Response:{}\r\n".format(str(NowTime), str(strFuncName),
                                                                                     str(NowTime), str(ExecResult))


