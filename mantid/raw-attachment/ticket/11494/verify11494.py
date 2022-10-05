# create table workspace and parent log workspace
LoadSpiceAscii(Filename='HB2A_exp0231_scan0001.dat',
      IntegerSampleLogNames="Sum of Counts, scan, mode, experiment_number",
      FloatSampleLogNames="samplemosaic, preset_value, Full Width Half-Maximum, Center of Mass",
      DateAndTimeLog='date,MM/DD/YYYY,time,HH:MM:SS AM',
      OutputWorkspace='Exp0231DataTable',
      RunInfoWorkspace='Exp0231ParentWS')

# load for HB2A
ConvertSpiceDataToRealSpace(InputWorkspace='Exp0231DataTable',
      RunInfoWorkspace='Exp0231ParentWS',
      OutputWorkspace='Exp0231DataMD',
      OutputMonitorWorkspace='Exp0231MonitorMD')

# Get raw counts of DetID = 20 out
ws = GetSpiceDataRawCountsFromMD(InputWorkspace='Exp0231DataMD', MonitorWorkspace='Exp0231MonitorMD', 
    OutputWorkspace='Det20Counts2Theta', DetectorID=20)
    
# Get raw counts of DetID = 20 out
ws = GetSpiceDataRawCountsFromMD(InputWorkspace='Exp0231DataMD', MonitorWorkspace='Exp0231MonitorMD',  Mode='Pt.',
    Pt=10, OutputWorkspace='Pt10Counts')
    
# Get raw counts of DetID = 20 out
ws = GetSpiceDataRawCountsFromMD(InputWorkspace='Exp0231DataMD', MonitorWorkspace='Exp0231MonitorMD', 
    OutputWorkspace='Det20CountsPt', DetectorID=20, XLabel='Pt.')
    
 # Get raw counts of DetID = 20 out
ws = GetSpiceDataRawCountsFromMD(InputWorkspace='Exp0231DataMD', MonitorWorkspace='Exp0231MonitorMD', 
    Mode='Sample Log', 
    OutputWorkspace='TwoTheta_Pt', SampleLogName='2theta')
    
# Get raw counts of DetID = 20 out
ws = GetSpiceDataRawCountsFromMD(InputWorkspace='Exp0231DataMD', MonitorWorkspace='Exp0231MonitorMD', 
    Mode='Sample Log', 
    OutputWorkspace='Vti_Pt', SampleLogName='vti')
    
# Get raw counts of DetID = 20 out
ws = GetSpiceDataRawCountsFromMD(InputWorkspace='Exp0231DataMD', MonitorWorkspace='Exp0231MonitorMD', 
    Mode='Sample Log', 
    OutputWorkspace='Sorb_Sorb', SampleLogName='sorb', XLabel='sorb')
    
    

