#define MNoVersionString
#define MNoPluginEntry

#include <maya/MFnPlugin.h>
#include <maya/MTime.h>
#include <maya/MFnMesh.h>
#include <maya/MPoint.h>
#include <maya/MFloatPoint.h>
#include <maya/MFloatPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MDoubleArray.h>

#include <maya/MFnUnitAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MPxNode.h>
#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MFnMeshData.h>

#include <maya/MIOStream.h>

MStatus returnStatus;

// Igor's preprocessors: To use, simply do something like
// time = unitAttr.create( "time", "tm", MFnUnitAttribute::kTime, 0.0, &returnStatus );
// McheckErr(returnStatus, "ERROR creating animCube time attribute\n");
// MAKE_INPUT(unitAttr);
#define McheckErr(stat,msg)			\
	if ( MS::kSuccess != stat ) {	\
		cerr << msg;				\
		return MS::kFailure;		\
	}

#define MAKE_INPUT(attr) \
CHECK_MSTATUS(attr.setKeyable(true)); \
CHECK_MSTATUS(attr.setStorable(true)); \
CHECK_MSTATUS(attr.setReadable(true)); \
CHECK_MSTATUS(attr.setWritable(true));

#define MAKE_OUTPUT(attr) \
CHECK_MSTATUS(attr.setKeyable(false)); \
CHECK_MSTATUS(attr.setStorable(false)); \
CHECK_MSTATUS(attr.setReadable(true)); \
CHECK_MSTATUS(attr.setWritable(false));

#define MAKE_ADDR(attr) \
CHECK_MSTATUS(attr.setKeyable(false)); \
CHECK_MSTATUS(attr.setStorable(false)); \
CHECK_MSTATUS(attr.setReadable(true)); \
CHECK_MSTATUS(attr.setWritable(false)); \
CHECK_MSTATUS(attr.setHidden(true));

class LSystemNode : public MPxNode
{
public:
	LSystemNode() {};
	virtual ~LSystemNode() {};
	virtual MStatus compute(const MPlug& plug, MDataBlock& data);
	static  void*	creator();
	static  MStatus initialize();
	
public:
	static MTypeId id;
	static MObject time;
	static MObject angle;
	static MObject stepSize;
	static MObject grammarFile;
	static MObject outputMesh;

//protected:
//	MObject createMesh(const MTime& time, MObject& outData, MStatus& stat);
};

// This initializes the node’s identifier to a unique tag
MTypeId LSystemNode::id (0x0); 

//The attributes of the node are initialized to NULL values. 
MObject LSystemNode::time;
MObject LSystemNode::angle;
MObject LSystemNode::stepSize;
MObject LSystemNode::grammarFile;
MObject LSystemNode::outputMesh;

// The creator() method simply returns new instances of this node. The return type is a void* so
// Maya can create node instances internally in a general fashion without having to know the return type.
void* LSystemNode::creator()
{
	return new LSystemNode;
}

// The initialize method is called only once when the node is first registered with Maya. In this method 
// you define the attributes of the node, what data comes in and goes out of the node that other nodes may want to connect to. 
MStatus LSystemNode::initialize()
{
	MFnNumericAttribute numAttr;
	MFnTypedAttribute typedAttr;
	MFnUnitAttribute unitAttr;

	MStatus returnStatus;

	// Create attributes
	LSystemNode::time = unitAttr.create( "time", "tm", MFnUnitAttribute::kTime, 0.0, &returnStatus );
	McheckErr(returnStatus, "ERROR creating LSystemNode time attribute\n");
	MAKE_INPUT(unitAttr);

	LSystemNode::angle = numAttr.create( "angle", "a", MFnNumericData::kDouble, 0.0, &returnStatus );
	McheckErr(returnStatus, "ERROR creating LSystemNode angle attribute\n");
	MAKE_INPUT(numAttr);

	LSystemNode::stepSize = numAttr.create( "stepSize", "ss", MFnNumericData::kDouble, 0.0, &returnStatus );
	McheckErr(returnStatus, "ERROR creating LSystemNode stepSize attribute\n");
	MAKE_INPUT(numAttr);

	LSystemNode::grammarFile = typedAttr.create( "grammarFile", "g", MFnData::kString, &returnStatus );
	McheckErr(returnStatus, "ERROR creating LSystemNode grammarFile attribute\n");
	MAKE_INPUT(typedAttr);

	LSystemNode::outputMesh = typedAttr.create( "outputMesh", "out", MFnData::kMesh, &returnStatus );
	McheckErr(returnStatus, "ERROR creating LSystemNode outputMesh attribute\n");
	MAKE_OUTPUT(typedAttr);

	// Add attributes
	returnStatus = addAttribute(LSystemNode::time);
	McheckErr(returnStatus, "ERROR adding time attribute\n");

	returnStatus = addAttribute(LSystemNode::angle);
	McheckErr(returnStatus, "ERROR adding angle attribute\n");

	returnStatus = addAttribute(LSystemNode::stepSize);
	McheckErr(returnStatus, "ERROR adding stepSize attribute\n");

	returnStatus = addAttribute(LSystemNode::grammarFile);
	McheckErr(returnStatus, "ERROR adding grammarFile attribute\n");

	returnStatus = addAttribute(LSystemNode::outputMesh);
	McheckErr(returnStatus, "ERROR adding outputMesh attribute\n");

	// Connect inputs to outputs via attributeAffects
	returnStatus = attributeAffects(LSystemNode::time, LSystemNode::outputMesh);
	McheckErr(returnStatus, "ERROR in attributeAffects\n");
	
	returnStatus = attributeAffects(LSystemNode::angle, LSystemNode::outputMesh);
	McheckErr(returnStatus, "ERROR in attributeAffects\n");

	returnStatus = attributeAffects(LSystemNode::stepSize, LSystemNode::outputMesh);
	McheckErr(returnStatus, "ERROR in attributeAffects\n");

	returnStatus = attributeAffects(LSystemNode::grammarFile, LSystemNode::outputMesh);
	McheckErr(returnStatus, "ERROR in attributeAffects\n");

	return MS::kSuccess;
}

MStatus LSystemNode::compute(const MPlug& plug, MDataBlock& data)
{
	return MS::kSuccess;
}
