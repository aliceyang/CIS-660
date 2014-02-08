# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random

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
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    
    inNumPoints = OpenMaya.MObject()
    
    minX = OpenMaya.MObject()
    minY = OpenMaya.MObject()
    minZ = OpenMaya.MObject()
    minVector = OpenMaya.MObject()
    
    maxX = OpenMaya.MObject()
    maxY = OpenMaya.MObject()
    maxZ = OpenMaya.MObject()
    maxVector = OpenMaya.MObject()
    
    outPoints = OpenMaya.MObject()
        
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # IN PROGRESS:: create the main functionality of the node. Your node should 
        #         take in three floats for max position (X,Y,Z), three floats 
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData 
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData. 
        
        if plug == randomNode.outPoints:
        
            print "Compute!\n"
            
            # Retrieve input values from their data handles
            inNumPointsData = data.inputValue(randomNode.inNumPoints)
            inNumPointsValue = inNumPointsData.asFloat()
            
            minVectorData = data.inputValue(randomNode.minVector)
            minVectorData = minVectorData.asFloat3()
            
            maxVectorData = data.inputValue(randomNode.maxVector)
            maxVectorData = maxVectorData.asFloat3()
            
            # Output value
            pointsData = data.outputValue(randomNode.outPoints) #the MDataHandle
            pointsAAD = OpenMaya.MFnArrayAttrsData() #the MFnArrayAttrsData
            pointsObject = pointsAAD.create() #the MObject
            
            # Create the vectors for position and id
            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")
            
            # TODO:: Loop to fill the arrays: 
            for num in range(0, inNumPointsValue):
                startx = random.uniform(minVectorData[0], maxVectorData[0])
                starty = random.uniform(minVectorData[1], maxVectorData[1])
                startz = random.uniform(minVectorData[2], maxVectorData[2])
                
                positionArray.append(OpenMaya.MVector(startx, starty, startz))
                idArray.append(num) 
            
            # Finally set the output data handle 
            pointsData.setMObject(pointsObject) 
            
        data.setClean(plug)
    
# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # DONE:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    
    # Input attributes
    randomNode.inNumPoints = nAttr.create("numPoints", "n", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    
    randomNode.minX = nAttr.create("minX", "miX", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minY = nAttr.create("minY", "miY", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minZ = nAttr.create("minZ", "miZ", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minVector = nAttr.create("minVector", "miV", randomNode.minX, randomNode.minY, randomNode.minZ)
    MAKE_INPUT(nAttr)
        
    randomNode.maxX = nAttr.create("maxX", "maX", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxY = nAttr.create("maxY", "maY", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxZ = nAttr.create("maxZ", "maZ", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxVector = nAttr.create("maxVector", "maV", randomNode.maxX, randomNode.maxY, randomNode.maxZ)
    MAKE_INPUT(nAttr)
    
    # Output attributes
    randomNode.outPoints = tAttr.create("outPoints", "op", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    
    try:
        # DONE:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print "Initialization!\n"
        
        # Add attributes
        randomNode.addAttribute(randomNode.inNumPoints)
        
        #randomNode.addAttribute(randomNode.minX)
        #randomNode.addAttribute(randomNode.minY)
        #randomNode.addAttribute(randomNode.minZ)
        randomNode.addAttribute(randomNode.minVector)
        
        #randomNode.addAttribute(randomNode.maxX)
        #randomNode.addAttribute(randomNode.maxY)
        #randomNode.addAttribute(randomNode.maxZ)
        randomNode.addAttribute(randomNode.maxVector)
        
        randomNode.addAttribute(randomNode.outPoints)    
        
        # Set attributeAffects
        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.minVector, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.maxVector, randomNode.outPoints)   

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
