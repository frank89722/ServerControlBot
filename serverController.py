import shutil
from os.path import join
import os
import time
import datetime


class serverController:

    serverStartParameters = '-Xms2048M -Xmx3072M'
    serverJar = 'forge_server.jar'
    lastStatus = ''

    def __init__(self, svName, serverStartParameters, serverJar, bot_dir):
        self.svName = svName
        self.serverStartParameters = serverStartParameters
        self.serverJar = serverJar
        self.bot_dir= bot_dir

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
                print(self.svName + ' is online')
                self.lastStatus = 'online'
            return True
        else:
            if self.lastStatus != 'offline':
                print(self.svName + ' is offline')
                self.lastStatus = 'offline'
            return False

    def checkCrash(self):
        try:
            crashes = os.listdir(self.bot_dir + self.svName + '/crash-reports')
            
        except:
            return False

        isCrash = False
        for item in crashes:
            if os.path.isfile(self.bot_dir + self.svName + '/crash-reports/' + item):
                createTime = os.path.getctime(self.bot_dir + self.svName + '/crash-reports/' + item)
                if(time.time() - createTime < 10):
                    isCrash = True

        return isCrash

    def getCrashReport(self):
        try:
            crashes = os.listdir(self.bot_dir + self.svName + '/crash-reports')
        except:
            return ''

        lastCrashTime = 0
        lastCrashReport = ''
        for item in crashes:
            if os.path.isfile(self.bot_dir + self.svName + '/crash-reports/' + item):
                createTime = os.path.getctime(self.bot_dir + self.svName + '/crash-reports/' + item)
                if(createTime > lastCrashTime):
                    lastCrashTime = createTime
                    lastCrashReport = item

        return self.bot_dir + self.svName + '/crash-reports/' + lastCrashReport
        
    def startServer(self):
        if not self.checkStatus():
            os.chdir(self.bot_dir + self.svName)
            os.system('screen -dmS ' + self.svName + ' java ' + self.serverStartParameters + ' -jar ' + self.serverJar + ' nogui')
            print(self.svName + ' is starting')
            return True
        else:
            print(self.svName + ' already started.')
            return False

    def stopServer(self):
        if self.checkStatus():
            self.server_command('stop')
            print('Shutting down' + self.svName)
            return True
        else:
            print(self.svName + ' is not running.')
            return False

    def killServer(self):
        if self.checkStatus():
            os.system('screen -X -S ' + self.svName + ' kill')
            print(self.svName + ' killed')
            return True
        else:
            print(self.svName + ' is not running.')
            return False

    def checkRestart(self):
        if not self.checkStatus():
            if self.checkCrash():
                return True
            else:
                return False
        else:
            return False