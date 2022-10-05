from mantid.kernel import DateAndTime
mtd.importAll()
ws = WISH00026110

def meanWithinRange(filterstart, filterend, logname):
	run = ws.getRun()
	temperature = run.getLogData(logname)
	times = numpy.array(temperature.times)
	values = numpy.array(temperature.value)
	mask = (filterstart < times) & (times < filterend) # Get times between filter start and end.
	return values[mask].mean() # Use mask to get the mean value in this time interval.

filterstart = DateAndTime("2013-10-30T10:03+00:00") # Example filter start
filterend = DateAndTime("2013-10-30T11:14+00:00") # Example filter end
logname = 'Sample_Temp'
print meanWithinRange(filterstart, filterend, logname)


