import pyvisa
import elog2float
import numpy as np


#import serial
#serial = serial.Serial('COM9', 115200)  # 打开COM1并设置波特率为115200，COM1只适用于Windows


# set the VOA


# set the OSA
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB::25::INSTR', timeout=500000)

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
x_center = x_data.append(inst.query("calc1:mark1:x?"))
y_center = y_data.append(inst.query("calc1:mark1:y?"))

# trace
for i in range(9):
    c = (i+1)
    # print("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
    inst.write("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
    x_data.append(inst.query("calc1:mark1:x?"))
    y_data.append(inst.query("calc1:mark1:y?"))
    inst.write("calc:mark1:func:delt:x:offs " + "-0."+str(c)+"nm")
    x_data.append(inst.query("calc1:mark1:x?"))
    y_data.append(inst.query("calc1:mark1:y?"))
    
#print(x)
#print(y)

#elog2float
x = elog2float(x_data)
y = elog2float(y_data)

#ployfit

# x_data = [0,1,2,3,4,5]
# y_data = [1003,1002,1001,1000,999,997]
fit = np.ployfit(x,y,deg=1)
ase = fit(center) #存疑





