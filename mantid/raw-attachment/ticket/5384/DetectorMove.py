rawMapWS = Load(r'\\isis\inst$\NDXMERLIN\Instrument\data\cycle_11_5\MER12024.raw')  

deti = rawMapWS.getDetector( 204801 )
detiID = deti.getID()
detiPositionX = deti.getPos().X()
detiPositionY = deti.getPos().Y() 
detiPositionZ = deti.getPos().Z()
yNew = -0.05
print "About to move detector from", detiPositionY
MoveInstrumentComponent( rawMapWS, DetectorID=detiID, Y=yNew )
print "Moved detector. About get its new position."
newDetiPositionY = deti.getPos().Y()  #MANTID CRASHES HERE
print "Got new position. About to print old position, then new position."
print "Old position", detiPositionY
print "New position", newDetiPositionY

    
    
