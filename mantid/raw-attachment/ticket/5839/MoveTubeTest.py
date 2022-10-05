#
# TUBE MOVING TEST to test ticket #5839
#
#
    
# Load Workspace    
WS = Load(r'\\isis\inst$\NDXMERLIN\Instrument\data\cycle_11_5\MER12024.raw') 

# Move Tubexxx of door3 up one metre.
MoveInstrumentComponent( WS,'door3/tube_3_5',X=0.0,Y=1.0,Z=0.0)
