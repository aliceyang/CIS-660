#include "LSystemCmd.h"


#include <maya/MGlobal.h>
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include "LSystem.h"
#include "vec.h"
#include <list>
#include <sstream>


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


	cout << "stepSize "<< stepSize << endl;
	cout << "angle " << angle << endl;
	cout << "iterations " << iterations << endl;
	cout << "grammar " << grammar.asChar() << endl;

	// Run the included L-System implementation
	LSystem system;
	system.loadProgramFromString(grammar.asChar());
	system.setDefaultAngle(angle);
	system.setDefaultStep(stepSize);
	std::vector<LSystem::Branch> branches;

	for (int i = 0; i < iterations; i++)
	{
		std::string insn = system.getIteration(i);
		cout << insn << endl;
        system.process(i, branches);
	}

	// Draw the branches from the final iteration
	for (int j = 0; j < branches.size(); j++)
	{
		vec3 start = branches.at(j).first;
		vec3 end = branches.at(j).second;

		std::string cmd;
		std::stringstream ss;

		// Create the branch using a curve. We use the z-value in each branch point as the y-value in Maya because in Maya y is the up-axis.
		MGlobal::executeCommand("global string $myCurve");
		ss << "$myCurve = `curve -d 1 -p " << start[0]	<< " " << start[2]	<< " " << start[1]	<< 
						" -p " << end[0]	<< " " << end[2]	<< " " << end[1]	<<
						 "-k 0 -k 1`";
		cmd = ss.str();
		MString mayaCmd = cmd.c_str();

		MGlobal::executeCommand(mayaCmd);
		MGlobal::executeCommand("circle -r 0.2 -name nurbsCircle1");
		MGlobal::executeCommand("select -r nurbsCircle1 curve1");
		MGlobal::executeCommand("extrude -ch true -rn false -po 1 -et 2 -ucp 1 -fpt 1 -upn 1 -rotation 0 -scale 1 -rsp 1 nurbsCircle1 $myCurve");
	}	
    return MStatus::kSuccess;
}

