# !usr/bin env python
# -*- coding: utf-8 -*-  

import re
import math  

def ConvertELogStrToValue(eLogStr):
    """    
    convert string of natural logarithm base of E to value    
    return (convertOK, convertedValue)    
    eg:    
    input:  -1.1694737e-03    
	output: -0.001169    
	input:  8.9455025e-04    
	output: 0.000895    
	"""     
	
    (convertOK, convertedValue) = (False, 0.0)    
    foundEPower = re.search("(?P<coefficientPart>-?\d+\.\d+)e(?P<ePowerPart>-\d+)", eLogStr, re.I)    
    #print "foundEPower=",foundEPower    
    if(foundEPower):
        coefficientPart = foundEPower.group("coefficientPart")
        ePowerPart = foundEPower.group("ePowerPart")        
		#print "coefficientPart=%s,ePower=%s"%(coefficientPart, ePower)        
        coefficientValue = float(coefficientPart)        
        ePowerValue = float(ePowerPart)        
		#print "coefficientValue=%f,ePowerValue=%f"%(coefficientValue, ePowerValue)        
		#math.e= 2.71828182846        
		# wholeOrigValue = coefficientValue * math.pow(math.e, ePowerValue)        
        wholeOrigValue = coefficientValue * math.pow(10, ePowerValue)         
		
		#print "wholeOrigValue=",wholeOrigValue;         
        (convertOK, convertedValue) = (True, wholeOrigValue)    
    else:        
        (convertOK, convertedValue) = (False, 0.0)     
    return (convertOK, convertedValue) 
	
def parseIntEValue(intEValuesStr):    
	# print "intEValuesStr=", intEValuesStr    
    intEStrList = re.findall("-?\d+\.\d+e-\d+", intEValuesStr)    
	# intEStrList = intEValuesStr.split(' ')    
	# print "intEStrList=", intEStrList    
    for eachIntEStr in intEStrList:        
		# intValue = int(eachIntEStr)        
		# print "intValue=",intValue        
        (convertOK, convertedValue) = ConvertELogStrToValue(eachIntEStr)        
		#print "convertOK=%s,convertedValue=%f"%(convertOK, convertedValue)        
        print "eachIntEStr=%s,\tconvertedValue=%f" % (eachIntEStr, convertedValue) 
	
	# intEValuesStr= 2.1690427e-005 -1.1694737e-003 -6.1193734e-004
	# 8.9455025e-004 -8.6277081e-004 -7.2735757e-004
	# intEStrList= ['2.1690427e-005', '-1.1694737e-003', '-6.1193734e-004', '8.9455025e-004', '-8.6277081e-004', '-7.2735757e-004']# eachIntEStr=2.1690427e-005,     convertedValue=0.014615
	# eachIntEStr=-1.1694737e-003,    convertedValue=-0.058225
	# eachIntEStr=-6.1193734e-004,    convertedValue=-0.112080
	# eachIntEStr=8.9455025e-004,     convertedValue=0.163843
	# eachIntEStr=-8.6277081e-004,    convertedValue=-0.158022
	# eachIntEStr=-7.2735757e-004,    convertedValue=-0.133220 
	
	
if __name__ == "__main__":    
    data_path = "/home/jianjiang/workingdir/CHA/linear-regression/data/data.txt"    
	with open(data_path, 'r') as f:        
	    for line in f.readlines():            
		    linestr = line.strip()            
			# print linestr            
			parseIntEValue(linestr)
















    
# if __name__  == "__main__":
    # test = “-5.2216393443E+001”
	# 字符串的特点 底数和指数，以E隔开
	# index_E = string.index(test, beg=0, end=len(string))
	# test.startswith(obj, beg=0,end=len(string))
	
