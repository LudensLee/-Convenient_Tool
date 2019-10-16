from PySide2.QtWidgets import QApplication
import subprocess
from lib.SetupUI import cTools
import sys
import os
class cApp(QApplication):
    def __init__(self):
        super(cApp, self).__init__(sys.argv)
        print os.path.abspath(os.curdir)
        Dt = subprocess.Popen(["python", "./Functions.py"])
        self.objMainWindow = cTools(Dt.pid)
        self.objMainWindow.show()
    def Start(self):
        sys.exit(self.exec_())


if __name__ == '__main__':
     objApp = cApp()
     objApp.Start()
