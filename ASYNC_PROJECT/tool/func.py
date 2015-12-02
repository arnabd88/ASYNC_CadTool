import sys
import re
import copy

##---- Trims a string towards the left
def trimleft( trimString ):
	#trimString = trimString.split()
	while( re.match(' ',trimString)):
		trimString = trimString[1:]
	return trimString
