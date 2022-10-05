from mantid import config, logger, mtd
# this section not needed - ws already there when gui is opened
instr = 'IRIS'
ana = 'graphite'
refl = '002'
mt_ws = '_empty'+instr
idf_dir = config['instrumentDefinition.directory']
idf = idf_dir + instr + '_Definition.xml'
LoadEmptyInstrument(Filename=idf, OutputWorkspace=mt_ws)
ipf = idf_dir + instr + '_' + ana + '_' + refl + '_Parameters.xml'
LoadParameterFile(Workspace=mt_ws, Filename=ipf)
# except for mt_ws
instrument = mtd[mt_ws].getInstrument()
analyser = instrument.getStringParameter('analyser')[0]
resolution = instrument.getComponentByName(analyser).getNumberParameter('resolution')[0]
x = [-6*resolution, -5*resolution, -2*resolution, 0.0, 2*resolution]
# BgdMin, BgdMax, PeakMin, PeakZero, PeakMax
y = [1,2,3,4]
e = [0,0,0,0]
CreateWorkspace(OutputWorkspace='energy', DataX=x, DataY=y, DataE=e,
    Nspec=1, UnitX='DeltaE')
ConvertToHistogram(InputWorkspace='energy', OutputWorkspace='energy')
LoadInstrument(Workspace='energy', InstrumentName=instr)
LoadParameterFile(Workspace='energy', Filename=ipf)
efixed = mtd['energy'].getInstrument().getNumberParameter('efixed-val')[0]
print 'efixed = '+str(efixed)
# Reset det IDs
spectrum = mtd['energy'].getSpectrum(0)
spectrum.setSpectrumNo(3)
spectrum.clearDetectorIDs()
spectrum.addDetectorID(3)
ConvertUnits(InputWorkspace='energy', OutputWorkspace='tof', Target='TOF',
    EMode='Indirect', EFixed=efixed)
tof = mtd['tof'].readX(0)
# energy increasing on converting becomes time decreasing
# so the parameter order is reversed
# these are the default values
PeakMin = tof[0]
PeakMax = tof[2]
BgdMin = tof[3]
BgdMax = tof[4]
