import logging
import configparser
import sys

'''
reasonId = 0 : Normally end.
reasonId = 1 : End by ERROR.
reasonId = 2 : Terminated by User.
'''

__langdict = None

def exitProgram(reasonId):
        #reasonId = 0 : Normally end.
        #reasonId = 1 : End by ERROR.
        #reasonId = 2 : Terminated by User.
        if (reasonId == 0):
            print(tr("Installation Finished"))
            logging.debug(tr("Installation Finished"))
        if (reasonId == 1):
            print(tr("End by ERROR"))
            logging.debug(tr("End by ERROR"))
        if (reasonId == 2):
            print(tr("Terminated by User"))
            logging.debug(tr("Terminated by User"))
        sys.exit()

'''Des'''
def createInstallationLog():
    installLog = logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',filename='Install.log',level=logging.DEBUG)

'''Des'''
def readConfigFile(section, value):
    config = configparser.ConfigParser()
    config.read('conf.cfg')
    return config[section][value]

def langdict(lang=None):
    if not lang: lang = readConfigFile('System', 'Language')
    global __langdict
    if __langdict is None:
        import os.path
        exec("from languages.lang_%s import lang_dict" % lang)
        __langdict = lang_dict
        for k,v in __langdict.items():
            if not isinstance(k, unicode): k = unicode(k,'utf-8', 'replace')
            if not isinstance(v, unicode): v = unicode(v,'utf-8', 'replace')
            __langdict[k] = v
    return __langdict

def tr(*args):        # old definition was tr(msg, default=-1):
    eles = []
    for ele in args:
        if isinstance(ele, unicode):
            sele = ele
        else:
            if hasattr(ele, "__str__"):
                sele = ele.__str__() #__str__ funciona mejor cuando el objeto es un errorresponse
            else:
                sele = str(ele)
        a =  {True: langdict().get(ele,langdict("en").get(ele,ele)), False: sele}[bool(langdict().get(ele,langdict("en").get(ele,ele)))]
        eles.append("%s" %(a))
    if (eles):
        res = " ".join(eles)
    else:
        res = ""
    if isinstance(res, unicode): return res
    return unicode(res, 'utf8', 'replace')
