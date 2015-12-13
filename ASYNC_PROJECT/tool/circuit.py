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
		self.internals=[]
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
			if(signalName not in input  and signalName not in output and signalName not in self.internals):
				self.internals.append(signalName)
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
		#print 'FanInList:', FanInList
		#print 'state:', state
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
			
			
	def getExcitedSignals(self,state,nonInput):
		sigNext = dict([])
		for sig in self.outSignals:
			sigNext[sig] = self.Evaluate(sig,state)
		for i in sigNext.keys():
			if(sigNext[i]==state[i]):
				del sigNext[i]
		if(nonInput==1):
			return sigNext
		else:
			if(len(self.inputs)!=0):
				for i in self.inputs:
					sigNext[i] = func.compStr(state[i])
			
		return sigNext
	
	def retState (self, hashDict):
		retList = []
		print 'allSignals:', self.allSignals
		for i in self.allSignals:
			retList.append(hashDict[i])
		return retList
		
	def extend_state( self, state ):
		s = copy.deepcopy(state)
		si = copy.deepcopy(s)
		last_s = copy.deepcopy(s)
		done = 0
		ReachedExtendState = 0
		stack = []
		tempStack = []
		result = dict([])
		for i in self.outputs:	
			result[i] = 0
		Te = self.getExcitedSignals(s,1) ##passing 1 returns excitation on only outputs and internal signals
		print 'Te-extend: ', Te
		if(len(Te.keys())==0):
			ReachedExtendState = 1
			##result.append([
		while(done != 1):
			t = Te.keys()[0]
			del Te[t]
			si = copy.deepcopy(s)
			if(len(Te.keys())!=0):
				stack.append([s,Te])
			si[t] = func.compStr(s[t])
			print 'Arnab', si
			tempTe = self.getExcitedSignals(si,1)
			print 'tempte-Excitation', tempTe
			ReachedExtendState = 0
			outSig = ''
			if(len(tempTe.keys())==0):
				ReachedExtendState = 1
				#result['noExcitation'] = 0
				#result['extendState'] = copy.deepcopy(si)
				result[t] = 1
				done = 1
			else:
				for sig in self.outputs:
					if(sig in tempTe.keys()):
						ReachedExtendState = 1
						outSig = sig
						result[outSig] = 1
				if(ReachedExtendState==1):
					result[outSig] = 1
					#result['noExcitation'] = 1
				else:
					s = copy.deepcopy(si)
					Te = tempTe
				if(ReachedExtendState==1  and len(stack)!=0):
					tempStack = stack.pop()
					si = tempStack[0]
					Te = tempStack[1]
					if(Te.keys()==0):
						done = 1
				elif(ReachedExtendState==1 and len(stack)==0):
					done = 1
		print '================= from extend state ======================'
		print '------------------ state = ',state , '--------------------'
		for i, v in result.iteritems() :
			print i ,'   ', v
		print '================ end of extend state ====================='
		return result
					
				
			
				
	def find_implSG( self, sgList, sgl):
		s = copy.deepcopy(self.init_state)
		si = copy.deepcopy(s)
		self.currentState = copy.deepcopy(self.init_state)
		done = 0
		stack = []
		failState = dict([])
		TRANSSET = []
		Te = self.getExcitedSignals(s,0)
		result = []
		if(len(Te.keys())==0):
			result = ['DeadLock']
			return result
		while(done != 1):
			failFlag = 0
			t = Te.keys()[0]
			del Te[t]
			si = copy.deepcopy(s)
			if(len(Te)!=0):
				stack.append([s,Te])
			si[t] = func.compStr(s[t])
			tempTe = self.getExcitedSignals(si,0)
			prevtempTe = self.getExcitedSignals(s,0)
			if(len(tempTe.keys())==0):
				failFlag = 1
			else:
				for trans in prevtempTe:
					if( trans not in self.inputs  and trans not in tempTe and trans!=t): ## transition has been disabled by this choice
						failFlag = 1
						print 'Fail Due to trans: ', t, Te, prevtempTe
			if(failFlag == 0 and [self.retState(s),t,self.retState(si)] not in TRANSSET):
				TRANSSET.append([self.retState(s),t,self.retState(si)])
				Te = tempTe
				s = copy.deepcopy(si)
			else:
				if(failFlag==1):
					print 'FailHere: ', self.retState(s),t,self.retState(si)
					if(tuple(self.retState(s)) not in failState):
						failState[tuple(self.retState(s))]=[]						
					if([s,t,si] in failState[tuple(self.retState(s))]):
						print 'Repeat'
					else:
						failState[tuple(self.retState(s))].append([s,t,si])
				if(len(stack)==0):
					done = 1
				else:
					tempStack = stack.pop()
					#print 'tempStack: ', tempStack
					Te = tempStack[1]
					s  = tempStack[0]
					if(len(Te.keys())==0):
						print 'TempStack :', tempStack
						print 'Because I was here'
						#done = 1
		result = ['Successful', TRANSSET, failState]
		return result
					
					
					
				
			
				
			
			
	def verifyCge( self, inputs, outputs, internals, init_state, sgList, sgl ):
		self.inputs = inputs
		self.outputs = outputs
		#self.internals = internals
		print 'self:', self.internals
		for i in internals:
			if(i not in self.internals):
				self.internals.append(i)
		print 'self2:', self.internals
		self.init_state = init_state
		retResult = dict([])
		for i in self.internals:
			self.init_state[i] = '0' ## this is an assumption that initially all internal signals are zero
		print 'New init state:', self.init_state
		self.allSignals = inputs+outputs+self.internals
		self.outputsExt = dict([])
		self.extSignals = inputs+outputs
		self.outSignals = outputs+self.internals
		self.StateSequence = self.getStateSequence(sgl)
		self.currentState = dict([])
		implState = dict([])
		#for pre, post in self.StateSequence.iteritems():
		#	print 'PRE: ', pre+'   ', post
		implSG = self.find_implSG( sgList, sgl );
		print implSG[0]
		print "============ FAILSTATE ================"
		for i, v in implSG[2].iteritems():
			print i, ': ==> :',v, '\n'
		print "============ TRANSSET =================\n\n"
		for i in implSG[1]:
			print 'here: ', i
		implState = dict([])
		vecDict = dict([])
		cgeDict = dict([])
		implSet = implSG[1]
		for i in implSG[1]:
			#print i[0], '  :  ',i[1],'  :  ',i[2]
			for j in range(0,len(self.allSignals)):
				implState[self.allSignals[j]] = i[0][j]
			print 'ImplState: ', implState
			if(tuple(i[0]) not in vecDict):
				vecDict[tuple(i[0])] = implState
			if(len(self.getExcitedSignals(implState,1).keys())!=0):
				retResult = self.extend_state(implState)
				print 'Got external excitations:', implState
				if( tuple(i[0]) not in cgeDict):
					print 'noMatch :', retResult, tuple(i[0])
					cgeDict[tuple(i[0])] = retResult
			else:
				retResult['noExcitation']=1
				#for k in self.outputs:
					#retResult[k] = implState[k]
					#retResult[k] = 0
			#print 'RetResult: ', retResult

					
		for i, v in cgeDict.iteritems():
			print '================ CGE_DICT ======================'
			print i, '   ', v
			print '=============== end cge dict ==================='
			
		
		for keyset, valset in self.StateSequence.iteritems():
			s = keyset
			sigTransList = []
			print 'key:' , keyset, '\nval:', valset
			for el in valset:
				if('+' in el[0]):
					sigTransList.append(el[0].split('+')[0])
				elif('-' in el[0]):
					sigTransList.append(el[0].split('-')[0])
				else:
					sigTransList.append(el[0])
			print 'MakesigTransList:', sigTransList
			print '\n state', keyset
			for i in cgeDict.keys():
				print '\ncgedictKeys', i
				s = func.concatList(i)[0:len(keyset)]
				print 'Concat string:', s
				if(keyset == func.concatList(i)[0:len(keyset)]):
					###---- Match the output signals ------
					for sigout in self.outputs:
						print '\n keyset', keyset, sigout, cgeDict[i]
						if(sigout not in sigTransList  and sigout not in cgeDict[i]):
							print 'Mark PassVacuous:',sigout
							print 'sigTransList:', sigTransList
						elif(sigout not in sigTransList and sigout in cgeDict[i]):
							print 'Mark Fail', sigout
							print 'cgeDict', cgeDict[i]
							print 'sigTransList:', sigTransList
						elif(sigout in sigTransList and sigout not in cgeDict[i]):
							print 'Mark Fail', sigout, cgeDict[i]
							print 'cgeDict', cgeDict[i]
							print 'sigTransList:', sigTransList
						elif(sigout in sigTransList and sigout in cgeDict[i]):
							print 'Mark Pass', sigout
							print 'sigTransList:', sigTransList
				else:
					print 'Unable to match', keyset
					
			
		
				
			
			
			
		

		#for state in self.StateSequence.keys():
		#	for i in range(0,len(self.extSignals)):
		#		self.currentState[self.extSignals[i]] = state[i]
			#print self.currentState
		#	for out in self.outputs:
		#		self.outputsExt = self.Evaluate(out)
			
			
			
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
			
		
