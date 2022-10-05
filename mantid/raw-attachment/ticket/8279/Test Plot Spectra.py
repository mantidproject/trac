dataX = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
dataY = [1,2,3,4,5,6,7,8,9,10,11,12]
dataE = [1,2,3,4,5,6,7,8,9,10,11,12]

smallDataX = [1,2,3,4]
smallDataY = [1,2,3]
smallDataE = [1,2,3]

even = CreateWorkspace(DataX=dataX, DataY=dataY, DataE=dataE, NSpec=4,UnitX="Wavelength")
odd = CreateWorkspace(DataX=dataX, DataY=dataY, DataE=dataE, NSpec=4,UnitX="Wavelength")
consecutive = CreateWorkspace(DataX=dataX, DataY=dataY, DataE=dataE, NSpec=4,UnitX="Wavelength")

singleEven = CreateWorkspace(DataX=smallDataX, DataY=smallDataY, DataE=smallDataE, NSpec=1,UnitX="Wavelength")
singleOdd = CreateWorkspace(DataX=smallDataX, DataY=smallDataY, DataE=smallDataE, NSpec=1,UnitX="Wavelength")

even.getSpectrum(0).setSpectrumNo(0)
even.getSpectrum(1).setSpectrumNo(2)
even.getSpectrum(2).setSpectrumNo(4)
even.getSpectrum(3).setSpectrumNo(6)

odd.getSpectrum(0).setSpectrumNo(1)
odd.getSpectrum(1).setSpectrumNo(3)
odd.getSpectrum(2).setSpectrumNo(5)
odd.getSpectrum(3).setSpectrumNo(7)

consecutive.getSpectrum(0).setSpectrumNo(2)
consecutive.getSpectrum(1).setSpectrumNo(3)
consecutive.getSpectrum(2).setSpectrumNo(4)
consecutive.getSpectrum(3).setSpectrumNo(5)

singleEven.getSpectrum(0).setSpectrumNo(4)
singleOdd.getSpectrum(0).setSpectrumNo(5)