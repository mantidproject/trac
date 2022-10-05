# random choice of run. Temp_Sample has 82 entries according to the dialog box ws=mtd["hifi00029177"]
ws=mtd["hifi00025091"]
r= ws.getRun()

time_array = r.getLogData("Temp_Sample").times

value_array = r.getLogData("Temp_Sample").value

# print time_array
# print value_array
print "log point 0  ", time_array[0]
print "log point 2  ", time_array[2]
print "log point 3  ", time_array[3]
print "log point 50 ", time_array[50]
print "start time   ", r.getProperty("run_start").value

#print dir(time_array[1])
#print time_array[1].year()

if (time_array[1] > r.getProperty("run_start").value) :
	print "point 1 is in the run"
else:
	print "point 1 before run starts"

if (time_array[50] > r.getProperty("run_start").value) :
	print "point 50 is in the run"
else:
	print "point 50 before run starts"

if (time_array[50] > time_array[1]) :
	print "time going forwards"
else:
	print "times going backwards!"

if (time_array[1] > time_array[50]) :
	print "time going backwards"
else:
	print "times going forwards!"


