import sys
import re
import copy
import graph
import func

flpn = open(sys.argv[1], 'r+');
fckt = open(sys.argv[2], 'r+');
fsg  = open(sys.argv[1].split('.')[0]+'.sg', 'w')


lpn = []
ckt = []

for line in flpn:
    
	lpn.append(line)

for line1 in fckt:
	print line1

graph_name = sys.argv[1].split('.')
print graph_name
SG = graph.graph(graph_name[0])
SG.CreateDSlpn(lpn)
getSG = SG.find_SG()
print "Message :", getSG[0]
if(len(getSG)>1):
	print "\n\n\n\n"
	print "=============== SET ================"
	print getSG[1] ,"\n\n"
	print "=============== DELTA(M,t,Mi) =============="
	print getSG[2], "\n\n"
	print "=============== LambdaS ================"
	print getSG[3]
	func.writeSGfull(fsg, getSG)
	if(len(getSG[6]) !=0 ):
		fsgSpec = open(sys.argv[1].split('.')[0]+'.spSpec', 'w')
		func.writeSGspec(fsgSpec, getSG)
#SG.disPlay()
