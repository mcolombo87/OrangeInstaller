import svnControl
import dataConnection
import Installer

'''
Project: OpenInstaller
Author: Colombo Maximiliano
Documentation: https://drive.google.com/drive/folders/0B4CKD2TRMlffOXlyUWVzSFE5ZnM?usp=sharing
Project Repository: https://github.com/mcolombo87/OrangeInstaller
'''

def consoleApplication():

    testObject = dataConnection.dataConnection()
    while (True):
        imputTest = input("Search Company: ")
        a = testObject.getDataSearch('company','name',imputTest)
        if (len(a) == 0):
            print ('Company not Found, try again')
        if (len(a) > 1):
            print ("Too many result, select one if it's here")
            for i in range(len(a)):
                if (i > 9):
                    print ("Some result not shown in screen. Choose '666' to search again")
                    break
                print('{}: {}'.format(i, a[i][1]))
            r = int(input("Please, select one: "))
            if (r != 666):
                selection = a[r]
                break
        if (len(a) == 1):
            selection = a[0]
            break
    installation = Installer.Installer()
    installation.initialization(selection[0]) #'selection[0]' is value companyId from table 'Company'\
    print('Ready to install OpenOrange for {}'.format(selection[1]))
    rta = input("Are you sure? (Enter to continue, type 'exit' to cancel): ")
    if (rta == 'exit'):
        print('CANCEL INSTALLATION BY USER')
    else:
        installation.startInstall()

def testing():
    #testObject = svnControl.svnControl()
    #testObject.checkout()
    #print (testObject.getDataSearch('company', 'name', '''%test%'''))
    #testObject = Installer.Installer()
    #testObject.initialization()
    pass


'''Start application interface or testing'''
consoleApplication() #Interface Console
#testing() #Testing