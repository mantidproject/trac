# Script is used to convert the Mantid binned VULCAN data to V-DRIVE binned GSAS data 
# in order to compare the final result
#
# Version   2.0
# Date      2014.08.14


calibrationfilename = "vulcan_foc_all_2bank_11p.cal"
characterfilename   =  "VULCAN_Characterization_2Banks_v2.txt"
#logbinfilename      = "vdrive_log_bin.dat"

def reduceVulcanRun(runnumber):
    """ Reduce a powder diffraction run with proper 
    """ 
    SNSPowderReduction( 
            Instrument  = "VULCAN",
            RunNumber   = runnumber,
            Extension   = "_event.nxs",
            PreserveEvents  = True,
            CalibrationFile = calibrationfilename,
            CharacterizationRunsFile = characterfilename,
            Binning = "-0.001",
            SaveAS  = "",
            OutputDirectory = "/home/wzz/Projects/MantidTests/Vulcan/Reduction/Generate_GSAS/temp", 
            NormalizeByCurrent = False,
            FilterBadPulses=0,
            CompressTOFTolerance = 0.)

    newrun = ConvertUnits(InputWorkspace="VULCAN_%d"%(runnumber), OutputWorkspace="VULCAN_%d_SNSReduc"%(runnumber), 
            Target="TOF", EMode="Elastic", AlignBins=False)
	    
    return newrun 



def getRunNumber(nexusfilename):
    """ Run number
    """
    filename = nexusfilename.split(".")[0]
    terms = filename.split("/")
    for t in terms:
        if t.count("IPTS") == 1:
            ipts = int(t.split("-")[1])
        elif t.count("event") == 1:
            run = int(t.split("_")[1])
    # ENDFOR

    return (ipts, run)


def main(nexusfilename, refxfilename):
    """ main
    """
    ipts, runnumber = getRunNumber(nexusfilename)

    vulcanws = reduceVulcanRun(runnumber)

    outfilename = "/tmp/mtd%s.gda" % (str(runnumber))
    SaveVulcanGSS(InputWorkspace=vulcanws, BinFilename=refxfilename, 
            OutputWorkspace="Proto2Bank", GSSFilename=outfilename, 
	    IPTS = ipts, GSSParmFilename="xxx.iparm")

    mtdgss = LoadGSS(Filename="/tmp/mtd%s.gda" % (str(runnumber)))
    vdrgss = LoadGSS(Filename="26299.gda")
    Minus(LHSWorkspace=vdrgss, RHSWorkspace=mtdgss, OutputWorkspace="diff_mv", AllowDifferentNumberSpectra=True)

    return


if __name__ == "__main__":
    nexusfilename = "/SNS/VULCAN/IPTS-9846/0/26299/NeXus/VULCAN_26299_event.nxs"
    vdrivebinfname = "vdrive_log_bin.dat"
    main(nexusfilename, vdrivebinfname)
