import sys

# Imports to use the Maya Python API
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Import the Python wrappers for MEL commands
import maya.cmds as cmds

# The name of the command. 
kPluginCmdName = "pyHelloMaya"

class helloMayaCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, argList):
        argData = OpenMaya.MArgParser (self.syntax(), argList)
        
        msg = 'defaultMessage'
        name = 'defaultName'
        id = 'defaultId'

        if argData.isFlagSet ('name'):
            name = argData.flagArgumentString ('name', 0)
        if argData.isFlagSet ('id'):
            id = argData.flagArgumentString ('id', 0)
            
        msg = "Name: " + name + "\r\n" + "ID: " + id
        
        cmds.confirmDialog( title='Hello Maya Python', message=msg)
        self.setResult("Executed command")
        
def syntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag('n', 'name', OpenMaya.MSyntax.kString)
    syntax.addFlag('id','identification', OpenMaya.MSyntax.kString)
    return syntax

# Create an instance of the command.
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(helloMayaCommand())

# Initialize the plugin
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "cg@penn", "1.0", "2012")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise

# Uninitialize the plugin
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
        raise
