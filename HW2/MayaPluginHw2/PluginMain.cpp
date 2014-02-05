#include <maya/MPxCommand.h>
#include <maya/MFnPlugin.h>
#include <maya/MIOStream.h>
#include <maya/MString.h>
#include <maya/MArgList.h>
#include <maya/MGlobal.h>
#include <maya/MSimple.h>
#include <maya/MDoubleArray.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MDGModifier.h>
#include <maya/MPlugArray.h>
#include <maya/MVector.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MStringArray.h>
#include <list>

#include "LSystemCmd.h"
#include "LSystemNode.h"

MStatus initializePlugin( MObject obj )
{
    MStatus   status = MStatus::kSuccess;
    MFnPlugin plugin( obj, "MyPlugin", "1.0", "Any");

    // Register Command
	status = plugin.registerCommand( "LSystemCmd", LSystemCmd::creator, LSystemCmd::newSyntax );
    if (!status) {
        status.perror("registerCommand");
        return status;
    }

	// Set name
	plugin.setName("LSystem");

	// Load UI from MEL file
	MGlobal::executeCommand("source \"" + plugin.loadPath() + "/ui.mel\"");
	status = plugin.registerUI("createLSystemUI", "deleteLSystemUI");

	// Register Node
	status = plugin.registerNode("LSystemNode", LSystemNode::id, LSystemNode::creator, LSystemNode::initialize);
	CHECK_MSTATUS_AND_RETURN_IT(status);

    return status;
}

MStatus uninitializePlugin( MObject obj )
{
    MStatus   status = MStatus::kSuccess;
    MFnPlugin plugin( obj );

	// Deregister Command
    status = plugin.deregisterCommand( "LSystemCmd" );
    if (!status) {
	    status.perror("deregisterCommand");
	    return status;
    }

	// Deregister Node
	status = plugin.deregisterNode(LSystemNode::id);
	CHECK_MSTATUS_AND_RETURN_IT(status);
}


