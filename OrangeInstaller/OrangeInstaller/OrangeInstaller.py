import argparse
import svnControl
import dataConnection
import Installer
from Functions import functions
from Test import Testing
from GUI import window
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

'''
Project: OrangeInstaller
Author: Colombo Maximiliano
Documentation: https://drive.google.com/drive/folders/0B4CKD2TRMlffOXlyUWVzSFE5ZnM?usp=sharing
Project Repository: https://github.com/mcolombo87/OrangeInstaller
'''

#For use in console.
def consoleApplication():

    functions.createInstallationLog()
    functions.logging.debug('Program started')
    msg = "OrangeInstaller for OpenOrange Software.\nType 'exit' to cancel"
    print(msg)
    dataConnect = dataConnection.dataConnection()
    installation = Installer.Installer()
    dataConnect.testConnection()
    while (True):
        imputTest = raw_input("Search Company: ")
        if (imputTest == 'exit'):
            print('CANCEL INSTALLATION BY USER')
            functions.logging.debug('CANCEL INSTALLATION BY USER')
            functions.exitProgram(2)
        resultOfSearch = dataConnect.getDataSearch('company','name',imputTest)
        if (len(resultOfSearch) == 0):
            print ('Company not Found, try again')
        if (len(resultOfSearch) > 1):
            print ("Too many result, select one if it's here")
            for i in range(len(resultOfSearch)):
                if (i > 9):
                    print ("Some result not shown in screen. Choose '999' to search again")
                    break
                print('{}: {}'.format(i, resultOfSearch[i][1]))
            rta = int(raw_input("Please, select one: "))
            if (rta != 999):
                selection = resultOfSearch[rta]
                break
        if (len(resultOfSearch) == 1):
            selection = resultOfSearch[0]
            break
    installation.initialization(selection[0]) #'selection[0]' is value companyId from table 'Company'\
    print('Default directory for installation: {}\t[If you wish write route of installation type: 0]'.format(installation.getInstallPath()))
    print('Ready to install OpenOrange for {}'.format(selection[1]))
    rta = raw_input("Are you sure? (Enter to continue, type 'exit' to cancel): ")
    if (rta == 0 or rta =='0'):
        print('\t***\tATTENTION: You should write path well or the installation maybe do not work\t***')
        newPath= raw_input("Write new path, for examples type 'help' or type 'cancel' for back to default directory:\n ")
        if (newPath == 'help'):
            msg = 'OS not recognized, help is not available'
            if (installation.getCurrentSystem() == 'Linux'):
                msg = 'Examples for Linux\n\tThe installation be make always over home/user, then only type the folders up it: home/user/ExampleFolder/Open Orange/Company'
            else:
                msg = 'Examples for Windows\n\tFull path: C:\ExampleFolder\Orange Installer\Company'
            print(msg)
            newPath= raw_input("Write new path, or type 'cancel' for back to default directory: ")
        if (newPath !='cancel'):
            installation.setInstallPath(newPath)
        else: print('Default directory for installation: {}'.format(installation.getInstallPath()))
    if (rta == 'exit'):
        print('CANCEL INSTALLATION BY USER')
        functions.logging.debug('CANCEL INSTALLATION BY USER')
        functions.exitProgram(2)
    else:
        functions.logging.debug('Ready to install OpenOrange for {}'.format(selection[1]))
        installation.startInstall()

#For use with GUI, this is main way to use
def userInterface():
    functions.createInstallationLog()
    functions.logging.debug('Program started')
    window.userWindow()
    Gtk.main()
    functions.exitProgram(2)
    
#Start Testing
def testing():
    test = Testing.test()
    #checkModule
    companyId = 1
    moduleToTest1 = "munozvet"
    moduleToTest2 = "munozvet"
    test.testModuleCheckout(companyId,moduleToTest1,moduleToTest2)
    pass


'''Start application interface or testing'''
# Define the parser to take values through prompt interface
parser = argparse.ArgumentParser(description='OrangeInstaller Software help')
parser.add_argument("--console", default=0, action="store_true", help= "for console use")
parser.add_argument("-c", default=0, action="store_true", help= "for console use")
args = parser.parse_args()
if (args.console == True or args.c == True):
    consoleApplication() # Console Interface
else:
    userInterface() #Graphic interface

#testing() #Testing
