# Alice Yang | CIS 660 HW 3
# randomNode.py: Produces random locations to be used with the Maya instancer node.
# LSystemInstanceNode.py: Creates L-System geometry as instances of input geometries

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
    
    
#==============================================
#================== Random Node ===============
#==============================================
# Define the name of the node
kPluginRandomNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # DONE:: declare the input and output class variables
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
            
            # DONE:: Loop to fill the arrays: 
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
def randomNodeInitializer():
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
        randomNode.addAttribute(randomNode.minVector)
        randomNode.addAttribute(randomNode.maxVector)
        randomNode.addAttribute(randomNode.outPoints)    
        
        # Set attributeAffects
        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.minVector, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.maxVector, randomNode.outPoints)   

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginRandomNodeTypeName) )

# creator
def randomNodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )



















#==============================================
#============= LSystemInstanceNode ============
#==============================================
    
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
            #switching y & z values because of Maya's vertical y-axis positioning
            startPos = OpenMaya.MVector(branch[0], branch[2], branch[1]) 
            endPos = OpenMaya.MVector(branch[3], branch[5], branch[4])
            dir = endPos - startPos 
            
            positionArrayBranch.append(startPos)
            idArrayBranch.append(idx)
            scaleArrayBranch.append(OpenMaya.MVector(1,1,1))
            aimDirArrayBranch.append(dir)
            print "======== BRANCH END ========\n\n"
                    
        
        # Loop through flowers to fill the arrays
        for idx, flower in enumerate(flowers):
            print "=====FLOWER START===="
            print "idx: " + str(idx)
            print "flower:"
            print flower
            #switching y & z values because of Maya's vertical y-axis positioning
            pos = OpenMaya.MVector(flower[0], flower[2], flower[1])
            
            positionArrayFlower.append(pos)
            idArrayFlower.append(idx)
            scaleArrayFlower.append(OpenMaya.MVector(1,1,1))
            aimDirArrayFlower.append(OpenMaya.MVector(1,1,1))
        
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
    
    # RandomNode
    try:
        mplugin.registerNode( kPluginRandomNodeTypeName, randomNodeId, randomNodeCreator, randomNodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginRandomNodeTypeName )
        
    # LSystemInstanceNode
    try:
        mplugin.registerNode( kPluginNodeTypeName, LSystemInstanceNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )


# uninitialize the script plug-in
def uninitializePlugin(mobject):
    # RandomNode
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginRandomNodeTypeName )

    # LSystemInstanceNode
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( LSystemInstanceNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )


