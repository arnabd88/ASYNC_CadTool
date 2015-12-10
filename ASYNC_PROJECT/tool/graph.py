import sys
import re
import copy
import func

##[row[i] for row in AT] for i in range(0,len(AT[0]))

class  graph:
	def __init__(self, name):
		self.name = name ## setting the petri net
		print "Instantiating graph: ",name

	def display(self):
		print "============================"
		print " Displaying Petri Net"
		print "============================"
		print "I:",self.inputs, 'O:',self.outputs, 'Int:', self.internals
		print "Aspec:", self.Aspec
		print "Initial State : ", self.init_state 
		print "Current Place Marking : \n======================"
		for i,v in self.P.iteritems():
			print i, v
		print "PlaceTrans============="
		for i,v in self.PlaceTrans.iteritems():
			print i,v
		print "\n\nTransitionPresets========"
		for i,v in self.TransitionPresets.iteritems():
			print i, v
		print "TransExcite=============\n"
		for i,v in self.transExcite.iteritems():
			print i, v

	def CreateDSlpn(self, lpn):
		print "============================="
		print "Invoking CreateDSlpn"
		print "============================="
		self.lpn = lpn
		self.TransPlace = dict([])
		self.PlaceTrans = dict([])
		self.inputs = []
		self.outputs = []
		self.internals = []
		self.P = dict([])
		self.T = dict([])
		self.transExcite = dict([])
		markList = []
		graphStart = 0;
		CommentList = [ i.split('#')[1]  for i in lpn if('#' in i)]
		state = [i.split( )[1][1:].split(']')[0] for i in CommentList if('init_state' in i)]
			##	self.init_state = line.split( )[1][1:].split(']')[0]
		self.lpn = [ i.split('#')[0]  for i in lpn]
		for line in self.lpn:
			line_list = line.split( )
			##---- get the outputs -----
			if('input' in line):
				self.inputs = line.split( )
				self.inputs = self.inputs[1:len(self.inputs)]
			elif('output' in line):
				self.outputs = line.split()
				self.outputs = self.outputs[1:len(self.outputs)]
			elif('internal' in line):
				self.internals = line.split()
				self.internals = self.internals[1:len(self.internals)]
			elif('markin' in line and '#' not in line):
			    line = line.split('{')[1].split('}')[0]
			    markList = line.split('>')
			    for i in range(0,len(markList)-1):
				    markList[i] = markList[i].split('<')[1].split(',')
				    markList[i] = 'Place_'+markList[i][0]+'_'+markList[i][1]
				##---- Update this later -----
			elif('.graph' in line):
				graphStart = 1 ;
				print '===== Graph Start Detected ===='
			elif('.end' in line):
				graphStart = 0 ;
				print '===== Graph Ends Here ===='
			elif(graphStart==1 and len(line_list)!=0):
				transPlaceList = line.split( );
				##---- Check if the first one is the transition -----
				if('+' in transPlaceList[0] or '-' in transPlaceList[0]):
					## ----- create the transition excitation tag -------
					if('+' in transPlaceList[0]):
						self.transExcite[transPlaceList[0]] = ['R', transPlaceList[0].split('+')[0]]
					elif('-' in transPlaceList[0]):
						self.transExcite[transPlaceList[0]] = ['F', transPlaceList[0].split('-')[0]]
					## --------------------------------------------------
					if (transPlaceList[0] not in self.TransPlace.keys()):
						self.TransPlace[transPlaceList[0]] = []
					for i in range(1,len(transPlaceList)):
						if('+' not in transPlaceList[i] and '-' not in transPlaceList[i]): ## Indicating a place
							self.TransPlace[transPlaceList[0]].append(transPlaceList[i])
						else : ## A transition
						    ## Update places with namesof P_preset_postset
							self.TransPlace[transPlaceList[0]].append('Place_'+transPlaceList[0]+'_'+transPlaceList[i])
							if('Place_'+transPlaceList[0]+'_'+transPlaceList[i] not in self.PlaceTrans.keys()):
								self.PlaceTrans['Place_'+transPlaceList[0]+'_'+transPlaceList[i]] = []
							self.PlaceTrans['Place_'+transPlaceList[0]+'_'+transPlaceList[i]].append(transPlaceList[i])
				else :
					if(transPlaceList[0] not in self.PlaceTrans.keys()):
						self.PlaceTrans[transPlaceList[0]] = []
					for i in range(1,len(transPlaceList)):
						self.PlaceTrans[transPlaceList[0]].append(transPlaceList[i])
		self.Aspec = set(self.inputs) | set(self.outputs) | set(self.internals)
		##self.T = self.TransPlace.keys()
		##'Places to postset transitions'
		for i in self.PlaceTrans.keys():
			if(i in markList) :
		   		self.P[i] = 1 ;
			else :
		   		self.P[i] = 0 ;
		##Making Transition and Presets
		self.TransitionPresets = dict([])
		for trans in self.TransPlace.keys():
			self.TransitionPresets[trans] = []
			for place, tx in self.PlaceTrans.iteritems():
				if(trans in tx):
					self.TransitionPresets[trans].append(place)
		all_signals = self.inputs+self.outputs+self.internals
		self.init_state = dict([])
		for i in range(0,len(all_signals)):
			self.init_state[all_signals[i]] = state[0][i] 
		#####---------------------------
		self.display()

	def getMarking(self):
		self.M = []
		for places, val in self.P.iteritems():
			if(val == 1):
				self.M.append(places);
		print "Marking: ", self.M
		return self.M
	
    
		

	def getEnabledTransitions(self):
		Te = []
		for trans,places in self.TransitionPresets.iteritems():
			notEnabled = 0
			for preset in places:
				if(self.P[preset]==0):
					notEnabled = 1
			if(notEnabled==0):
				Te.append(trans)
				self.T[trans] = 1
			else :
				self.T[trans] = 0
		print "Enabled Transitions: ", Te
		return Te
		
	def updatePlaces(self, M):
		mark = copy.deepcopy(M)
		for place in self.P.keys():
			self.P[place] = 0 
			if(place in mark):
				self.P[place] = 1
					

	def find_SG(self):
		print "Find_SG"
		self.M0 = self.getMarking()
		lambdaS = dict([])
		M = tuple(self.M0) 
		s = copy.deepcopy(self.init_state)
		print "Init_state: ", self.init_state
		Te = self.getEnabledTransitions()
		print "Init_state: ", self.init_state
		stack = []
		if(len(Te)==0):
			return ['STG_DEADLOCK:Incorrect_Spec']
		SET = []
		SET.append(M)
		lambdaS[M] = copy.deepcopy(s) 
		done = 0
		delta = []
		while(done == 0):
			##done = 1
			t = copy.deepcopy(Te[0])
			if(len(Te)>1):
				print "Stack :", M, s, Te[1:]
				stack.append([M,s,Te[1:]])
			if( len(((set(M) - set(self.TransitionPresets[t])) & set(self.TransPlace[t]))) != 0):
				return ['STG is not safe']
			Mi = tuple((set(M) - set(self.TransitionPresets[t]))   |  set(self.TransPlace[t]))
			si = copy.deepcopy(s)
			if(self.transExcite[t][0] == 'R'):
				si[self.transExcite[t][1]] = '1'
			elif(self.transExcite[t][0] == 'F'):
				si[self.transExcite[t][1]] = '0'
			##delta = set([M, t, Mi])
			delta1 = [M, t, Mi]
			delta.append(delta1)
			if(Mi not in SET):
				SET.append(Mi)
				lambdaS[Mi] = copy.deepcopy(si)
				M = copy.deepcopy(Mi)
				s = copy.deepcopy(si)
				self.updatePlaces(M)
				Te = self.getEnabledTransitions()
				if(len(Te)==0):
					return ['STG_DEADLOCK:Incorrect_Spec']
			else:
				if(lambdaS[Mi] != si):
					return ['Inconsistent State Assignment: Mi: '+Mi+'   1: '+lambdaS[Mi]+'   2:  '+si]
				if(len(stack)!=0):
					bucket = stack.pop()
					M = copy.deepcopy(bucket[0])
					s = copy.deepcopy(bucket[1])
					Te = copy.deepcopy(bucket[2])
					print "Pop: " , Te, M, self.P, "\n\n\n"
					self.updatePlaces(M)
					print "Update P :", self.P, "\n", s, "\n\n\n"
				else:
					done = 1
				
		result = ["Final SG is in this list", SET, delta, lambdaS, self.inputs, self.outputs, self.internals]
		return result
			
			
			
			
			
			
			
			
			
			
			
			
	   	
