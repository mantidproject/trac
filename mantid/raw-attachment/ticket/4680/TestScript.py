from mantidsimple import *

PIX=1.1E-3 #m
RunNo=4699
RIO=[69,80]
DB=[26,31]
Theta=0.49
SC=175


Load(Filename='POLREF00004699.raw',OutputWorkspace='X')
X=mtd['X']
ConvertUnits(InputWorkspace=X,OutputWorkspace=X,Target="Wavelength",AlignBins="1")
CropWorkspace(InputWorkspace=X,OutputWorkspace='Io',XMin=0.8,XMax=14.5,StartWorkspaceIndex=2,EndWorkspaceIndex=2)
CropWorkspace(InputWorkspace=X,OutputWorkspace='D',XMin=0.8,XMax=14.5,StartWorkspaceIndex=3)
Io=mtd['Io']
D=mtd['D']

Divide(D,Io,'I','1','1')
I=mtd['I']

ConvertSpectrumAxis(InputWorkspace=I,OutputWorkspace='tl1',Target='signed_theta')

inst=I[0].getInstrument()
sampleLocation=inst.getComponentByName('some-surface-holder').getPos()
detLocation=inst.getComponentByName('pointdetector').getPos()
sample2detector=detLocation-sampleLocation    # meters


# Move the detector so that the detector channel matching the reflected beam is at 0,0
MoveInstrumentComponent(Workspace=I,ComponentName="lineardetector",X=0,Y=0,Z=-PIX*(SC))


#CloneWorkspace(I,'I2')
ConvertSpectrumAxis(InputWorkspace=I,OutputWorkspace='tl2',Target='signed_theta')