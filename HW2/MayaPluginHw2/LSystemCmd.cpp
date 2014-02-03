#include "LSystemCmd.h"


#include <maya/MGlobal.h>
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <list>


const char *stepSizeFlag = "-ss", *stepSizeLongFlag = "-stepsize";
const char *angleFlag = "-a", *angleLongFlag = "-angle";
const char *grammarFlag = "-g", *grammarLongFlag = "-grammar";
const char *iterationsFlag = "-i", *iterationsLongFlag = "-iterations";


LSystemCmd::LSystemCmd() : MPxCommand()
{
}

LSystemCmd::~LSystemCmd() 
{
}

MSyntax LSystemCmd::newSyntax()
{
	MSyntax syntax;
	syntax.addFlag( stepSizeFlag, stepSizeLongFlag, MSyntax::kDouble );
	syntax.addFlag( angleFlag, angleLongFlag, MSyntax::kDouble );
	syntax.addFlag( grammarFlag, grammarLongFlag, MSyntax::kString );
	syntax.addFlag( iterationsFlag, iterationsLongFlag, MSyntax::kLong );
	return syntax;
}

MStatus LSystemCmd::doIt( const MArgList& args )
{
	double stepSize = 0.0;
	double angle = 0.0;
	MString grammar = "";
	int iterations = 0;

	MArgDatabase argData( syntax(), args );

	if( argData.isFlagSet(stepSizeFlag) )
		argData.getFlagArgument( stepSizeFlag, 0, stepSize);

	if( argData.isFlagSet(angleFlag) )
		argData.getFlagArgument( angleFlag, 0, angle);
	
	if( argData.isFlagSet(grammarFlag) )
		argData.getFlagArgument( grammarFlag, 0, grammar);
	
	if( argData.isFlagSet(iterationsFlag) )
		argData.getFlagArgument( iterationsFlag, 0, iterations);


	cout<<"stepSize "<< stepSize <<endl;
	cout<<"angle " << angle<<endl;
	cout<<"iterations " << iterations<<endl;
	cout<<"grammar " << grammar.asChar()<<endl;


	MGlobal::displayInfo("Implement Me!");	
	MGlobal::executeCommand("curve -d 1 -p 0 0 0 -p 0 1 0 -k 0 -k 1 -name curve1");
	MGlobal::executeCommand("circle -r 1 -nr 0 1 0 -name nurbsCircle1");
	MGlobal::executeCommand("select -r nurbsCircle1 curve1");
	MGlobal::executeCommand("extrude -ch true -rn false -po 1 -et 2 -fpt 1 -upn 1 -rotation 0 - scale 1 -rsp 1 nurbsCircle1 curve1");

    return MStatus::kSuccess;
}

