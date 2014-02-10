# Alice Yang | CIS 660 HW 3
# LSystemInstanceNode.py
# Creates L-System geometry as instances of input geometries

import sys
import random
import LSystem

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)
    
# Define the name of the node
kPluginNodeTypeName = "LSystemInstanceNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
LSystemInstanceNodeId = OpenMaya.MTypeId(0x8705)

# Node definition
class LSystemInstanceNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    
    angle = OpenMaya.MObject()
    stepSize = OpenMaya.MObject()
    grammarFile = OpenMaya.MObject()
    iterations = OpenMaya.MObject()
    
    outputBranches = OpenMaya.MObject()
    outputFlowers = OpenMaya.MObject()
    
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        
        
    # compute
    def compute(self,plug,data):
        # IN PROGRESS:: create the main functionality of the node.
        data.setClean(plug)

# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    
    # DONE:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    
    # Input attributes
    LSystemInstanceNode.angle = nAttr.create("angle", "a", OpenMaya.MFnNumericData.kDouble, 0.0)
    MAKE_INPUT(nAttr)
    
    LSystemInstanceNode.stepSize = nAttr.create("stepSize", "ss", OpenMaya.MFnNumericData.kDouble, 0.0)
    MAKE_INPUT(nAttr)
    
    LSystemInstanceNode.grammarFile = tAttr.create("grammarFile", "g", OpenMaya.MFnData.kString)
    MAKE_INPUT(nAttr)
    
    LSystemInstanceNode.iterations = nAttr.create("iterations", "i", OpenMaya.MFnNumericData.kDouble, 0.0)
    MAKE_INPUT(nAttr)
        
    # Output attributes
    LSystemInstanceNode.outputBranches = tAttr.create("outBranches", "ob", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    
    LSystemInstanceNode.outputFlowers = tAttr.create("outFlowers", "of", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    
    try:
        # DONE:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print "Initialization!\n"
        
        # Add attributes
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.angle)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.stepSize)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.grammarFile)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.iterations)
        
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.outputBranches)        
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.outputFlowers)        
        
        # Set attributeAffects
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle,LSystemInstanceNode.outputFlowers)
        
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.stepSize,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.stepSize,LSystemInstanceNode.outputFlowers)
        
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.grammarFile,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.grammarFile,LSystemInstanceNode.outputFlowers)
        
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iterations,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iterations,LSystemInstanceNode.outputFlowers)
        
    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )
        
        
# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstanceNode() )
    
# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, LSystemInstanceNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )


# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( LSystemInstanceNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )





















