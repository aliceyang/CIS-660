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
    # DONE:: declare the input and output class variables
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
        #if plug == LSystemInstanceNode.outputBranches or plug == LSystemInstanceNode.outputFlowers:
        
        print "Compute!\n"
        
        # Retrieve input values from their data handles
        angleData = data.inputValue(LSystemInstanceNode.angle)
        angleValue = angleData.asDouble()
        print "angleValue = %d" % (angleValue)
        
        stepSizeData = data.inputValue(LSystemInstanceNode.stepSize)
        stepSizeValue = stepSizeData.asDouble()
        print "stepSizeValue = %d" % (stepSizeValue)
        
        grammarFileData = data.inputValue(LSystemInstanceNode.grammarFile)
        grammarFileValue = grammarFileData.asString()
        print "grammarFileValue = %s" % (grammarFileValue)
        
        iterationsData = data.inputValue(LSystemInstanceNode.iterations)
        iterationsValue = iterationsData.asDouble()
        print "iterationsValue = %d \n" % (iterationsValue)
        
        # Output values
        outBranchesData = data.outputValue(LSystemInstanceNode.outputBranches) #the MDataHandle
        outBranchesAAD = OpenMaya.MFnArrayAttrsData() #the MFnArrayAttrsData
        outBranchesObject = outBranchesAAD.create() #the MObject
        
        outFlowersData = data.outputValue(LSystemInstanceNode.outputFlowers) #the MDataHandle
        outFlowersAAD = OpenMaya.MFnArrayAttrsData() #the MFnArrayAttrsData
        outFlowersObject = outFlowersAAD.create() #the MObject
        
        # Create the vectors for position, id, scale, and aimDirection (branch end - start) for Branches
        positionArrayBranch = outBranchesAAD.vectorArray("position")
        idArrayBranch = outBranchesAAD.doubleArray("id")
        scaleArrayBranch = outBranchesAAD.vectorArray("scale")
        aimDirArrayBranch = outBranchesAAD.vectorArray("aimDirection")
        
        # Create the vectors for position, id, scale, and aimDirection (branch end - start) for Flowers
        positionArrayFlower = outFlowersAAD.vectorArray("position")
        idArrayFlower = outFlowersAAD.doubleArray("id")
        scaleArrayFlower = outFlowersAAD.vectorArray("scale")
        aimDirArrayFlower = outFlowersAAD.vectorArray("aimDirection")
        
        # TODO:: Run the LSystem and set the positions/ids/ etc
        system = LSystem.LSystem()
        system.loadProgram(str(grammarFileValue))
        system.setDefaultAngle(angleValue)
        system.setDefaultStep(stepSizeValue)
        
        branches = LSystem.VectorPyBranch()
        flowers = LSystem.VectorPyBranch()
                
        for i in range (0, int(iterationsValue)):
            insn = system.getIteration(i)
            print insn
            system.processPy(i, branches, flowers)
            
        # Loop through branches to fill the arrays     
        for idx,branch in enumerate(branches):
            print "===== BRANCH START ===="
            print "idx: " + str(idx)
            print "branch: "
            print branch 
            startPos = OpenMaya.MVector(branch[0], branch[1], branch[2])
            endPos = OpenMaya.MVector(branch[3], branch[4], branch[5])
            dir = endPos - startPos 
            
            positionArrayBranch.append(startPos)
            idArrayBranch.append(idx)
            scaleArrayBranch.append(OpenMaya.MVector(2,2,2))
            aimDirArrayBranch.append(dir)
            print "======== BRANCH END ========\n\n"
                    
        
        # Loop through flowers to fill the arrays
        for flower in flowers:
            print flower      
        
        # Finally set the output data handles
        outBranchesData.setMObject(outBranchesObject)
        outFlowersData.setMObject(outFlowersObject)

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
    LSystemInstanceNode.outputBranches = tAttr.create("outputBranches", "ob", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    
    LSystemInstanceNode.outputFlowers = tAttr.create("outputFlowers", "of", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
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





















