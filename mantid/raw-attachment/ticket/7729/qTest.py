ws  = Load("irs26173_graphite002_red")
spec = ConvertSpectrumAxis(InputWorkspace=ws,Target="ElasticQ",EMode="Indirect")
ax = spec.getAxis(1)

for row in range(0,spec.getNumberHistograms()):
	print ax.getValue(row)