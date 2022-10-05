from mantid import *
import sys
def run_comparison(input_ws_name, output_ws_name, relative_time_shift =0.0, absolute_time_shift="", log = False):
    # Create a duplicate
    duplicate = CloneWorkspace(InputWorkspace = input_ws_name)
    
    # Run ChangeTimeZero
    ChangeTimeZero(InputWorkspace = input_ws_name, OutputWorkspace = output_ws_name, 
                           RelativeTimeOffset= relative_time_shift , AbsoluteTimeOffset = absolute_time_shift)
    
    # Compare the sample logs
    time_shift = 0.0
    if (absolute_time_shift != ""):
        proton_charge_times = duplicate.getRun().getProperty("proton_charge").times
        if len(proton_charge_times) == 0:
            sys.exit("When using absolute times you need a proton charge log")
        time_shift = time_duration.total_nanoseconds(proton_charge_times[0]- DateAndTime(absolute_time_shift))
    else:
        time_shift = relative_time_shift

    compare_logs(output_ws_name, duplicate, time_shift, log)
    
    # Compare the neutrons for event workspaces
    if isinstance(duplicate, IEventWorkspace):
        compare_neutrons(output_ws_name, duplicate, time_shift)

def compare_logs(output_ws_name, duplicate, time_shift, log):
    # Iterate over all TimeSeries properties
    ws = mtd[output_ws_name]
    run = ws.getRun()
    props = run.getProperties()
    props_duplicate = duplicate.getRun().getProperties()
    
    size = len(props)
    size_duplicate = len(props_duplicate)
    assert(size == size_duplicate)
   
    for prop in props:
        prop_2 = []
        for prop_duplicate in props_duplicate:
            prop_2 = []
            if prop_duplicate.name == prop.name:
                prop_2 = prop_duplicate
                break
                
        if isinstance(prop, FloatTimeSeriesProperty) or isinstance(prop, BoolTimeSeriesProperty) or isinstance(prop, StringTimeSeriesProperty):
            # Need to find the property in duplicate ws
            times_1 = prop.times
            times_2 = prop_2.times
            assert(len(times_1) == len(times_2))
            compare_time_series_log(times_1, times_2, time_shift, log)
        elif isinstance(prop, StringPropertyWithValue) and isinstance(prop_2, StringPropertyWithValue):
            val_1 = 0.0
            val_2 = 0.0
            try:
                val_1 = DateAndTime(prop.value)
                val_2 = DateAndTime(prop_2.value)
                compare_string_value(val_1, val_2, time_shift, log)
            except ValueError:
                pass

def compare_time_series_log(times_1, times_2, expected_time_shift, log):
    for i in range(0,len(times_1)):
        if time_duration.total_nanoseconds(times_1[i] - times_2[i])/1e9 != expected_time_shift:
            sys.exit("The time difference for a time series property does not seem correct.")
            
        if log:
            print "| Orig: " + str(times_1[i]) + "  |  Shift: " + str(times_2[i]) + "  |  Diff[s]: "  + str(time_duration.total_nanoseconds(times_1[i] - times_2[i])/1e9) + "  |" 


def compare_string_value(val1, val2, expected_time_shift, log):
    if time_duration.total_nanoseconds(val1 - val2)/1e9 != expected_time_shift:
        sys.exit("The time difference for a string property does not seem correct.")
    if log:
        print "| ValOrig: " + str(val1) + "  |  ValShift: " + str(val2) + "  |  Diff[s]: "  + str(time_duration.total_nanoseconds(val1 - val2)/1e9) + "  |" 

def compare_neutrons(output_ws_name, duplicate, time_shift):
    ws = mtd[output_ws_name]
    for index in range(0,ws.getNumberHistograms()):
        pulse_times = ws.getEventList(index).getPulseTimes()
        pulse_times_2 = duplicate.getEventList(index).getPulseTimes()
        for i in range(0, len(pulse_times)):
            time1 = pulse_times[i]
            time2 = pulse_times_2[i]
            if time_duration.total_nanoseconds(pulse_times[i] - pulse_times_2[i])/1e9 != time_shift:
                sys.exit("The time difference for neutrons does not seem correct. Original was: " + str(pulse_times[i]) + " and shifted was: pulse_times_2[i]" )

#-------------------------------------------------------------------------
# DEFINE SHIFTS HERE - You need to load a your workspace into Mantid and use their name as the input
#-------------------------------------------------------------------------
#SET THIS FLAG TO PRINT LOG COMPARISON
PRINT_LOG = True

#-- RELATIVE TIME SHIFT
input_ws_name_REL = "SANS2D00022023"
output_ws_name_REL = "REL_SAMPLE"
time_shift_REL = 1000.0
run_comparison(input_ws_name= input_ws_name_REL, output_ws_name= output_ws_name_REL,  relative_time_shift= time_shift_REL, log = PRINT_LOG)

#-- ABSOLUTE TIME SHIFT
input_ws_name_ABS = "SANS2D00022023"
output_ws_name_ABS = "ABS_SAMPLE"
absolute_time_shift_ABS ="2013-10-25T13:58:03"
run_comparison(input_ws_name= input_ws_name_ABS, output_ws_name= output_ws_name_ABS,  absolute_time_shift= absolute_time_shift_ABS)

