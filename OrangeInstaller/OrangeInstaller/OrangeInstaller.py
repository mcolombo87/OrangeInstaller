import svnControl
import dataConnection
import Installer

'''
Project: OpenInstaller
Author: Colombo Maximiliano
Documentation: https://drive.google.com/drive/folders/0B4CKD2TRMlffOXlyUWVzSFE5ZnM?usp=sharing
Project Repository: https://github.com/mcolombo87/OrangeInstaller
'''

#testObject = svnControl.svnControl()
#testObject.checkout()
#testObject = dataConnection.dataConnection()
#a = testObject.testConnection()
#print (testObject.getDataSearch('company', 'name', '''%test%'''))
testObject = Installer.Installer()
testObject.initialization()


