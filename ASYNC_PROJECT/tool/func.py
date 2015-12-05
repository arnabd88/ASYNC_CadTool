import sys
import re
import copy

##---- Trims a string towards the left
def trimleft( trimString ):
	#trimString = trimString.split()
	while( re.match(' ',trimString)):
		trimString = trimString[1:]
	return trimString
	
	
def writeSG( fsg, sglist ):
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
			
		fsg.write(fromState+"----"+tx+"----"+toState+"\n")
		
	fsg.write("\n.end")
		
