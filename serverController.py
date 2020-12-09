import shutil
from os.path import join
import os
import time
import datetime


class serverController:

    serverStartParameters = '-Xms2048M -Xmx3072M'
    serverJar = 'forge_server.jar'
    lastStatus = ''

    def __init__(self, svName, para, Jar):
        self.svName = svName
        self.serverStartParameters = para
        self.serverJar = Jar

    def getLastStatus(self):
        return self.lastStatus

    def getServerName(self):
        return self.svName

    def server_command(self, cmd):
        os.system('screen -S ' + self.svName + ' -X stuff "{}\015"'.format(cmd))
    
    def getScreen(self):
        output = os.popen('screen -ls').read()
        return output

    def checkStatus(self):
        if self.svName in self.getScreen():
            if self.lastStatus != 'online':
                print('\n' + self.svName + ' is online')
                self.lastStatus = 'online'
            return True
        else:
            if self.lastStatus != 'offline':
                print('\n' + self.svName + ' is offline')
                self.lastStatus = 'offline'
            return False

    def checkCrash(self):
        try:
            crashes = os.listdir(self.svName + '/crash-reports')
            
        except:
            return False

        isCrash = False
        for item in crashes:
            if os.path.isfile(self.svName + '/crash-reports/' + item):
                createTime = os.path.getctime(self.svName + '/crash-reports/' + item)
                if(time.time() - createTime < 10):
                    isCrash = True

        return isCrash

    def getCrashReport(self):
        try:
            crashes = os.listdir(self.svName + '/crash-reports')
        except:
            return ''

        lastCrashTime = 0
        lastCrashReport = ''
        for item in crashes:
            if os.path.isfile(self.svName + '/crash-reports/' + item):
                createTime = os.path.getctime(self.svName + '/crash-reports/' + item)
                if(createTime > lastCrashTime):
                    lastCrashTime = createTime
                    lastCrashReport = item

        return self.svName + '/crash-reports/' + lastCrashReport
        

    def startServer(self):
        if not self.checkStatus():
            os.chdir(self.svName)
            os.system('screen -dmS ' + self.svName + ' java ' + self.serverStartParameters + ' -jar ' + self.serverJar + ' nogui')
            print(self.svName + ' is starting')
            return True
        else:
            print(self.svName + ' already started.')
            return False

    def stopServer(self):
        if self.checkStatus():
            self.server_command('stop')
            print("Server stopped.")
            return True
        else:
            print("Server not running.")
            return False

    def checkRestart(self):
        if not self.checkStatus():
            if self.checkCrash():
                return True
            else:
                return False
        else:
            return False