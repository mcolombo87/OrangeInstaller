import xml.etree.ElementTree as xml
import xml.dom.minidom as xmlDom
import sys

class openSettingsMaker(object):
    """Create Settings file from the company modules installed. Also too, 
    it make a check in the directories for validate installation against 
    Settings file and modules loaded in database"""
    modules = None

    def __init__(self, **kwargs):
        pass

    def createSettings(self, modules):
        settingsXML = xml.Element('settings')
        xmlFile = xml.ElementTree(settingsXML)
        subElement = xml.Element('dbserver')
        subElement.text = 'mysql'
        settingsXML.append(subElement)
        subElement = xml.Element('skin')
        subElement.text = 'GlossyOpen'
        settingsXML.append(subElement)
        subElement = xml.Element('logqueries')
        subElement.text = 'True'
        settingsXML.append(subElement)
        subElement = xml.Element('language')
        subElement.text = 'es'
        settingsXML.append(subElement)
        subElement = xml.Element('webdir')
        subElement.text = ''
        settingsXML.append(subElement)
        subElement = xml.Element('defaultcompany')
        subElement.text = ''
        settingsXML.append(subElement)
        #Starting with modules
        subElement = xml.Element('scriptdir level="0" path="base"')
        settingsXML.append(subElement)
        subElement = xml.Element('scriptdir level="1" path="standard"')
        settingsXML.append(subElement)
        for a in range(len(modules)):
            module = modules[a]
            moduleLevel = str(module[1]) #module[1]. 1 is for Level column in DB
            modulePath = str(module[0]) #module[0]. 0 is for module column in DB
            subElement = xml.Element('scriptdir level="'+moduleLevel+'" path="'+modulePath+'"')
            settingsXML.append(subElement)
        outXMLfile = open('settings.xml','x')
        roughString = xml.tostring(settingsXML, 'utf-8') #From a pretty XML file and not all in same line
        print (roughString)
        xmlReparsed = xmlDom.parseString(roughString).toprettyxml()
        outXMLfile.write(xmlReparsed)