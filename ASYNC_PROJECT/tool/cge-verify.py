import sys
import re
import copy
import graph
import circuit
import func

flpn = open(sys.argv[1], 'r+');
fckt = open(sys.argv[2], 'r+');
fsg  = open(sys.argv[1].split('.')[0]+'.sg', 'w')


lpn = []
ckt = []

for line in flpn:    
	lpn.append(line)

for line in fckt:
	ckt.append(line)

graph_name = sys.argv[1].split('.')
print graph_name
SG = graph.graph(graph_name[0])
CKT = circuit.circuit(graph_name[0])
SG.CreateDSlpn(lpn)
getSG = SG.find_SG()
print "Message :", getSG[0]
if(len(getSG)>1):
	print "Hell0: ", getSG[4:7]
	func.writeSGfull(fsg, getSG)
	if(len(getSG[6]) !=0 ):
		fsgSpec = open(sys.argv[1].split('.')[0]+'.sgSpec', 'w')
		func.writeSGspec(fsgSpec, getSG)
		fsgSpec.close()
	fsg.close()
	CKT.createCircuit(ckt,SG.inputs,SG.outputs)
	###---------- Perform CGE verify ---------------####
	if(len(getSG[6]) !=0):
		fopen = open(sys.argv[1].split('.')[0]+'.sgSpec', 'r+')
	else:
		fopen = open(sys.argv[1].split('.')[0]+'.sg', 'r+')
	sgl = []
	for line in fopen:
		sgl.append(line)
	CKT.verifyCge(SG.inputs, SG.outputs, SG.internals, SG.init_state, getSG, sgl)
#SG.disPlay()


