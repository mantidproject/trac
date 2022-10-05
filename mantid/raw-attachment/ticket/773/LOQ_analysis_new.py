import datetime
#LOQ data analysis script
#path = "C:/MantidInstall/"
#path = "C:/Mantid/Test/"
path="C:/Documents and Settings/wmx35332/Mantid/Test/"
# this makes a list for a rectangular block (wide x high) from pixel startID [with (1,1) at bottom left in usual LOQ sense
# though may need to change for SANS2d ??? ] for square array dim x dim
def detBlock(startID,wide,high,dim=128):
        output = ""
	# no idea why this says zero here rather than one ! - but it works
        for j in range(0,high):
                for i in range(0,wide):
                        output += str(startID+i+(dim*j))+","
        output = output.rstrip(",")
        return output
#
#######################
print datetime.datetime.now()
for x in range(0,1):
        # Call the LOQScriptInput algorithm to get the input data and parameters
        #input = LOQScriptInputDialog("48098","48094","48130","48127","48128",path+"Data/DIRECT.041","38","419","2.2","10.0","-0.035","0.008","0.28","0.002","324.95","328.02")
        input = LOQScriptInput("48098","48094","48130","48127","48128",path+"Data/DIRECT.041","38","419","2.2","10.0","-0.035","0.008","0.28","0.002","324.95","328.02")
        #,path+"Data/LOQ sans configuration/DIRECT.041")
        data_file = path + "Data/LOQ" + input.getPropertyValue("SampleWorkspace") + ".raw"
        empty_file = path + "Data/LOQ" + input.getPropertyValue("EmptyCanWorkspace") + ".raw"
        trans_sample_file = path + "Data/LOQ" + input.getPropertyValue("TransmissionSampleWorkspace") + ".raw"
        trans_direct_file = path + "Data/LOQ" + input.getPropertyValue("TransmissionDirectWorkspace") + ".raw"
        trans_empty_file = path + "Data/LOQ" + input.getPropertyValue("TransmissionEmptyCanWorkspace") + ".raw"
        min_radius = float(input.getPropertyValue("RadiusMin"))
        max_radius = float(input.getPropertyValue("RadiusMax"))
        wav1 = float(input.getPropertyValue("WavelengthMin"))
        wav2 = float(input.getPropertyValue("WavelengthMax"))
        dwav = input.getPropertyValue("WavelengthDelta")
        q1 = input.getPropertyValue("QMin")
        q2 = input.getPropertyValue("Q_max")
        dq = input.getPropertyValue("Q_delta")
        xshift=str((317.5-float(input.getPropertyValue("BeamCentreX")))/1000.0)
        yshift=str((317.5-float(input.getPropertyValue("BeamCentreY")))/1000.0)
        direct_beam_file = input.getPropertyValue("EfficiencyCorrectionFile")

        outputWS = "Small_Angle"

        #######################
        #Step 1 - Load the data file 
        LoadDataAlg = LoadRaw(data_file,OutputWorkspace="Monitor",SpectrumMin="2",SpectrumMax="2")
        #data_file = LoadDataAlg.getPropertyValue("Filename")
        #Load the small angle bank
        # whole det is 3 to 16386, but skip first and last two rows is 130 to 16130, note the crop on flat_cell needs these numbers
        firstsmall=130
        lastsmall=16130
        LoadRaw(Filename = data_file, OutputWorkspace=outputWS,SpectrumMin=str(firstsmall),SpectrumMax=str(lastsmall))
        #Load the high angle bank
        #LoadRaw(Filename = data_file, OutputWorkspace="High_Angle",spectrummin="16386",spectrummax="17792")

        #######################
        #Step 1.2 - Correct the monitor spectrum for flat background and remove prompt spike
        # Interpolation is just linear for now
        RemoveBins("Monitor","Monitor","19900","20500",Interpolation="Linear")
        FlatBackground("Monitor","Monitor","0","31000","39000")

        #######################
        #Step 1.3 - Mask out unwanted detetctors
        # XML description of a cylinder containing detectors to remove
        inner = "<infinite-cylinder id='inner'> "
        inner +=	"<centre x='0.0' y='0.0' z='0.0' /> " 
        inner +=	"<axis x='0.0' y='0.0' z='1' /> "
        inner +=	"<radius val='"+str(min_radius/1000.0)+"' /> "
        inner +=	"</infinite-cylinder> "
        inner +=	"<algebra val='inner' /> "

        # Remove the beam stop
        MaskDetectorsInShape(outputWS,inner)

        outer = "<infinite-cylinder id='outer'> "
        outer +=	"<centre x='0.0' y='0.0' z='0.0' /> " 
        outer +=	"<axis x='0.0' y='0.0' z='1' /> "
        outer +=	"<radius val='"+str(max_radius/1000.0)+"' /> "
        outer +=	"</infinite-cylinder> "
        # The hash in front of the name says that we want to keep everything inside the cylinder
        outer +=	"<algebra val='#outer' /> "

        # Remove the corners
        MaskDetectorsInShape(outputWS,outer)

        # mask right hand column
        MaskDetectors(outputWS,DetectorList=detBlock(128+2,1,128))	

        #######################
        #Step 1.1 - try move detector for beam centre (324.95, 328.02),
        #This step has to happen after the detector masking
        #RelativePosition="0" is a logical variable, which means an "absolute shift"
        # the detector centr is at X=Y=0 so does relative or absolute matter ?
        MoveInstrumentComponent(outputWS,"main-detector-bank",X=xshift,Y=yshift,RelativePosition="1")

        #######################
        #Step 2 - Convert all of the files to wavelength and rebin
        # ConvertUnits does have a rebin option, but it's crude. In particular it rebins on linear scale.
        wavbin=str(wav1)+","+str(dwav)+","+str(wav2)
        wavname="_"+str(int(wav1))+"_"+str(int(wav2))
        #
        ConvertUnits("Monitor","Monitor","Wavelength")
        Rebin("Monitor","Monitor",wavbin)
        ConvertUnits(outputWS,outputWS,"Wavelength")
        Rebin(outputWS,outputWS,wavbin)
        #ConvertUnits("High_Angle","High_Angle","Wavelength")
        #Rebin("High_Angle","High_Angle",wavbin)

        # FROM NOW ON JUST LOOKING AT MAIN DETECTOR DATA.....

        #######################
        #step 2.5 remove unwanted Wavelength bins
        #Remove non edge bins and linear interpolate #373
        #RemoveBins("High_Angle","High_Angle","3.00","3.50",Interpolation="Linear")
        #Future Missing - add cubic interpolation

        #######################
        #Step 3 - Flat cell correction

        #OPTION 1
        #calculate from raw flood source file
        #maybe later!

        #OPTION 2
        #LoadRKH with scalar value for wavelength ranges
        #data/flat(wavelength)
        #LoadRKH(path+"Data/LOQ sans configuration/FLAT_CELL.061","flat","SpectraNumber")
        #CropWorkspace("flat","flat",StartSpectrum=str(firstsmall),EndSpectrum=str(lastsmall))
        #optional correct for diffrernt detector positions
        #SolidAngle("flat","flatsolidangle")
        #SolidAngle(outputWS,"solidangle")
        #Divide("flatsolidangle","solidangle","SAcorrection")
        #Divide("flat","SAcorrection","flat")
        #RETRY
        #Divide(outputWS,"flat",outputWS)

        #OPTION 3
        #Correction using instrument geometry
        #SolidAngle(outputWS,"solidangle")
        #Divide(outputWS,"solidangle","Small_Angle corrected by solidangle")

        #######################
        #Step 4 - Correct by incident beam monitor
        # At this point need to fork off workspace name to keep a workspace containing raw counts
        outputWS_cor = outputWS + "_tmp"
        Divide(outputWS,"Monitor",outputWS_cor)
        mantid.deleteWorkspace("Monitor")

        #######################
        #Step 6 - Correct by transmission
        # Load the run with sample
        #LoadRawDialog(path+"Data/LOQ48130.raw","sample")
        LoadRaw(Filename=trans_sample_file,OutputWorkspace="sample")
        # Change the instrument definition to the correct one
        LoadInstrument("sample",path+"Instrument/LOQ_trans_Definition.xml")
        # Need to remove prompt spike and, later, flat background
        RemoveBins("sample","sample","19900","20500",Interpolation="Linear")
        FlatBackground("sample","sample","1,2","31000","39000")
        ConvertUnits("sample","sample","Wavelength")
        Rebin("sample","sample",wavbin)
        # Now load and convert the direct run
        #LoadRawDialog(path+"Data/LOQ48127.raw","direct")
        LoadRaw(Filename=trans_direct_file,OutputWorkspace="direct")
        LoadInstrument("direct",path+"Instrument/LOQ_trans_Definition.xml")
        RemoveBins("direct","direct","19900","20500",Interpolation="Linear")
        FlatBackground("direct","direct","1,2","31000","39000")
        ConvertUnits("direct","direct","Wavelength")
        Rebin("direct","direct",wavbin)

        CalculateTransmission("sample","direct","transmission")
        mantid.deleteWorkspace("sample")
        mantid.deleteWorkspace("direct")

        # Now do the correction
        Divide(outputWS_cor,"transmission",outputWS_cor)
        #mantid.deleteWorkspace("transmission")

        #######################
        #Step 7 - Correct for efficiency
        CorrectToFile(outputWS_cor,direct_beam_file,outputWS_cor,"Wavelength","Divide")

        #######################
        #Step 8 - Rescale(detector)
        # Enter the rescale value here
        rescale = 1.508*100.0

        #######################
        #Step 10 - Correct for sample/Can volume
        # Could easily move this to be done after the sample-can operation
        # Enter the value here
        thickness = 1.0
        area = 3.1414956*8*8/4

        correction = rescale/(thickness*area)

        CreateSingleValuedWorkspace("scalar",str(correction),"0.0")
        Multiply(outputWS_cor,"scalar",outputWS_cor)
        mantid.deleteWorkspace("scalar")

        #######################
        #Step 11 - Convert to Q
        #Convert units to Q (MomentumTransfer)
        ConvertUnits(outputWS_cor,outputWS_cor,"MomentumTransfer")
        ConvertUnits(outputWS,outputWS,"MomentumTransfer")

        #Need to mark the workspace as a distribution at this point to get next rebin right
        ws = mantid.getMatrixWorkspace(outputWS_cor)
        ws.isDistribution(True)

        # Calculate the solid angle corrections
        SolidAngle(outputWS_cor,"solidangle")

        #rebin to desired Q bins
        q_bins = q1+","+dq+","+q2
        Rebin(outputWS,outputWS,q_bins)
        Rebin(outputWS_cor,outputWS_cor,q_bins)
        RebinPreserveValue("solidangle","solidangle",q_bins)

        #Sum all spectra
        SumSpectra(outputWS,outputWS)
        SumSpectra(outputWS_cor,outputWS_cor)
        SumSpectra("solidangle","solidangle")

        #######################
        #correct for solidangle
        Divide(outputWS_cor,"solidangle",outputWS_cor)
        #mantid.deleteWorkspace("solidangle")

        #######################
        # Now put back the fractional error from the raw count workspace into the result
        PoissonErrors(outputWS_cor,outputWS,outputWS+wavname)
        mantid.deleteWorkspace(outputWS_cor)
        mantid.deleteWorkspace(outputWS)

        #######################
        #step 12 - Cross section (remove can scatering)
        #Perform steps 1-11 for the sample and can
        # sample-can

        #######################
        #step 12 - Save 1D data
        # this writes to the /bin directory - why ?
        SaveRKH(outputWS+wavname,Filename=outputWS+wavname+".Q",FirstColumnValue="MomentumTransfer")
	# print x
print datetime.datetime.now()
