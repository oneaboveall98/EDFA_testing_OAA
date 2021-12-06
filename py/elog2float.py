import math
import re

#科学记数法转为为float类型小数,使用正则表达式,re模块
def elog2float(eLogStr):
    wholeOrigValue = 0.0
    foundEPower = re.search("(?P<coefficientPart>[-+]\d+\.\d+)e(?P<ePowerPart>[-+]\d+)", eLogStr, re.I)
    if (foundEPower):
        coefficientPart = foundEPower.group("coefficientPart")
        ePowerPart = foundEPower.group("ePowerPart")
        coefficientValue = float(coefficientPart)
        ePowerValue = float(ePowerPart)
        wholeOrigValue = coefficientValue * float(math.pow(10, ePowerValue))
    return wholeOrigValue
#
#if __name__ == "__main__":    
#    data_path = "data.txt"    
#    with open(data_path, 'r') as f:
##        a = f.readlines()
##        print(a[0])
##        print(elog2float(a[0]))
#        for line in f.readlines():
#            linestr = line.strip()
#            print(linestr)
#            print(str(elog2float(linestr)))
