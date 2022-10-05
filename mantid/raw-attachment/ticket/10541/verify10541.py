LoadIsawPeaks(Filename='verify10541.peaks', OutputWorkspace='peaks')
LoadIsawUB(Inputworkspace='peaks',Filename='verify10541.mat')
nx_event_filename = '/SNS/MANDI/2014_1_11B_SCI/data/MANDI_801_event.nxs'
event_ws = LoadEventNexus( Filename = nx_event_filename )
md = ConvertToDiffractionMDWorkspace( InputWorkspace = event_ws, LorentzCorrection = False )
IntegratePeaksMD(InputWorkspace='md', PeakRadius=0.003, PeaksWorkspace='peaks', OutputWorkspace='peaks', IntegrateIfOnEdge=False, Cylinder=True, CylinderLength=0.075, PercentBackground=10, ProfileFunction='NoFit', IntegrationOption='Sum')
