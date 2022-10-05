######################################################################
#
# This is a partial copy from LeBailFitScript.py
#
# Python Script as Step 1 of Le Bail Fitting to
# 1. Load file
# 2. Create LeBailFitInput
# 3. Fit Peaks
#
# Step 1:   Load data, model (HKL list) and starting instrument parameters values,
#           and do an initial LeBailFit/calculation to see how much the starting
#           values are off;
#
######################################################################
from Calibration_ImportInformation import *

global numsteps 

numsteps = 2002  # Step 4
numprofsteps = 20000 # Step 4.1 (step 5)

#--------------  Definition of Global Variables ---------------------
bankid = 0

datafilename = "" 
hklfilename = ""
irffilename = ""

datawsname = ""
instrparamwsname = ""
braggpeakparamwsname = ""

# Range for Le Bail Fit of all peaks 
startx = -1
endx =  -1

# Range for fitting single peaks for step 1~3 
tofmin_singlepeaks = -1
tofmax_singlepeaks = -1

# Background related
backgroundtype = "Polynomial"
backgroundorder = 6
bkgdtablewsname = ""
bkgdwsname = ""
bkgdfilename = ""
usrbkgdpoints = ''

latticesize = 4.1568899999999998
#--------------------------------------------------------------------

def setupGlobals(infofilename):
    """ Set up globals values
    """

    global datafilename, hklfilename, irffilename  
    global datawsname, instrparamwsname, braggpeakparamwsname
    global bkgdtablewsname, bkgdwsname, bkgdfilename, backgroundorder
    global tofmin_singlepeaks, tofmax_singlepeaks, startx, endx
    global bankid, latticesize
    global usrbkgdpoints

    bankid, calibDict = importCalibrationInformation(infofilename)
    bankid = int(bankid)

    datafilename = calibDict["DataFileDir"] + calibDict[bankid]["DataFileName"] 
    hklfilename  = calibDict["HKLFileDir"]  + calibDict[bankid]["HKLFileName"]
    irffilename  = calibDict["IrfFileDir"]  + calibDict[bankid]["IrfFileName"]
    
    startx = float(calibDict[bankid]["LeBailFitMinTOF"])
    endx   = float(calibDict[bankid]["LeBailFitMaxTOF"])

    # Name of workspaces
    datawsname = calibDict[bankid]["DataWorkspace"]
    instrparamwsname     = "Bank%sInstrumentParameterTable" % (bankid)
    braggpeakparamwsname = 'BraggPeakParameterTable'

    # Background related
    usrbkgdpoints   = calibDict[bankid]["UserSpecifiedBkgdPts"]
    bkgdwsname      = datawsname+"_Background"
    backgroundtype  = calibDict["BackgroundType"]
    backgroundorder = int(calibDict["BackgroundOrder"])
    bkgdfilename    = calibDict["WorkingDir"] + datawsname + "_Parameters.bak'"
    bkgdwsname      = datawsname + "_Background"
    bkgdtablewsname = datawsname + "_Background_Parameters"

    # Other constants
    latticesize   = calibDict[bankid]["LatticeSize"]

    return

def generateMCSetupTable(wsname):
    """ Generate a Le Bail fit Monte Carlo random walk setup table
    """
    import mantid.simpleapi as api
    
    tablews = api.CreateEmptyTableWorkspace(OutputWorkspace=str(wsname))
    
    tablews.addColumn("str", "Name")
    tablews.addColumn("double", "A0")
    tablews.addColumn("double", "A1")
    tablews.addColumn("int", "NonNegative")
    tablews.addColumn("int", "Group")
    
    group = 0
    tablews.addRow(["Dtt1"  , 5.0, 0.0, 0, group]) 
    tablews.addRow(["Dtt1t" , 5.0, 0.0, 0, group])
    tablews.addRow(["Dtt2t" , 0.1, 1.0, 0, group])
    tablews.addRow(["Zero"  , 5.0, 0.0, 0, group])
    tablews.addRow(["Zerot" , 5.0, 0.0, 0, group])
    tablews.addRow(["Width" , 0.0, 0.1, 1, group])
    tablews.addRow(["Tcross", 0.0, 1.0, 1, group])
    
    group = 1
    tablews.addRow(["Beta0" , 0.50, 1.0, 0, group]) 
    tablews.addRow(["Beta1" , 0.05, 1.0, 0, group])
    tablews.addRow(["Beta0t", 0.50, 1.0, 0, group])
    tablews.addRow(["Beta1t", 0.05, 1.0, 0, group])
    
    group = 2
    tablews.addRow(["Alph0" , 0.05, 1.0, 0, group])
    tablews.addRow(["Alph1" , 0.02, 1.0, 0, group])
    tablews.addRow(["Alph0t", 0.10, 1.0, 0, group])
    tablews.addRow(["Alph1t", 0.05, 1.0, 0, group])
    
    group = 3
    tablews.addRow(["Sig0", 2.0, 1.0, 1, group])
    tablews.addRow(["Sig1", 2.0, 1.0, 1, group])
    tablews.addRow(["Sig2", 2.0, 1.0, 1, group])
    
    group = 4
    tablews.addRow(["Gam0", 2.0, 1.0, 0, group])
    tablews.addRow(["Gam1", 2.0, 1.0, 0, group])
    tablews.addRow(["Gam2", 2.0, 1.0, 0, group])

    return tablews

def breakParametersGroups(tablews):
    """ Break the parameter groups.  Such that each parameter/row has an individual group
    """
    numrows = tablews.rowCount()
    for ir in xrange(numrows):
        tablews.setCell(ir, 4, ir)

    return

def resetParametersGroups(tablews):
    """ Set the group number to original setup
    """
    numrows = tablews.rowCount()
    for ir in xrange(numrows):
        parname = tablews.cell(ir, 0)
        if parname in ["Dtt1", "Dtt1t", "Dtt2t", "Zero", "Zerot", "Width", "Tcross"]:
            group = 0
        elif parname in ["Beta0", "Beta1", "Beta0t", "Beta1t"]:
            group = 1
        elif parname in ["Alph0", "Alph1", "Alph0t", "Alph1t"]:
            group = 2
        elif parname in ["Sig0", "Sig1", "Sig2"]:
            group = 3
        else:
            group = 4
        tablews.setCell(ir, 4, group)
        return

def doStep4(numsteps):
    """ Use Monte Carlo random/drunken walk for solution
            FitRegion                   = '8500,49000',
            BackgroundParametersWorkspace   ='PG3_10808_Background_Parameters',
    """ 
    global datawsname 
    global instrparamwsname
    global braggpeakparamwsname 
    global startx, endx
    global backgroundorder, bkgdtablewsname

    outputwsname = '%s_MC_%s' % (datawsname, numsteps)
    outputwsname2 = '%s_MC_%s' % (datawsname, numprofsteps)
    
    print instrparamwsname    
    print braggpeakparamwsname
    print startx, endx

    instwsname = 'Bank1InstrumentParametersTable'

    # Set up the parameters to refine
    UpdatePeakParameterTableValue(
            InputWorkspace=instwsname,
            Column="FitOrTie",
            NewStringValue="tie")
    UpdatePeakParameterTableValue( 
            InputWorkspace=instwsname, 
            Column="FitOrTie",
            ParameterNames=["Dtt1", "Dtt1t", "Zerot", "Width"],
	    #ParameterNames=["Dtt1", "Dtt1t", "Zerot"],
            NewStringValue="fit")

    # Limit the range of MC 
    cwl = 0.533
    UpdatePeakParameterTableValue( 
            InputWorkspace=instwsname, 
            Column="Min",
            ParameterNames=["Width"],
            NewFloatValue=0.50) #cwl*0.25)
	    
    UpdatePeakParameterTableValue( 
            InputWorkspace=instwsname, 
            Column="Max",
            ParameterNames=["Width"],
            NewFloatValue=1.25) #cwl*4.0)
	    
    wsname = "MCSetupParameterTable"
    tablews = generateMCSetupTable(wsname)
    #breakParametersGroups(tablews)

    print "Fit range: %f , %f" % (startx, endx)
    LeBailFit(
            InputWorkspace                  = datawsname,
            OutputWorkspace                 = outputwsname,
            InputParameterWorkspace         = instwsname,
            OutputParameterWorkspace        = 'Bank1RefinedProfileTable',
            InputHKLWorkspace               = 'BraggPeakParameterTable1',
            OutputPeaksWorkspace            = 'BraggPeakRefinedParameterTable',
            FitRegion                       = '%f, %f' % (startx, endx),
            Function                        = 'MonteCarlo', 
            NumberMinimizeSteps             = numsteps, 
            BackgroundParametersWorkspace   = bkgdtablewsname,
            UseInputPeakHeights             = False, 
            PeakRadius                      ='8',
            Minimizer                       = 'Levenberg-Marquardt',
	    MCSetupWorkspace        = str(wsname),
            Damping                         = '5.0',
            RandomSeed                      = 0,
            AnnealingTemperature            = 100.0,
    	    DrunkenWalk                     = True)	    
    
    # Set up the parameters to refine
    
    instwsname = str('Bank1RefinedProfileTable')
    UpdatePeakParameterTableValue(
            InputWorkspace=instwsname,
            Column="FitOrTie",
            NewStringValue="tie")
    UpdatePeakParameterTableValue( 
            InputWorkspace=instwsname, 
            Column="FitOrTie",
            ParameterNames=["Alph0", "Alph0t", "Alph1", "Beta0", "Beta1", "Beta0t", "Beta1t", "Sig1", "Sig2"],
            NewStringValue="fit")
	    
    #breakParametersGroups(tablews)	    
    
    print "Fit range: %f , %f" % (startx, endx)
    LeBailFit(
            InputWorkspace                  = datawsname,
            OutputWorkspace                 = outputwsname2,
            InputParameterWorkspace         = instwsname,
            OutputParameterWorkspace        = 'Bank1RefinedProfileTable2',
            InputHKLWorkspace               = 'BraggPeakParameterTable1',
            OutputPeaksWorkspace            = 'BraggPeakParameterTable4',
            FitRegion                       = '%f, %f' % (startx, endx),
            Function                        = 'MonteCarlo', 
            NumberMinimizeSteps             = numprofsteps/10, 
            BackgroundParametersWorkspace   = bkgdtablewsname,
            UseInputPeakHeights             = False, 
            PeakRadius                      ='8',
            Minimizer                       = 'Levenberg-Marquardt',
	    MCSetupWorkspace        = str(wsname),
            Damping                         = '1.0',
            RandomSeed                      = 0,
            AnnealingTemperature            = 100.0,
    	    DrunkenWalk                     = True)
    return


def main(argv):
    """ Main
    """
    global numsteps
    if numsteps <= 0:
	    numsteps = 200
	    print "Using default number of steps 200"

    setupGlobals("/home/wzz/Projects/MantidTests/LeBailFit/Test2013B/Bank1/Calibration_Information.config")

    doStep4(numsteps)

    return

if __name__=="__main__":
    main([])