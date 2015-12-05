import sys
import re
import copy

##---- Trims a string towards the left
def trimleft( trimString ):
	#trimString = trimString.split()
	while( re.match(' ',trimString)):
		trimString = trimString[1:]
	return trimString
	
def writeSGspec( fsgSpec, sglist ):
	##--------- Writes the SG spec output file ---------
	SET     = copy.deepcopy(sglist[1])
	DELTA   = copy.deepcopy(sglist[2])
	LAMBDAS = copy.deepcopy(sglist[3])
	signalList = sglist[4]+sglist[5] 
	print "Signals :", signalList
	
	fsgSpec.write("Inputs :"+str(sglist[4])+"\n")
	fsgSpec.write("Outputs :"+str(sglist[5])+"\n")
	fsgSpec.write("Signal Vector : <"+str(signalList)+">\n\n\n")
	fsgSpec.write(".SG\n\n")
	
	DELTA_MOD = []
	
	for i in DELTA:
		tx = copy.deepcopy(i[1])
		if('+' in tx):
			signal = tx.split('+')[0]
		elif('-' in tx):
			signal = tx.split('-')[0]
		if(signal in signalList):
			DELTA_MOD.append(i)
	
	trackDuplicate = []
	
	for i in DELTA_MOD:
		tx        =  copy.deepcopy(i[1])
		from_Mark = copy.deepcopy(i[0])
		to_Mark   = copy.deepcopy(i[2])
		fromState = ""
		toState   = ""
		for j in signalList:
			fromState = fromState+LAMBDAS[from_Mark][j]
			
		for k in signalList:
			toState   = toState+LAMBDAS[to_Mark][k]
			
		if ([fromState,tx,toState] not in trackDuplicate):
			trackDuplicate.append([fromState,tx,toState])			
			#fsg.write(fromState+"----"+tx+"----"+toState+"\n")
			##fsg.write('{0:7d} {1:7d} {2:7d}' .format(fromState, tx, toState))
			fsgSpec.write('{0:7} {1:8} {2:7}' .format(fromState, tx, toState))
			fsgSpec.write('\n')
	fsgSpec.write("\n.end")
	
def writeSGfull( fsg, sglist ):
	##---------- Writes the SG output file --------------
	SET     = copy.deepcopy(sglist[1])
	DELTA   = copy.deepcopy(sglist[2])
	LAMBDAS = copy.deepcopy(sglist[3])
	signalList = sglist[4]+sglist[5]+sglist[6]
	print "Signals :", signalList
	
	fsg.write("Inputs :"+str(sglist[4])+"\n")
	fsg.write("Outputs :"+str(sglist[5])+"\n")
	fsg.write("Internals :"+str(sglist[6])+"\n")
	fsg.write("Signal Vector : <"+str(signalList)+">\n\n\n")
	fsg.write(".SG\n\n")
	
	for i in DELTA:
		tx        =  copy.deepcopy(i[1])
		from_Mark = copy.deepcopy(i[0])
		to_Mark   = copy.deepcopy(i[2])
		fromState = ""
		toState   = ""
		for j in signalList:
			fromState = fromState+LAMBDAS[from_Mark][j]
			
		for k in signalList:
			toState   = toState+LAMBDAS[to_Mark][k]
			
		#fsg.write(fromState+"----"+tx+"----"+toState+"\n")
		##fsg.write('{0:7d} {1:7d} {2:7d}' .format(fromState, tx, toState))
		fsg.write('{0:7} {1:8} {2:7}' .format(fromState, tx, toState))
		fsg.write('\n')

		
	fsg.write("\n.end")
		
