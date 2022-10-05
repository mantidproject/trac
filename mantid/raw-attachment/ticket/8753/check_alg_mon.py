
OUT = 'trans_test_rear'

trans_test_rear = mtd[OUT]

hist = trans_test_rear.getHistory()

index = 0
final_index = 500

try:
  while True:
	try:
	  alg = hist.getAlgorithm(index)
	except ValueError: 
	   index +=1
	   continue
	index+=1
	if alg.name() == 'ExtractSingleSpectrum':
		final_index = index + 3
		print str(alg)
		
	if alg.name() == 'CalculateFlatBackground':
		print str(alg)
	
	if index > final_index:
		break


except IndexError: 
    print 'finished'	
	
