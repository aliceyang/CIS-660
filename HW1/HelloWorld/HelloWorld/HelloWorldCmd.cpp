//
// Copyright (C) 
// 
// File: HelloWorldCmd.cpp
//
// MEL Command: HelloWorld
//
// Author: Maya Plug-in Wizard 2.0.1
// Revised by Isaac Peral
//

// Includes everything needed to register a simple MEL command with Maya.
// 
#include <maya/MPxCommand.h>
#include <maya/MObject.h>
#include <maya/MFnPlugin.h>
#include <maya/MSimple.h>
#include <maya/MGlobal.h>

#define EXPORT _declspec(dllexport) 
// define EXPORT for exporting as .dll, 
// (Do not need if you use ‘Maya PluginWizard‘) 
// custom Maya command 
class helloMaya: public MPxCommand 
{ 
public: 
	virtual MStatus doIt( const MArgList& args) 
	{ 
		MStatus status; 
		MString name = "defaultName";
		MString id = "defaultId";

		unsigned index;
		index = args.flagIndex("n", "name");
		if (index != MArgList::kInvalidArgIndex)
		{
			args.get(index + 1, name);
		}
		
		index = args.flagIndex("id");
		if (index != MArgList::kInvalidArgIndex)
		{
			args.get(index + 1, id);
		}

		MString confDialog("confirmDialog -t \"Hello Maya\"");
		MString message("Name: " + name + "\\r\\n" + "ID: " + id);
		MGlobal::executeCommand(confDialog + " -m " + "\"" + message + "\"");
		return status; 
	} 
	static void *creator() { return new helloMaya; } 
}; 
// Initialize Plugin upon loading 
EXPORT MStatus initializePlugin(MObject obj) 
{ 
	MStatus stat; 
	MFnPlugin plugin( obj, "CIS660", "1.0", "Any"); 
	stat = plugin.registerCommand("helloMaya", helloMaya::creator ); 
	if (!stat) stat.perror( "registerCommand failed" );
	return stat; 
} 
// Cleanup Plugin upon unloading 
EXPORT MStatus uninitializePlugin(MObject obj) 
{ 
	MStatus stat; 
	MFnPlugin plugin(obj); 
	stat = plugin.deregisterCommand("helloMaya"); 
	if(!stat) stat.perror( "deregisterCommand failed" ); 
	return stat; 
}