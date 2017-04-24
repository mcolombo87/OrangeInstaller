import xml.etree.ElementTree as xml
import xml.dom.minidom as xmlDom
from Functions import functions
import sys

class openSettingsMaker(object):
    """Create Settings file from the company modules installed. Also too, 
    it make a check in the directories for validate installation against 
    Settings file and modules loaded in database"""
    modules = None

    def __init__(self, **kwargs):
        pass

    def createSettings(self, outXMLfile, modules, companyInfo):
        companyInfo = companyInfo[0] #Extract lonely vector from list (this come from getData)
        settingsXML = xml.Element('settings')
        xmlFile = xml.ElementTree(settingsXML)
        subElement = xml.Element('dbserver')
        subElement.text = str(companyInfo[2])
        settingsXML.append(subElement)
        subElement = xml.Element('skin')
        subElement.text = str(companyInfo[3])
        settingsXML.append(subElement)
        subElement = xml.Element('logqueries')
        if(str(companyInfo[4]) == 0):
            subElement.text = 'False'
        else:
            subElement.text = 'True'
        settingsXML.append(subElement)
        subElement = xml.Element('language')
        subElement.text = str(companyInfo[5])
        settingsXML.append(subElement)
        subElement = xml.Element('beep_on_queries')
        subElement.text = str(companyInfo[6])
        settingsXML.append(subElement)
        subElement = xml.Element('webdir')
        subElement.text = str(companyInfo[7])
        settingsXML.append(subElement)
        subElement = xml.Element('defaultcompany')
        subElement.text = str(companyInfo[8])
        settingsXML.append(subElement)
        #Starting with modules
        for a in range(len(modules)):
            module = modules[a]
            moduleLevel = str(module[1]) #module[1]. 1 is for Level column in DB
            modulePath = str(module[0]) #module[0]. 0 is for module column in DB
            if (moduleLevel == '1'):
                subElement = xml.Element('scriptdir level="0" path="base"')
                settingsXML.append(subElement)
                subElement = xml.Element('scriptdir level="1" path="standard"')
                settingsXML.append(subElement)
            else:
                subElement = xml.Element('scriptdir level="'+moduleLevel+'" path="'+modulePath+'"')
                settingsXML.append(subElement)
        roughString = xml.tostring(settingsXML, 'utf-8') #From a pretty XML file and not all in same line
        xmlReparsed = xmlDom.parseString(roughString).toprettyxml()
        outXMLfile.write(xmlReparsed)
        functions.logging.debug('Settings.XML create: '.format(roughString))