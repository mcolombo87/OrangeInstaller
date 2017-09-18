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

tr = functions.tr

#For use in console.
def consoleApplication():

    functions.createInstallationLog()
    functions.logging.debug(tr("Program started"))
    msg  = tr("OrangeInstaller for OpenOrange Software.\n")
    msg += tr("Type 'exit' to cancel")
    print(msg)
    dataConnect = dataConnection.dataConnection()
    installation = Installer.Installer()
    dataConnect.testConnection()

    invalidCode = False
    validCode = False
    while not validCode:
        imputTest = raw_input(tr("Company Code: "))
        if len(imputTest) == 8:
            codeToSearch = dataConnect.getDataSearch('company_keys', 'companykey', imputTest, "*")
            if codeToSearch:
                validCode = True
                break
            else:
                invalidCode = True
        else:
            invalidCode = True
        if invalidCode:
            print tr("Invalid company code, try again.")
        else: break

    selection = None
    while codeToSearch[0][0] == "0pen0r4n":
        imputTest = raw_input(tr("Search Company: "))
        if (imputTest == tr('exit')):
            print(tr("CANCEL INSTALLATION BY USER"))
            functions.logging.debug(tr("CANCEL INSTALLATION BY USER"))
            functions.exitProgram(2)
        resultOfSearch = dataConnect.getDataSearch('company', 'name', imputTest, "*")
        if (len(resultOfSearch) == 0):
            print (tr("Company not Found, try again"))
        if (len(resultOfSearch) > 1):
            print (tr("Too many results, choose one from this list:"))
            for i in range(len(resultOfSearch)):
                if (i > 9):
                    print (tr("Some result not shown in screen." + tr(" Type '999' to search again")))
                    break
                print('{}: {}'.format(i, resultOfSearch[i][1]))
            rta = int(raw_input(tr("Please, select one: ")))
            if (rta != 999):
                selection = resultOfSearch[rta]
                break
        if (len(resultOfSearch) == 1):
            selection = resultOfSearch[0]
            break

    if not selection:
        installation.setSvnControlLogon(codeToSearch[0][1],codeToSearch[0][2])
        selection = dataConnect.getDataSearch('company', 'idcompany', codeToSearch[0][3], "*")[0]
    installation.initialization(selection[0]) #'selection[0]' is value companyId from table 'Company'\
    if selection[1]:
        installation.setInstallPath(installation.getInstallPath(), selection[1])
    print(tr("Default directory for installation: ") + "{}\t".format(installation.getInstallPath()) + tr("[If you wish write route of installation type: 0]"))
    print(tr("Ready to install OpenOrange for ") + "{}".format(selection[1]))
    rta = raw_input(tr("Are you sure? (Enter to continue, type 'exit' to cancel): "))
    if (rta == 0 or rta =='0'):
        print(tr("\t***\tATTENTION: You should write path well or the installation may not work\t***"))
        newPath= raw_input(tr("Write new path, for examples type 'help' or type 'cancel' for back to default directory:\n "))
        if (newPath == tr("help")):
            msg = 'OS not recognized, help is not available'
            if (installation.getCurrentSystem() == 'Linux'):
                msg = tr("Examples for Linux\n\tThe installation has to be over home/user, for example: home/user/ExampleFolder/Company")
            else:
                msg = tr("Examples for Windows\n\tFull path: C:\ExampleFolder\Orange Installer\Company")
            print(msg)
            newPath = raw_input(tr("Write new path, or type 'cancel' for back to default directory: "))
        if (newPath != tr("cancel")):
            installation.setInstallPath(newPath)
        else: print(tr("Default directory for installation: ") + "{}".format(installation.getInstallPath()))
    if (rta == tr("exit")):
        print(tr("CANCEL INSTALLATION BY USER"))
        functions.logging.debug(tr("CANCEL INSTALLATION BY USER"))
        functions.exitProgram(2)
    else:
        functions.logging.debug(tr("Ready to install OpenOrange for ") + "{}".format(selection[1]))
        installation.startInstall()

#For use with GUI, this is main way to use
def userInterface():
    functions.createInstallationLog()
    functions.logging.debug(tr("Program started"))
    window.userWindow()
    Gtk.main()
    functions.exitProgram(2)

#Start Testing
def testing():
    test = Testing.test()
    test.checkSystemTools()
    #checkModule
    companyId = 1
    moduleToTest1 = "munozvet"
    moduleToTest2 = "munozvet"
    test.testModuleCheckout(companyId,moduleToTest1,moduleToTest2)
    pass

'''Start application interface or testing'''
# Define the parser to take values through prompt interface
parser = argparse.ArgumentParser(description = "OrangeInstaller Software Help")
parser.add_argument("--console", default = 0, action="store_true", help = "for console use")
parser.add_argument("-c", default = 0, action = "store_true", help = "for console use")
parser.add_argument("--test", default = 0, action = "store_true", help = "for test soft, don't use")
args = parser.parse_args()
if (args.test == True):
    testing() # run test
if (args.console == True or args.c == True):
    consoleApplication() # Console Interface
else:
    userInterface() #Graphic interface

#testing() #Testing
