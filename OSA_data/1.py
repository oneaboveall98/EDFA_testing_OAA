import pyvisa
import serial
import numpy as np
import math
import scipy.constants as C
import re

#define function elog-string convert to float
def elog2float(elogstr):
    wholeOrigValue = 0.0
    foundEPower = re.search("(?P<coefficientPart>[-+]\d+\.\d+)e(?P<ePowerPart>[-+]\d+)", elogstr, re.I)
    if foundEPower:
        coefficientPart = foundEPower.group("coefficientPart")
        ePowerPart = foundEPower.group("ePowerPart")
        coefficientValue = float(coefficientPart)
        ePowerValue = float(ePowerPart)
        wholeOrigValue = coefficientValue * float(math.pow(10, ePowerValue))
    return wholeOrigValue

#import serial
#serial = serial.Serial('COM9', 115200)  # 打开COM1并设置波特率为115200，COM1只适用于Windows

# set the VOA
ser = serial.Serial('COM9', 115200, timeout=0.5)  # 打开COM9并设置波特率为115200
ser.write('voa 1 set 20\n'.encode())
ser.write('VOA 2 SET 10\n'.encode())

# set the OSA
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB::25::INSTR', timeout=500000)

# -----------------------------------------------------------
# with no EDFA,i.e. original spectrum
# sweep
inst.write("init:imm;*opc?")
inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
inst.write("calc1:mark1:srl")
inst.write("sens:wav:span 10nm")
inst.write("init:imm;*opc?")
inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
inst.write("init:imm;*opc?")
inst.write("init:cont off")
inst.write("calc1:aver:stat on")
inst.write("calc1:aver:coun 10")
inst.write("init:imm;*opc?")

# center
inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
# x_data = []
# y_data = []
inst.write("calc:mark1:func:delt:stat on")
# x_center = elog2float(inst.query("calc1:mark1:x?"))
# x_data.append(x_center)
# y_center = elog2float(inst.query("calc1:mark1:y?"))
# y_data.append(y_center)
y_org = elog2float(inst.query("calc1:mark1:y?"))	##这里读原谱的峰值功率密度

inst.write("calc1:aver:clear")
inst.write("calc1:aver:stat off")
# ------------------------------------------------------------

# 更换光路

# 更换完成


# ------------------------------------------------------------
# with EDFA,i.e. original spectrum
# sweep
inst.write("init:imm;*opc?")
inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
inst.write("calc1:mark1:srl")
inst.write("sens:wav:span 10nm")
inst.write("init:imm;*opc?")
inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
inst.write("init:imm;*opc?")
inst.write("init:cont off")
inst.write("calc1:aver:stat on")
inst.write("calc1:aver:coun 10")
inst.write("init:imm;*opc?")

# center
inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
x_data = []
y_data = []
inst.write("calc:mark1:func:delt:stat on")
x_center = elog2float(inst.query("calc1:mark1:x?"))
x_data.append(x_center)
y_center = elog2float(inst.query("calc1:mark1:y?"))
y_data.append(y_center)

# trace
for i in range(9):
    c = (i+1)
    # print("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
    inst.write("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
    x_data.append(elog2float(inst.query("calc1:mark1:x?")))
    y_data.append(elog2float(inst.query("calc1:mark1:y?")))
    inst.write("calc:mark1:func:delt:x:offs " + "-0."+str(c)+"nm")
    x_data.append(elog2float(inst.query("calc1:mark1:x?")))
    y_data.append(elog2float(inst.query("calc1:mark1:y?")))
    
#print(x)
#print(y)
inst.write("calc1:aver:clear")
inst.write("calc1:aver:stat off")
# ------------------------------------------------------------


#ployfit
fit = np.polyfit(x_data,y_data,deg=1)
gain_db = y_center-y_org							##gain in dB
gain = float(math.pow(10,gain_db))
ase_db = x_center*fit[0]+fit[1] 
ase = float(math.pow(10,ase_db))
nf = 10*log10(1/gain+(ase*C.c)/(gain*C.h*x_center))	##NF

print(ase)
print(x_data)
print(y_data)
print(fit)



