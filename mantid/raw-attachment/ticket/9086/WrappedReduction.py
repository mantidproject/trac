import numpy
import sys, os
import dis, inspect, opcode
import matplotlib.pyplot as plt
from mantid.simpleapi import *

############################################################################################
def lineno():
    """
    call signature(s)::
    lineno()

    Returns the current line number in our program.
    
    No Arguments.


    Working example
    >>> print "This is the line number ",lineno(),"\n"
    
    """
    return inspect.currentframe().f_back.f_lineno

def decompile(code_object):
	''' 	taken from http://thermalnoise.wordpress.com/2007/12/30/exploring-python-bytecode/

	decompile extracts dissasembly information from the byte code and stores it in a 
		list for further use.
	
	call signature(s)::
		instructions=decompile(f.f_code)

	Required arguments:
	=========   =====================================================================
	f.f_code    A  bytecode object ectracted with inspect.currentframe()
		    or anyother mechanism that returns byte code.   
	
	Optional keyword arguments: NONE	

	Outputs:
	=========   =====================================================================
	instructions  a list of offsets, op_codes, names, arguments, argument_type, 
			argument_value which can be deconstructed to find out various things
			about a function call.

	Examples:
	
	f = inspect.currentframe().f_back.f_back
	i = f.f_lasti  # index of the last attempted instruction in byte code
	ins=decompile(f.f_code)
	pretty_print(ins)
	

	'''
	code = code_object.co_code
	variables = code_object.co_cellvars + code_object.co_freevars
	instructions = []
	n = len(code)
	i = 0
	e = 0
	while i < n:
		i_offset = i
		i_opcode = ord(code[i])
		i = i + 1
		if i_opcode >= opcode.HAVE_ARGUMENT:
			i_argument = ord(code[i]) + (ord(code[i+1]) << (4*2)) + e
			i = i +2
			if i_opcode == opcode.EXTENDED_ARG:
				e = iarg << 16
			else:
				e = 0
			if i_opcode in opcode.hasconst:
				i_arg_value = repr(code_object.co_consts[i_argument])
				i_arg_type = 'CONSTANT'
			elif i_opcode in opcode.hasname:
				i_arg_value = code_object.co_names[i_argument]
				i_arg_type = 'GLOBAL VARIABLE'
			elif i_opcode in opcode.hasjrel:
				i_arg_value = repr(i + i_argument)
				i_arg_type = 'RELATIVE JUMP'
			elif i_opcode in opcode.haslocal:
				i_arg_value = code_object.co_varnames[i_argument]
				i_arg_type = 'LOCAL VARIABLE'
			elif i_opcode in opcode.hascompare:
				i_arg_value = opcode.cmp_op[i_argument]
				i_arg_type = 'COMPARE OPERATOR'
			elif i_opcode in opcode.hasfree:
				i_arg_value = variables[i_argument]
				i_arg_type = 'FREE VARIABLE'
			else:
				i_arg_value = i_argument
				i_arg_type = 'OTHER'
		else:
			i_argument = None
			i_arg_value = None
			i_arg_type = None
		instructions.append( (i_offset, i_opcode, opcode.opname[i_opcode], i_argument, i_arg_type, i_arg_value) )
	return instructions
 
# Print the byte code in a human readable format
def pretty_print(instructions):
	print '%5s %-20s %3s  %5s  %-20s  %s' %  ('OFFSET', 'INSTRUCTION', 'OPCODE', 'ARG', 'TYPE', 'VALUE')
	for (offset, op, name, argument, argtype, argvalue) in instructions:
		print '%5d  %-20s (%3d)  ' % (offset, name, op),
		if argument != None:
			print '%5d  %-20s  (%s)' % (argument, argtype, argvalue),
		print


def lhs(output='names'):
	''' 	
	call signature(s)::
	NamesofOutPutsExpected    = lhs(output='names')   # This is the default
	NumberOfOutputsExpected  = lhs('number')
	Number, Names                    = lhs('both')

	Return how many values the caller is expecting or the names of the output variables on the left of the = in a list or both. 

	Required arguments:	NONE
	
	Optional keyword arguments: NONE	


	Outputs:
	=========   =====================================================================
	numReturns	Number of return values on expected on the left of the equal sign.

	Examples:

	This function is not designed for cammand line use.  Using in a function can 
	follow the form below.
	
	def MyFunction():
		"""Documentation for MyFunction
		"""
		ReturnVarNumber, ReturnVarNames=lhs('both')
		### Do something useful 
		single = 1, double_1 = 1, double_2=2
		
		if ReturnVarNumber == 0:
			# process like a void return
			return
		elif  ReturnVarNumber == 1:
			# return a single output
			return single
		elif ReturnVarNumber == 2:
			# retrun a pair
			return double_1, double_2
			
	x     = MyFunction() # returns x=1
	x, y = MyFunction() # returns x=1, y=2

	'''
	f = inspect.currentframe().f_back.f_back
	i = f.f_lasti  # index of the last attempted instruction in byte code
	ins=decompile(f.f_code)
	#pretty_print(ins)

	CallFunctionLocation={}
	first=False; StartIndex=0; StartOffset=0
	# we must list all of the operators that behave like a function call in byte-code
	OperatorNames=set(['CALL_FUNCTION','UNARY_POSITIVE','UNARY_NEGATIVE','UNARY_NOT','UNARY_CONVERT','UNARY_INVERT','GET_ITER', 'BINARY_POWER','BINARY_MULTIPLY','BINARY_DIVIDE', 'BINARY_FLOOR_DIVIDE', 'BINARY_TRUE_DIVIDE', 'BINARY_MODULO','BINARY_ADD','BINARY_SUBTRACT','BINARY_SUBSCR','BINARY_LSHIFT','BINARY_RSHIFT','BINARY_AND','BINARY_XOR','BINARY_OR'])

	for index in range(len(ins)):
		(offset, op, name, argument, argtype, argvalue) = ins[index]
		if name in OperatorNames:
			if not first:
				CallFunctionLocation[StartOffset] = (StartIndex,index)
			StartIndex=index
			StartOffset = offset

	(offset, op, name, argument, argtype, argvalue) = ins[-1]
	CallFunctionLocation[StartOffset]=(StartIndex,len(ins)-1) # append the index of the last entry to form the last boundary

	#print CallFunctionLocation
	#pretty_print( ins[CallFunctionLocation[i][0]:CallFunctionLocation[i][1]] )
	# In our case i should always be the offset of a Call_Function instruction. We can use this to baracket 
	# the bit which we are interested in
	
	OutputVariableNames=[]
	(offset, op, name, argument, argtype, argvalue) = ins[CallFunctionLocation[i][0] + 1] 
	if name == 'POP_TOP':  # no Return Values
		pass
		#return OutputVariableNames
	if name == 'STORE_FAST' or name == 'STORE_NAME': # One Return Value 
		OutputVariableNames.append(argvalue)
	if name == 'UNPACK_SEQUENCE': # Many Return Values, One equal sign 
		for index in range(argvalue):
			(offset_, op_, name_, argument_, argtype_, argvalue_) = ins[CallFunctionLocation[i][0] + 1 + 1 +index] 
			OutputVariableNames.append(argvalue_)
	maxReturns = len(OutputVariableNames)
	if name == 'DUP_TOP': # Many Return Values, Many equal signs
		# The output here should be a multi-dim list which mimics the variable unpacking sequence.
		# For instance a,b=c,d=f() => [ ['a','b'] , ['c','d'] ]
		#              a,b=c=d=f() => [ ['a','b'] , 'c','d' ]  So on and so forth.

		# put this in a loop and stack the results in an array.
		count = 0; maxReturns = 0 # Must count the maxReturns ourselves in this case
		while count < len(ins[CallFunctionLocation[i][0] :CallFunctionLocation[i][1]]):
			(offset_, op_, name_, argument_, argtype_, argvalue_) = ins[CallFunctionLocation[i][0]+count] 
			#print 'i= ',i,'count = ', count, 'maxReturns = ',maxReturns
			if name_ == 'UNPACK_SEQUENCE': # Many Return Values, One equal sign 
				hold=[]
				#print 'argvalue_ = ', argvalue_, 'count = ',count
				if argvalue_ > maxReturns:
					maxReturns=argvalue_
				for index in range(argvalue_):
					(_offset_, _op_, _name_, _argument_, _argtype_, _argvalue_) = ins[CallFunctionLocation[i][0] + count+1+index] 
					hold.append(_argvalue_)
				count = count + argvalue_
				OutputVariableNames.append(hold)
			# Need to now skip the entries we just appended with the for loop.
			if name_ == 'STORE_FAST' or name_ == 'STORE_NAME': # One Return Value 
				if 1 > maxReturns:
					maxReturns = 1
				OutputVariableNames.append(argvalue_)
			count = count + 1

	# Now that OutputVariableNames is filled with the right stuff we need to output the correct thing. Either the maximum number of 
	# variables to unpack in the case of multiple ='s or just the length of the array or just the naames of the variables.		
	
	if output== 'names':
		return OutputVariableNames
	elif output == 'number':
		return maxReturns 
	elif output == 'both':
		return (maxReturns,OutputVariableNames)
	
	return 0 # Should never get to here

############################################################################################
def centerbins(xvals):
	''' for a given numpy array return the bin centers 
	'''
	NewXvals=( xvals + numpy.roll(xvals,-1) )/2 # calculate the bin center 
	return numpy.delete(NewXvals,-1) # remove the last element which is junk
	

def CorrectMonitor(TheWorkspaceToCorrect):
	''' Correct the monitors so that I/Io would return a flat line if the detector was in the direct beam
	'''
	WorkspaceToCorrect=CloneWorkspace(TheWorkspaceToCorrect)
	CorrectedOutput=0
	if WorkspaceToCorrect.isMultiPeriod():
		instrument=WorkspaceToCorrect[0].getInstrument()
	else:
		instrument=WorkspaceToCorrect.getInstrument()

	CorrectionType=instrument.getStringParameter('correction')[0]
	if CorrectionType == 'polynomial':
		CorrectedOutput=PolynomialCorrection(InputWorkspace=WorkspaceToCorrect, Coefficients=instrument.getStringParameter('polystring')[0], Operation='Multiply') #Operation='Divide'
	elif CorrectionType == 'exponential':
		CorrectedOutput=ExponentialCorrection(InputWorkspace=WorkspaceToCorrect,C0=instrument.getNumberParameter('C0')[0], C1=instrument.getNumberParameter('C1')[0], Operation='Multiply')#Operation='Divide'

	return CorrectedOutput

def CorrectPolarization(TheDataIn):
	'''
	This function takes a two period data set or four period data set and corrects for polarization efficiencies.
	'''
	# Make a copy of the data to work on locally 
	DataIn=CloneWorkspace(TheDataIn)
	# Check the the workspace is in wavelength
	
	if DataIn.isMultiPeriod():
		instrument=DataIn[0].getInstrument()
	else:
		instrument=DataIn.getInstrument()

	# Calculate the required polynomials
	Ones=DataIn[1] * 0.0 + 1.0 # The polynomial correction function operates on a workspace of ones.  
				   # In the case of multidetector data we expect the monitors have been stripped away.    
	rho    = PolynomialCorrection(InputWorkspace=Ones,Coefficients=instrument.getStringParameter('crho')[0])
	Pp     = PolynomialCorrection(InputWorkspace=Ones,Coefficients=instrument.getStringParameter('cPp')[0])
	if(len(DataIn) == 2):# R+ and R-
		# split out the spin-states and name them according to the journal article
		Ip=DataIn[0];  Ia=DataIn[1]
		#print "Ip,Ia ",Ip, Ia
		D = Pp * ( 1.0 + rho) 
		nIp = ( Ip * (rho * Pp + 1.0) + Ia * (Pp - 1.0) ) / D
		nIa = ( Ip * (rho * Pp - 1.0) + Ia * (Pp + 1.0) ) / D
		#print "nIp,nIa ",nIp, nIa
		DataOut=GroupWorkspaces([nIp, nIa])
		return DataOut

	elif(len(DataIn)== 4):# R++ , R+- , R-+ , R-- 
		
		alpha  = PolynomialCorrection(InputWorkspace=Ones,Coefficients=instrument.getStringParameter('calpha')[0])
		Ap     = PolynomialCorrection(InputWorkspace=Ones,Coefficients=instrument.getStringParameter('cAp')[0])

		# split out the spin-states and name them according to the journal article
		Ipp=DataIn[0];  Iaa=DataIn[1]; Ipa=DataIn[2]; Iap=DataIn[3]
		
		############## Precalculate parts of the correction equation
		A0 = Iaa * Pp * Ap + Ap * Ipa * rho * Pp + Ap * Iap * Pp * alpha + Ipp * Ap * alpha * rho * Pp
		A1 = Pp * Iaa
		A2 = Pp * Iap
		A3 = Ap * Iaa
		A4 = Ap * Ipa
		A5 = Ap * alpha * Ipp
		A6 = Ap * alpha * Iap
		A7 = Pp * rho   * Ipp
		A8 = Pp * rho   * Ipa

		D = Pp * Ap *( 1.0 + rho + alpha + rho * alpha ) 

		############## Build the corrections    # Note the mathematical symmetry 
		nIpp = (A0 - A1 + A2 - A3 + A4 + A5 - A6 + A7 - A8 + Ipp + Iaa - Ipa - Iap) / D
		nIaa = (A0 + A1 - A2 + A3 - A4 - A5 + A6 - A7 + A8 + Ipp + Iaa - Ipa - Iap) / D
		nIpa = (A0 - A1 + A2 + A3 - A4 - A5 + A6 + A7 - A8 - Ipp - Iaa + Ipa + Iap) / D
		nIap = (A0 + A1 - A2 - A3 + A4 + A5 - A6 - A7 + A8 - Ipp - Iaa + Ipa + Iap) / D

		DataOut=GroupWorkspaces([nIpp, nIaa, nIpa, nIap])
		return DataOut
	else: 
		print len(DataIn), ' This function only operates on 2 or 4 period data' 
		return DataIn; # Should scream with an error here.  We can only correct data which has 2 or 4 spin-states

def ref(RunNumbers='8169+8171+8173+8175+8177+8179+8181', theta=1.0):
	'''Basic shorthand for the default point detector reduction.
	
	  Example:
	
	 >>>  rqz, rLambda , ThetaOut= ref(RunNumbers='8169+8171+8173+8175+8177+8179+8181', theta=1.0)
	'''
	ReturnVarNumber, ReturnVarNames=lhs('both')
	dd=Load(RunNumbers); 
	trans=CreateTransmissionWorkspaceAuto(FirstTransmissionRun=dd,I0MonitorIndex='2',ProcessingInstructions='2')
	#Now correct for the monitor to detector efficiency and optionally correct the monitors to deal with the polarization corrections too
	trans=CorrectMonitor(trans)
	(_,rl,ThetaOut)=ReflectometryReductionOneAuto(InputWorkspace=dd,I0MonitorIndex='2',ProcessingInstructions='3',ThetaIn=theta,FirstTransmissionRun=trans,StrictSpectrumChecking=False)
	
	RcorrectedVsLambda = CorrectPolarization(rl)
	CloneWorkspace(InputWorkspace=RcorrectedVsLambda,OutputWorkspace=ReturnVarNames[1])
	
	RcorrectedVsQz = RcorrectedVsLambda.convertUnits('MomentumTransfer')
	CloneWorkspace(InputWorkspace=RcorrectedVsQz,OutputWorkspace=ReturnVarNames[0])
	
	return mtd[ReturnVarNames[0]], mtd[ReturnVarNames[1]] , ThetaOut

def refq(RunNumbers='8169+8171+8173+8175+8177+8179+8181', theta=1.0):
	'''Outputs I/Io vs qz.  See ref for more documentation.
	
	  Example:
	  >>> xx=refq(RunNumbers='8169+8171+8173+8175+8177+8179+8181', theta=1.0)
	'''
	rq,rl,ThetaOut=ref(RunNumbers, theta)
	# Ensure that the desired output is coppied and named correctly.  This is required since Mantid is not completely pass by value. 
	ReturnVarNumber, ReturnVarNames=lhs('both')
	CloneWorkspace(InputWorkspace=rq,OutputWorkspace=ReturnVarNames[ReturnVarNumber-1])
	return mtd[ReturnVarNames[ReturnVarNumber-1]]

def refl(RunNumbers='8169+8171+8173+8175+8177+8179+8181', theta=1.0):
	'''Outputs I/Io vs lambda. See ref for more documentation.
	
	  Example:  
	  >>> xx = refl(RunNumbers='8169+8171+8173+8175+8177+8179+8181')
	'''
	rq,rl,ThetaOut=ref(RunNumbers, theta)
	# Ensure that the desired output is coppied and named correctly.  This is required since Mantid is not completely pass by value. 
	ReturnVarNumber, ReturnVarNames=lhs('both')
	CloneWorkspace(InputWorkspace=rq,OutputWorkspace=ReturnVarNames[ReturnVarNumber-1])
	return mtd[ReturnVarNames[ReturnVarNumber-1]]
	
