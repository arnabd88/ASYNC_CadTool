import sys
import re
import copy
import func

class circuit:
	def __init__(self,name):
		self.name = name
	
	def getSignalName( self, expr ):
		if('+' in expr):
			signal = expr.split(':')[0].split('+')[1]
		elif('-' in expr):
			signal = expr.split(':')[0].split('-')[1]
		else:
			signal = expr.split(':')[0]
		return signal
		
	def getSignalDict(self, prs):
		circuitDict = dict([])
		for line in prs:
			line = func.trim(func.concatList(func.concatList(func.concatList(line.split('#')[0:]).split('[')[1]).split(']')[0]))
			signalName = self.getSignalName(line)
			circuitDict[signalName] = {'SET': [], 'RESET': [], 'COMB':[]}			
		return circuitDict
		
	def getExprList(self, line):
		print "LineExpr : ", line
		return line.split('(')[1].split(')')[0].split('&')
			

		
		
	def createCircuit(self, prs, input, output):
		self.prs = prs
		print "======== Creating Circuit Structure ==========="
		print "IO_LIST: " , input, output
		self.circuitDict = self.getSignalDict(prs)
		for line in prs:
			print "LineExpr : ", line
			line = func.trim(func.concatList(func.concatList(func.concatList(line.split('#')[0:]).split('[')[1]).split(']')[0]))
			print "Line: ", line
			signalName = self.getSignalName(line)
			print 'Signal :', signalName
			if('+' in line):
				self.circuitDict[signalName]['SET'].append(self.getExprList(line))
			elif('-' in line):
				self.circuitDict[signalName]['RESET'].append(self.getExprList(line))
			else:
				self.circuitDict[signalName]['COMB'].append(self.getExprList(line))			
		for i,v in self.circuitDict.iteritems():
			for j, k in v.iteritems():
				print 'SignalDict  :', i, j, k
		#self.Evaluate('csc1')
			
	

	def getFanInList( self, sig ):
		FI = []
		for i, v in self.circuitDict[sig].iteritems():
			for j in v :
				#print 'from circuitDict :', j, v
				for k in j:
					if('~' in k):
						#print 'True'
						dum_sig = func.concatList(k.split('~')[1])
					else:
						dum_sig = k 
					if(dum_sig not in FI):
						FI.append(dum_sig)
		return FI
		
	def getStateSequence(self, sgl):
		print 'IOs : ', self.inputs, self.outputs
		signalVectorList = self.inputs+self.outputs
		start = 0
		dictState = dict([])
		stgList = []
		for line in sgl:
			if('.SG' in line):
				start = 1
			elif('.end' in line):
				start = 0
			elif(start == 1 and line!='' and line!=' '):
				stgList = func.trimList(line.split(' '))
				print stgList
			if(len(stgList)!=0):
				if(stgList[0] not in dictState):
					dictState[stgList[0]] = []
				dictState[stgList[0]].append([stgList[1], stgList[2]])	
		return dictState
			
			
		
			
	def Evaluate(self,x,state):
		FanInList = self.getFanInList(x)
		FanInVal = dict([])
		for i in FanInList:
			FanInVal[i] = state[i]
			FanInVal['~'+i] = func.compStr(state[i])
		comb_OrEval = 0
		set_OrEval = 0
		reset_OrEval = 0
		combAndEval = 0
		setAndEval = 0
		resetAndEval = 0
		if(len(self.circuitDict[x]['COMB'])!=0):
			combList = self.circuitDict[x]['COMB']
			comb_OrEval = 0
			for ckt in combList:
				combAndEval = 1
				for i in ckt:
					combAndEval = combAndEval & int(FanInVal[i])
				comb_OrEval = comb_OrEval | combAndEval
		if(len(self.circuitDict[x]['SET'])!=0):
			setList = self.circuitDict[x]['SET']
			set_OrEval = 0
			for  ckt in setList:
				setAndEval = 1
				for i in ckt:
					setAndEval = setAndEval & int(FanInVal[i])
				set_OrEval = set_OrEval | setAndEval
		if(len(self.circuitDict[x]['RESET'])!=0):
			resetList = self.circuitDict[x]['RESET']
			reset_OrEval = 0
			for ckt in resetList:
				resetAndEval = 1
				for i in ckt:
					resetAndEval = resetAndEval & int(FanInVal[i])
				reset_OrEval = reset_OrEval | resetAndEval
		result = comb_OrEval | func.Celem(set_OrEval , int(func.compStr(str(reset_OrEval))), int(state[x]))
		return str(result)
			
			
			
	"""def Evaluate( self,x ):
		FanInList  =  self.getFanInList(x)
		print x+' FanInList : ', FanInList
		FanInVal = dict([])
		comb_OrEval = 0
		set_OrEval = 0
		reset_OrEval = 0
		combAndEval = 1
		setAndEval = 1
		setAndEval = 1
		#for sig in FanInList:
			if(sig in self.extSignals):
				FanInVal[sig] = self.currentState[sig] ## no need to evaluate further
				FanInVal['~'+sig] = func.compStr(self.currentState[sig])
			else:
				temp = self.Evaluate(sig)
				FanInVal[sig] = temp
				FanInVal['~'+sig] = func.compSte(temp)
		if(len(self.circuitDict[x]['COMB'])!=0):
			combList = self.circuitDict[x]['COMB']
			comb_OrEval = 0
			for ckt in combList:
				combAndEval = 1
				#OrEval  = 0
				for i in ckt:
					combAndEval = combAndEval & int(FanInVal[i])
				comb_OrEval = comb_OrEval | combAndEval
		if(len(self.circuitDict[x]['SET'])!=0):
			setList = self.circuitDict[x]['SET']
			set_OrEval = 0
			for ckt in setList:
				setAndEval = 1
				for i in ckt:
					setAndEval = setAndEval & int(FanInVal[i])
				set_OrEval = set_OrEval | setAndEval
		if(len(self.circuitDict[x]['RESET'])!=0):
			resetList = self.circuitDict[x]['RESET']
			reset_OrEval = 0
			for ckt in resetList:
				resetAndEval = 1
				for i in ckt:
					resetAndEval = resetAndEval & int(FanInVal[i])
				reset_OrEval = reset_OrEval | resetAndEval
				
		result = comb_OrEval | func.Celem(set_OrEval , func.compStr(str(reset_OrEval)), int(self.currentState[x]))"""
			
			
	def getExcitedSignals(self,state):
		sigNext = dict([])
		for sig in self.outSignals:
			sigNext[sig] = self.Evaluate(sig,state)
		for i in sigNext.keys():
			if(sigNext[i]==state[i]):
				del sigNext[i]
		if(len(self.inputs)!=0):
			for i in self.inputs:
				sigNext[i] = func.compStr(state[i])
			
		return sigNext
	
	def retState (self, hashDict):
		retList = []
		for i in self.allSignals:
			retList.append(hashDict[i])
		return retList
			
			
				
	def find_implSG( self, sgList, sgl):
		s = copy.deepcopy(self.init_state)
		si = copy.deepcopy(s)
		self.currentState = copy.deepcopy(self.init_state)
		done = 0
		stack = []
		failState = dict([])
		TRANSSET = []
		Te = self.getExcitedSignals(s)
		print 'FirstExcitedSignals :', Te
		result = []
		if(len(Te.keys())==0):
			result = ['DeadLock']
			return result
		while(done != 1):
			#done = 1
			failFlag = 0
			#Te = self.getExcitedSignals(s)
			#print 'state :', s
			#print 'TE :', Te
			print '============================================'
			print 'State: ', self.retState(s)
			print 'ExcitedSignals :', Te
			t = Te.keys()[0]
			del Te[t]
			stack.append([s,Te])
			si[t] = func.compStr(s[t])
			tempTe = self.getExcitedSignals(si)
			#print 'Stack :', stack
			#print 'TempTe : ', tempTe
			print 'Trans Taken: ', t
			print 'Trans stacked: ', Te
			if(len(tempTe.keys())==0):
				failFlag = 1
			else:
				for trans in Te:
					if( trans not in self.inputs  and trans not in tempTe ): ## transition has been disabled by this choice
						failFlag = 1
						print 'Fail Due to trans: ', t, Te
			if(failFlag == 0 and [self.retState(s),t,self.retState(si)] not in TRANSSET):
				TRANSSET.append([self.retState(s),t,self.retState(si)])
				Te = tempTe
				s = copy.deepcopy(si)
			else:
				if(failFlag==1):
					print 'FailHere: ', self.retState(s),t,self.retState(si)
					if(tuple(self.retState(s)) not in failState):
						failState[tuple(self.retState(s))]=[]						
					failState[tuple(self.retState(s))].append([s,t,si])
				if(len(stack)==0):
					done = 1
				else:
					tempStack = stack.pop()
					#print 'tempStack: ', tempStack
					Te = tempStack[1]
					s  = tempStack[0]
					if(len(Te.keys())==0):
						done = 1
		result = ['Successful', TRANSSET, failState]
		return result
					
					
					
				
			
				
			
			
	def verifyCge( self, inputs, outputs, internals, init_state, sgList, sgl ):
		self.inputs = inputs
		self.outputs = outputs
		self.outputs = internals
		self.init_state = init_state
		for i in internals:
			self.init_state[i] = '0' ## this is an assumption that initially all internal signals are zero
		self.allSignals = inputs+outputs+internals
		self.outputsExt = dict([])
		self.extSignals = inputs+outputs
		self.outSignals = outputs+internals
		self.StateSequence = self.getStateSequence(sgl)
		self.currentState = dict([])
		for pre, post in self.StateSequence.iteritems():
			print pre+'   ', post
		implSG = self.find_implSG( sgList, sgl );
		print implSG[0]
		print "============ FAILSTATE ================"
		for i, v in implSG[2].iteritems():
			print i, ': ==> :',v
		print "============ TRANSSET ================="
		for i in implSG[1]:
			print i[0], '  :  ',i[1],'  :  ',i[2]

		#for state in self.StateSequence.keys():
		#	for i in range(0,len(self.extSignals)):
		#		self.currentState[self.extSignals[i]] = state[i]
			#print self.currentState
		#	for out in self.outputs:
		#		self.outputsExt = self.Evaluate(out)
			
			
			
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
			
		
