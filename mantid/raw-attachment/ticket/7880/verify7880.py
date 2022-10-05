# This script is to be executed inside MantidPlot

def setupProfileWS():
    """ Main
    """
    import math
    
    parammap = []
    parammap.append(["BANK", 1, "tie"])
    parammap.append(["Dtt1", 16370.650, "tie"])
    parammap.append(["Dtt2", 0.10, "tie"])
    parammap.append(["Zero", 0.0, "tie"])

    # Use peak shape parameters from Argonne Silicon example
    parammap.append(["Alph0", 1.0, "tie"])
    parammap.append(["Alph1", 0.0, "tie"])
    parammap.append(["Beta0", 0.109036, "tie"])
    parammap.append(["Beta1", 0.009834, "tie"])

    parammap.append(["Sig2",  math.sqrt(91.127), "tie"])
    parammap.append(["Sig1",  math.sqrt(1119.230), "tie"])
    parammap.append(["Sig0",  math.sqrt(0.0), "tie"])

    parammap.append(["Gam0", 0.0, "tie"])
    parammap.append(["Gam1", 0.0, "tie"])
    parammap.append(["Gam2", 0.0, "tie"])

    parammap.append(["LatticeConstant", 5.431363, "tie"])

    CreateEmptyTableWorkspace(OutputWorkspace="Vulcan_Bank1")
    pws = mtd["Vulcan_Bank1"]
    
    pws.addColumn("str", "Name")
    pws.addColumn("double", "Value")
    pws.addColumn("str", "FitOrTie")
    
    for item in parammap:
        pws.addRow(item)

    return


def main():
    """ Main
    """
    LoadAscii(Filename="VULCAN_22946_NOM.dat", OutputWorkspace="VULCAN_22946", Unit="TOF")
	 
    # Generate list of reflections
    CreateLeBailFitInput(FullprofParameterFile=r'dummy.irf', 
            Bank='1', LatticeConstant='4.0010000000000003', InstrumentParameterWorkspace='I',
            GenerateBraggReflections='1',BraggPeakParameterWorkspace='BraggPeaks')
    DeleteWorkspace(Workspace="I")
    
    setupProfileWS()

    LoadNexusProcessed(Filename="v22946_bkgd_polynomial.nxs", OutputWorkspace="VUL_22946_BackgroundParameters")

    # For debug purpose
    ExaminePowderDiffProfile(InputWorkspace="VULCAN_22946", LoadData=False,
            StartX = 7000., EndX = 29100., 
            ProfileWorkspace = "Vulcan_Bank1", BraggPeakWorkspace = "BraggPeaks", GenerateInformationWS = False,
            BackgroundType = "Polynomial", BackgroundParameterWorkspace = "VUL_22946_BackgroundParameters", ProcessBackground = False, 
            BackgroundWorkspace = "V22946_Background", OutputWorkspace = "VUL_22946_Cal")

    # Load data


if __name__ == "__main__":
    main()
