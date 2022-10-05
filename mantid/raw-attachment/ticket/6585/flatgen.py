# flatgen.py
# S.King
#
# Generates a Flat Cell correction file for LOQ or SANS2D Mantid SANS data reduction
# NB: this is different to a Flat Cell file generated for COLETTE data reduction because
#        the two programs handle the solid angle normalisation differently.
#
# THIS VERSION USES SetDetectorOffsets(bank, x, y, z, rot, radius, side) INSTEAD OF MoveInstrumentComponent
# BECAUSE THE LATTER DOES NOT ALLOW FOR THE FRONT DETECTOR ROT, RADIUS OR SIDE OFFSETS
#
# Make the reduction module available
#from SANSReduction import *
from ISISCommandInterface import *
#
# And need this to use getInstrument(), etc
from mantidsimple import *
#
# Pull in the external fortran algorithm
# IMPORTANT NOTE: This .pyd file must be located in a directory covered by the environment variable PATH or this script will crash!
import mantid_flatgen

def FlatGen(verbose,instr,datain,padding,format,flood,quiet,workto,wires,radmin,radmax,xcent,ycent,xpixel,ypixel,spos,rxoff,ryoff,rzoff,fxoff,fyoff,fzoff,froff,fqoff,fsoff):

    maxspectra = 73800

# Convert shifts/offsets to metres for MoveInstrumentComponent later
    spos = spos / 1000
# NB: SetDetectorOffsets uses mm not m so don't need the following conversions
#    rxoff = rxoff / 1000
#    ryoff = ryoff / 1000
#    rzoff = rzoff / 1000
#    fxoff = fxoff / 1000
#    fyoff = fyoff / 1000
#    fzoff = fzoff / 1000
# NB: froff is not currently implemented
#    froff = froff / 1000
#    fqoff = fqoff / 1000
#    fsoff = fsoff / 1000

    if (quiet != -1):
        sum_file = workto + 'MAN_' + str(flood) + '-' + str(quiet) + '_SUM_RAW.TXT'
        col_type_flat_file = workto + 'COL_FLAT_CELL_' + str(flood) + '-' + str(quiet) + '.TXT'
        flat_file = workto + 'MAN_FLAT_CELL_' + str(flood) + '-' + str(quiet) + '.TXT'
    else:
        sum_file = workto + 'MAN_' + str(flood) + '_SUM_RAW.TXT'
        col_type_flat_file = workto + 'COL_FLAT_CELL_' + str(flood) + '.TXT'
        flat_file = workto + 'MAN_FLAT_CELL_' + str(flood) + '.TXT'

    solid_angle_file = workto + 'MAN_' + str(flood) + '_SOLID_ANGLES.TXT'

    workspace0 = 'temporary_data'
    workspace1 = 'TOF_Flood'
    workspace2 = 'RawSum_Flood'
    workspace3 = 'TOF_Quiet'
    workspace4 = 'RawSum_Quiet'
    workspace5 = 'RawSum_FloodMinusQuiet'
    workspace6 = 'RawSumBySpectrum_Flood'
    workspace7 = 'RawSumBySpectrum_FloodMinusQuiet'
    workspace8 = 'COLETTE-type_Flat_Cell'
    workspace9 = 'SolidAnglesBySpectrum'
    workspace10 = 'MANTID-type_Flat_Cell'

    # Set instrument
    if instr == 'SANS2D':
        SANS2D()
        instr_code = 2
        if verbose == 1:
            print 'SANS2D data is expected'
    elif instr == 'LOQ':
        LOQ()
        instr_code = 1
        if verbose == 1:
            print 'LOQ data is expected'
    else:
        SANS2D()
        instr_code = 2
        print 'WARNING! The instrument specified does not make sense!  Will default to SANS2D'

    # Set data directory
    DataPath(datain)
    if verbose == 1:
        print 'Will look for data in',datain

    if format == '.raw':
        if verbose == 1:
            print 'RAW files are expected'
    elif format == '.nxs':
        if verbose == 1:
            print 'NXS files are expected'
    else:
        format = ".nxs"
        print 'WARNING! The file format specified does not make sense!  Will assume NXS'

    print ' '

# RAW =============================================================================================================================

    if format == '.raw':
        data_file = datain + instr + padding + str(flood) + format
        print 'Processing run',data_file
        print ' '

        LoadRaw(Filename=data_file,OutputWorkspace=workspace1)
        print '      sample position is at:',mtd[workspace1].getInstrument().getSample().getPos()
        if instr == 'LOQ':
            print '     main detector position:',mtd[workspace1].getInstrument().getComponentByName('main-detector-bank').getPos()
            print '      HAB detector position:',mtd[workspace1].getInstrument().getComponentByName('HAB').getPos()
        elif instr == 'SANS2D':
            print '    front detector position:',mtd[workspace1].getInstrument().getComponentByName('front-detector').getPos()
            print '     rear detector position:',mtd[workspace1].getInstrument().getComponentByName('rear-detector').getPos()

        print ' '
        print 'Applying following shifts:'
        if instr == 'LOQ':
            print '         to sample position: 0.0 0.0',spos
            print '  to main detector position:',rxoff,ryoff,rzoff
#            MoveInstrumentComponent(workspace1, 'main-detector-bank', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
            SetDetectorOffsets('main-detector-bank', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)
            print '   to HAB detector position:',fxoff,fyoff,fzoff
#            MoveInstrumentComponent(workspace1, 'HAB', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
            SetDetectorOffsets('HAB', fxoff, fyoff, fzoff, 0.0, 0.0, 0.0)

        elif instr == 'SANS2D':
            print '         to sample position: 0.0 0.0',spos
            print ' to front detector position:',fxoff,fyoff,fzoff
#            MoveInstrumentComponent(workspace1, 'front-detector', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
            SetDetectorOffsets('front', fxoff, fyoff, fzoff, froff, fqoff, fsoff)
            print '  to rear detector position:',rxoff,ryoff,rzoff
#            MoveInstrumentComponent(workspace1, 'rear-detector', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
            SetDetectorOffsets('rear', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)

#       Re-load file to force offsets to be applied
#        LoadRaw(Filename=data_file,OutputWorkspace=workspace1)
#        MoveInstrumentComponent(workspace1, 'some-sample-holder', X = 0.0, Y = 0.0, Z = spos, RelativePosition="1")

        print ' '
        print '      sample position is now:',mtd[workspace1].getInstrument().getSample().getPos()
        if instr == 'LOQ':
            print '     main detector position now:',mtd[workspace1].getInstrument().getComponentByName('main-detector-bank').getPos()
            print '      HAB detector position now:',mtd[workspace1].getInstrument().getComponentByName('HAB').getPos()
        elif instr == 'SANS2D':
            print '    front detector position now:',mtd[workspace1].getInstrument().getComponentByName('front-detector').getPos()
            print '     rear detector position now:',mtd[workspace1].getInstrument().getComponentByName('rear-detector').getPos()

        Integration(workspace1,workspace2)

        if (quiet != -1):
            data_file = datain + instr + padding + str(quiet) + format
            print ' '
            print 'Processing run',data_file
#           Apply position offsets/shifts to the quiet count run for good measure
            if instr == 'LOQ':
#                MoveInstrumentComponent(workspace1, 'main-detector-bank', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
                SetDetectorOffsets('main-detector-bank', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)
#                MoveInstrumentComponent(workspace1, 'HAB', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
                SetDetectorOffsets('HAB', fxoff, fyoff, fzoff, 0.0, 0.0, 0.0)
            elif instr == 'SANS2D':
#                MoveInstrumentComponent(workspace3, 'front-detector', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
                SetDetectorOffsets('front', fxoff, fyoff, fzoff, froff, fqoff, fsoff)
#                MoveInstrumentComponent(workspace3, 'rear-detector', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
                SetDetectorOffsets('rear', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)
# Tidy this up when SetDetectorOffsets is working properly
#            LoadRaw(Filename=data_file,OutputWorkspace=workspace3)
#            MoveInstrumentComponent(workspace3, 'some-sample-holder', X = 0.0, Y = 0.0, Z = spos, RelativePosition="1")

            Integration(workspace3,workspace4)
            Minus(workspace2,workspace4,workspace5)
            SaveRKH(workspace5,sum_file,0)
        else:
            SaveRKH(workspace2,sum_file,0)

        print ' '
        print 'Writing',sum_file

# NEXUS ===========================================================================================================================

    elif format == '.nxs':
        data_file = datain + instr + padding + str(flood) + format
        print 'Processing run',data_file
        print ' '

        LoadNexus(Filename=data_file,OutputWorkspace=workspace1)
        print '      sample position is at:',mtd[workspace1].getInstrument().getSample().getPos()
        if instr == 'LOQ':
            print '     main detector position:',mtd[workspace1].getInstrument().getComponentByName('main-detector-bank').getPos()
            print '      HAB detector position:',mtd[workspace1].getInstrument().getComponentByName('HAB').getPos()
        elif instr == 'SANS2D':
            print '    front detector position:',mtd[workspace1].getInstrument().getComponentByName('front-detector').getPos()
            print '     rear detector position:',mtd[workspace1].getInstrument().getComponentByName('rear-detector').getPos()

        print ' '
        print 'Applying following shifts:'
        if instr == 'LOQ':
            print '         to sample position: 0.0 0.0',spos
            print '  to main detector position:',rxoff,ryoff,rzoff
#            MoveInstrumentComponent(workspace1, 'main-detector-bank', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
            SetDetectorOffsets('main-detector-bank', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)
            print '   to HAB detector position:',fxoff,fyoff,fzoff
#            MoveInstrumentComponent(workspace1, 'HAB', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
            SetDetectorOffsets('HAB', fxoff, fyoff, fzoff, 0.0, 0.0, 0.0)

        elif instr == 'SANS2D':
            print '         to sample position: 0.0 0.0',spos
            print ' to front detector position:',fxoff,fyoff,fzoff
#            MoveInstrumentComponent(workspace1, 'front-detector', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
            SetDetectorOffsets('front', fxoff, fyoff, fzoff, froff, fqoff, fsoff)
            print '  to rear detector position:',rxoff,ryoff,rzoff
#            MoveInstrumentComponent(workspace1, 'rear-detector', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
            SetDetectorOffsets('rear', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)

#       Re-load file to force offsets to be applied
#        LoadNexus(Filename=data_file,OutputWorkspace=workspace1)
#        MoveInstrumentComponent(workspace1, 'some-sample-holder', X = 0.0, Y = 0.0, Z = spos, RelativePosition="1")

        print ' '
        print '      sample position is now:',mtd[workspace1].getInstrument().getSample().getPos()
        if instr == 'LOQ':
            print '     main detector position now:',mtd[workspace1].getInstrument().getComponentByName('main-detector-bank').getPos()
            print '      HAB detector position now:',mtd[workspace1].getInstrument().getComponentByName('HAB').getPos()
        elif instr == 'SANS2D':
            print '    front detector position now:',mtd[workspace1].getInstrument().getComponentByName('front-detector').getPos()
            print '     rear detector position now:',mtd[workspace1].getInstrument().getComponentByName('rear-detector').getPos()

        Integration(workspace1,workspace2)

        if (quiet != -1):
            data_file = datain + instr + padding + str(quiet) + format
            print ' '
            print 'Processing run',data_file
#           Apply position offsets/shifts to the quiet count run for good measure
            if instr == 'LOQ':
#                MoveInstrumentComponent(workspace1, 'main-detector-bank', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
                SetDetectorOffsets('main-detector-bank', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)
#                MoveInstrumentComponent(workspace1, 'HAB', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
                SetDetectorOffsets('HAB', fxoff, fyoff, fzoff, 0.0, 0.0, 0.0)
            elif instr == 'SANS2D':
#                MoveInstrumentComponent(workspace3, 'front-detector', X = fxoff, Y = fyoff, Z = fzoff, RelativePosition="1")
                SetDetectorOffsets('front', fxoff, fyoff, fzoff, froff, fqoff, fsoff)
#                MoveInstrumentComponent(workspace3, 'rear-detector', X = rxoff, Y = ryoff, Z = rzoff, RelativePosition="1")
                SetDetectorOffsets('rear', rxoff, ryoff, rzoff, 0.0, 0.0, 0.0)
# Tidy this up when SetDetectorOffsets is working properly
#            LoadNexus(Filename=data_file,OutputWorkspace=workspace3)
#            MoveInstrumentComponent(workspace3, 'some-sample-holder', X = 0.0, Y = 0.0, Z = spos, RelativePosition="1")

            Integration(workspace3,workspace4)
            Minus(workspace2,workspace4,workspace5)
            SaveRKH(workspace5,sum_file,0)
        else:
            SaveRKH(workspace2,sum_file,0)

        print ' '
        print 'Writing',sum_file

# IMPORTANT NOTE: sum_file contains the integrated number of counts per spectrum, summed over all TOF's. If a Quiet Count run was specified it is 
# the DIFFERENCE between the integral for the Flood Source run and the integral for the Quiet Count run. HOWEVER the corresponding Mantid 
# workspaces - RawSum_Flood, RawSum_Quiet or RawSum_FloodMinusQuiet - contain the first and last TOF's as the X data AND NOT the spectrum number!
#
# To replace the X data **in Mantid** with a spectral index we need to do one of two things, EITHER:
#
# 1) call upon a Mantid user algorithm (ie, not one distributed with Mantid), or
# 2) use the Transpose algorithm (which was created more recently!)
#
# =================================================================================================================================
# METHOD 1)
#
#    if (quiet != -1):
#        ConvertXToSpectrumNumber('RawSum_FloodMinusQuiet', 'RawSumBySpectrum_FloodMinusQuiet')
#    else:
#        ConvertXToSpectrumNumber('RawSum_Flood', 'RawSumBySpectrum_Flood')
#
# =================================================================================================================================
# Algorithm courtesy of M Gigg
# IMPORTANT NOTE: This algorithm must be present in C:\MantidInstall\plugins\PythonAlgs or this script will crash!
#
# from MantidFramework import *
# 
# class ConvertXToSpectrumNumber(PythonAlgorithm):
#
#     def PyInit(self):
#         self.declareWorkspaceProperty("InputWorkspace", "", Direction = Direction.Input)
#         self.declareWorkspaceProperty("OutputWorkspace", "", Direction = Direction.Output)
# 
#     def PyExec(self):
#         input_ws = self.getProperty("InputWorkspace")
# 
#         nhists = input_ws.getNumberHistograms()
#         nbins = 1
#         output_ws = WorkspaceFactory.createMatrixWorkspaceFromCopy(input_ws, NVectors = nhists, YLength = nbins, XLength = 1)
#         for i in range(nhists):
#             # Set the data in the new workspace
#             output_ws.dataX(i)[0] = i + 1
#             output_ws.dataY(i)[0] = input_ws.readY(i)[0]
#             output_ws.dataE(i)[0] = input_ws.readE(i)[0]
# 
#         self.setProperty("OutputWorkspace", output_ws)
# 
# mtd.registerPyAlgorithm(ConvertXToSpectrumNumber())
# =================================================================================================================================
# METHOD 2)

    if (quiet != -1):
        Transpose(workspace5,workspace7)
    else:
        Transpose(workspace2,workspace6)

# =================================================================================================================================

# Then extract the spectrum number values, the corresponding integrals and the number of bins from the converted workspaces...
    if (quiet != -1):
        RawSumBySpectrum_Workspace = mtd[workspace7]
    else:
        RawSumBySpectrum_Workspace = mtd[workspace6]
    
    xdata = list(RawSumBySpectrum_Workspace.readX(0))
    ndata = len(xdata)
    ydata = list(RawSumBySpectrum_Workspace.readY(0))
    edata = list(RawSumBySpectrum_Workspace.readE(0))

# A small complication is that string and array lengths passed from Python to Fortran must match EXACTLY. Because LOQ and SANS2D have wildy different
# numbers of spectra (normally 17792 and 73736, respectively) it is not possible to dimension arrays in the Fortran subroutine to suit one case and expect
# Python to stillbe happy in the other. Thus it is necessary to either pad out a smaller array, or have two seperate Fortran routines doing the same thing.
# Here we shall pad (with thanks to W S Howells!)...

# An Aside... Yes, we could have combined the previous two operations in:
# RawSumBySpectrum_Workspace = ConvertXToSpectrum('RawSum_...', 'RawSumBySpectrum_...').workspace()

    xarray = PadArray(xdata,maxspectra)
    yarray = PadArray(ydata,maxspectra)
    earray = PadArray(edata,maxspectra)

# ...and pass the data to a wrapped version of RKH's Genie-II function routine FLATGEN to do whatever it does to generate 
# a COLETTE-type Flat Cell file. The wrapping has been achieved with the F2Py utility within NumPy and it creates a Python .pyd file.
#
# IMPORTANT NOTE: The .pyd file must be located in a directory covered by the environment variable PATH (eg, drive:/Python25 or drive/Python25/scripts)
# or this script will crash!
#
    print ' '
    print 'Passing', ndata, 'spectra to Mantid_Flatgen.Flatgen...'

    retcode,xout,yout,eout,totcnt,navgd,avgds,avgde = mantid_flatgen.flatgen(instr_code,wires,radmin,radmax,xcent,ycent,xpixel,ypixel,ndata,xarray,yarray,earray)

    print ' '
    print 'Retcode is', retcode
    print 'See flatgenlog.txt for details'

    print ' '
    print 'total counts (all spectra) was', "%.3e" % totcnt
    print ' '
    print navgd, 'spectra were averaged; result was', "%.3e" % avgds, '+/-', "%.3e" % avgde
    
    print ' '
    print 'Creating workspace...'
#        xout/yout/eout are returned as float32 numpy.ndarray variables but CreateWorkspace requires list arguments
#        CreateWorkspace creates one spectrum with all spectra numbers on its x-axis...
    CreateWorkspace(workspace0,list(xout),list(yout),list(eout),NSpec=1)
#        ...so use Transpose to create many spectra with the spectra axis copied from the original x-axis...
    Transpose(workspace0,workspace0)

#        ...and then remove the trailing zeroes from the array padding
#        NB: Cropping on the X value (rather than the index) does not currently (07/12/10) work properly when the X data is not a continuously increasing data set
    CropWorkspace(workspace0,workspace8,StartWorkspaceIndex=0,EndWorkspaceIndex=ndata-1)

    print ' '
    print 'Writing COLETTE-type flat cell file:'
    print col_type_flat_file
    SaveRKH(workspace8,col_type_flat_file,0)

#        For Mantid SANS (SANS2D or LOQ) reduction ONLY we now need to 'normalise' the data by the solid angle for each pixel
#        SolidAngle needs to know where it can get the detector information; best place is in a .raw or .nxs file!
    SolidAngle(workspace1,workspace9,StartWorkspaceIndex=0,EndWorkspaceIndex=ndata-1)
    SaveRKH(workspace9,solid_angle_file,0)

    print ' '
    print 'Dividing by solid angle...'
    mtd.deleteWorkspace(workspace0)
    Divide(workspace8,workspace9,workspace0)
    
    print ' '
    print 'Cleaning up workspace...'
#        Need to tidy up the end of the workspace because 0's will have become infinity!
    ReplaceSpecialValues(workspace0,workspace0,InfinityValue=0.0)
#    SaveRKH(workspace0,workto+'MAN_Unclean_Flat_Cell.txt',0)

#        But also what were -1's on return from mantid_flatgen.flatgen have become large negative numbers so need to reset them
#        No easy way to do this within Mantid (because data is in a workspace not an array or list), so will call another external Fortran routine
#        So first package the data...
    Transpose(workspace0,workspace0)
    xdata = list(mtd[workspace0].readX(0))
    ndata = len(xdata)
    ydata = list(mtd[workspace0].readY(0))
    edata = list(mtd[workspace0].readE(0))
    xarray = PadArray(xdata,maxspectra)
    yarray = PadArray(ydata,maxspectra)
    earray = PadArray(edata,maxspectra)

    print ' '
    print 'Passing', ndata, 'spectra to Mantid_Flatgen.Cleanup...'
#        ...then feed it to the external subroutine...
    retcode,xout,yout,eout = mantid_flatgen.cleanup(instr_code,wires,ndata,xarray,yarray,earray)

    print ' '
    print 'Retcode is', retcode
    print 'See flatgenlog.txt for details'

#        ...then re-create a new Mantid workspace...
    print ' '
    print 'Creating workspace...'
    mtd.deleteWorkspace(workspace0)
    CreateWorkspace(workspace0,list(xout),list(yout),list(eout),NSpec=1)
    Transpose(workspace0,workspace0)
    CropWorkspace(workspace0,workspace10,StartWorkspaceIndex=0,EndWorkspaceIndex=ndata-1)

#        ...and write it out!
    print ' '
    print 'Writing Mantid-type flat cell file:'
    print flat_file
    SaveRKH(workspace10,flat_file,0)

    print ' '
    print 'Done'




def PadArray(inarray,nfixed):
    npt=len(inarray)
    padding = nfixed-npt
    outarray=[]
    outarray.extend(inarray)
    outarray +=[0]*padding
    return outarray



