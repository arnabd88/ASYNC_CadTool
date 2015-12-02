import sys
import re
import copy

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
		markList = []
		graphStart = 0;
		CommentList = [ i.split('#')[1]  for i in lpn if('#' in i)]
		self.init_state = [i.split( )[1][1:].split(']')[0] for i in CommentList if('init_state' in i)]
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
		self.T = self.TransPlace.keys()
		##'Places to postset transitions'
		for i in self.PlaceTrans.keys():
			if(i in markList) :
		   		self.P[i] = 1 ;
			else :
		   		self.P[i] = 0 ;
		self.display()

	


