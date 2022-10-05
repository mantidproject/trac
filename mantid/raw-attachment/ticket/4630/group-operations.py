Load(Filename='/home/tr9/svn-mantid/Test/Data/SystemTests/POLREF00003014.raw',OutputWorkspace='POLREF00003014')
S=mtd['POLREF00003014'] # Scan type workspace with 22 entries
T=mtd['POLREF00003014']

M=S-T 			# Works
M=S+T # doesn't create a workspace group

