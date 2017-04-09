import svnControl
import dataConnection
import Installer
from Functions import functions

'''
Project: OpenInstaller
Author: Colombo Maximiliano
Documentation: https://drive.google.com/drive/folders/0B4CKD2TRMlffOXlyUWVzSFE5ZnM?usp=sharing
Project Repository: https://github.com/mcolombo87/OrangeInstaller
'''

def consoleApplication():

    functions.createInstallationLog()
    functions.logging.debug('Program started')
    dataConnect = dataConnection.dataConnection()
    installation = Installer.Installer()
    dataConnect.testConnection()
    while (True):
        imputTest = input("Search Company: ")
        resultOfSearch = dataConnect.getDataSearch('company','name',imputTest)
        if (len(resultOfSearch) == 0):
            print ('Company not Found, try again')
        if (len(resultOfSearch) > 1):
            print ("Too many result, select one if it's here")
            for i in range(len(resultOfSearch)):
                if (i > 9):
                    print ("Some result not shown in screen. Choose '666' to search again")
                    break
                print('{}: {}'.format(i, resultOfSearch[i][1]))
            rta = int(input("Please, select one: "))
            if (rta != 666):
                selection = resultOfSearch[rta]
                break
        if (len(resultOfSearch) == 1):
            selection = resultOfSearch[0]
            break
    installation.initialization(selection[0]) #'selection[0]' is value companyId from table 'Company'\
    print('Ready to install OpenOrange for {}'.format(selection[1]))
    rta = input("Are you sure? (Enter to continue, type 'exit' to cancel): ")
    if (rta == 'exit'):
        print('CANCEL INSTALLATION BY USER')
        functions.logging.debug('CANCEL INSTALLATION BY USER')
        functions.exitProgram(2)
    else:
        functions.logging.debug('Ready to install OpenOrange for {}'.format(selection[1]))
        installation.startInstall()

def testing():
    #testObject = svnControl.svnControl()
    #testObject.checkout()
    #print (testObject.getDataSearch('company', 'name', '''%test%'''))
    testObject = Installer.Installer()
    testObject.createInstallationLog()
    pass


'''Start application interface or testing'''
consoleApplication() #Interface Console
#testing() #Testing