# This file was created with the old SofQW algorithm
Load(Filename='irs53664_graphite002_sqw.nxs', OutputWorkspace='irs53664_graphite002_sqw')
# Do something to show how the incorrect detector table breaks analysis
ConvertUnits(InputWorkspace='irs53664_graphite002_sqw', OutputWorkspace='original_sqw_conversion', Target='Wavelength', EMode='Indirect', EFixed=1.845)

# This is the file the original Sqw was created from
Load(Filename='irs53664_graphite002_red.nxs', OutputWorkspace='irs53664_graphite002_red')
# Recreate the Sqw with the fixed algorithm
SofQW(InputWorkspace='irs53664_graphite002_red', OutputWorkspace='new_sqw', QAxisBinning='0.4,0.1,1.8', EMode='Indirect', EFixed=1.845)
# Do the same check
ConvertUnits(InputWorkspace='new_sqw', OutputWorkspace='new_sqw_conversion', Target='Wavelength', EMode='Indirect', EFixed=1.845)