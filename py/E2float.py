import math
import re

#科学记数法转为为float类型小数,使用正则表达式,re模块
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
    #分组(?P<name>),方便取出匹配内容 -?:正负号1次或0次 \d+匹配数字任意次，\.匹配小数点 re.I忽略大小写
    foundEPower = re.search("(?P<coefficientPart>-?\d+\.\d+)e(?P<ePowerPart>-\d+)", eLogStr, re.I)
    if (foundEPower):
        # 整数部分
        coefficientPart = foundEPower.group("coefficientPart")
        # 小数部分
        ePowerPart = foundEPower.group("ePowerPart")
        #转化为float
        coefficientValue = float(coefficientPart)
        ePowerValue = float(ePowerPart)
        #结果
        wholeOrigValue = coefficientValue * math.pow(10, ePowerValue)
        #将内容替换
        print(wholeOrigValue)
        convertedValue =re.sub("-?\d+\.\d+E-\d+",str(wholeOrigValue),eLogStr)
        # print "wholeOrigValue=",wholeOrigValue;
        convertOK=True
        print(convertedValue)
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
        print ("eachIntEStr=%s,\tconvertedValue=%f" % (eachIntEStr, convertedValue))

# import numpy as np
## x_data = [0,1,2,3,4,5]
## y_data = [1003,1002,1001,1000,999,997]
# fit = np.ployfit(x_data,y_data,deg=1)
# ase = fit(center) #存疑
#
#
#if __name__ == "__main__":    
#    data_path = "data.txt"    
#    with open(data_path, 'r') as f:
##         print (f.readlines())
#        for line in f.readlines():
#            linestr = line.strip()
#           # print linestr
#            parseIntEValue(linestr)
        
if __name__ == "__main__":    
    data_path = "data.txt"    
    with open(data_path, 'r') as f:
#        a = 0
        for line in f.readlines():
            linestr = line.strip()
#            print(linestr)
            foundEPower = re.search("(?P<coefficientPart>[-+]\d+\.\d+)e(?P<ePowerPart>[-+]\d+)", linestr, re.I)
            if (foundEPower):
                coefficientPart = foundEPower.group("coefficientPart")
                ePowerPart = foundEPower.group("ePowerPart")
                coefficientValue = float(coefficientPart)
                ePowerValue = float(ePowerPart)
#                if (ePowerValue<0):
#                    ePowerValue = ePowerValue
#                else:
#                    ePowerValue = 0
                wholeOrigValue = coefficientValue * math.pow(10, ePowerValue)
                print(str(wholeOrigValue))
#            else:
#                a = a+1
##                print(foundEPower)
#            nofound = re.search("(?P<coefficientPart>[-+]\d+\.\d+)e(?P<ePowerPart>[-+]\d+)", linestr, re.I)
#            if (nofound):
#                print("yes")
#            else:
#                print('no')
#        print(a)
#                test = wholeOrigValue*2
#                print(test)
