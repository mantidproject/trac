instrument = "IRIS"
analyser = "graphite"
reflection = "002"

#using water
formula = "H2-O"
density = 0.1
thickness = 0.1

IndirectTransmission(Instrument=instrument, Analyser=analyser, Reflection=reflection,
								ChemicalFormula=formula, NumberDensity=density, Thickness=thickness, OutputWorkspace='IRIS_graphite_002_Transmission')