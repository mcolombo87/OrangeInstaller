import platform
import os


"""Tools for operate with distinct OS. Used it to recognize and execute different 
task that we aren't same thing in Windows or Linux, or simply work with system tasks (provided order
to code)"""


def systemInfo():
    currentSystem = platform.system()
    releaseSystem = platform.release()
    return (currentSystem, releaseSystem)

"Return currently OS name"
def osName():
    currentSystem = systemInfo()
    currentSystem = currentSystem[0]
    return currentSystem

"Return True if OS is Linux"
def isLinux():
    name = osName()
    if name == "Linux": return True
    else: return False

"Return True if OS is Windows"
def isWindows():
    name = osName()
    if name == "Windows": return True
    else: return False

'''Des'''
def isPreviuosInstallation():
    return True

'''Des'''
def createShortcut():
    pass
