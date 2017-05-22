import logging
import configparser
import sys

'''
reasonId = 0 : Normally end.
reasonId = 1 : End by ERROR.
reasonId = 2 : Terminated by User.
'''
def exitProgram(reasonId):
        #reasonId = 0 : Normally end.
        #reasonId = 1 : End by ERROR.
        #reasonId = 2 : Terminated by User.
        if (reasonId == 0):
            print('Installation Finish')
            logging.debug('Installation Finish')
        if (reasonId == 1):
            print('End by ERROR')
            logging.debug('End by ERROR')
        if (reasonId == 2):
            print('Terminated by User')
            logging.debug('Terminated by User')
        sys.exit()

'''Des'''
def createInstallationLog():
    installLog = logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',filename='Install.log',level=logging.DEBUG)

'''Des'''
def readConfigFile(section, value):
    config = configparser.ConfigParser()
    config.read('conf.cfg')
    return config[section][value]
