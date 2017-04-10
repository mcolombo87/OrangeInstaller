import platform
import os


"""Tools for operate with distinct OS. Used it to recognize and execute different 
task that we aren't same thing in Windows or Linux, or simply work with system tasks (provided order
to code)"""


def systemInfo():
    currentSystem = platform.system()
    releaseSystem = platform.release()
    return (currentSystem, releaseSystem)

'''Des'''
def isPreviuosInstallation():
    return True

'''Des'''
def createShortcut():
    pass
