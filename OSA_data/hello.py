import pyvisa
import serial
from tkinter import *  # 导入 Tkinter 库

ser = serial.Serial('COM9', 115200, timeout=0.5)  # 打开COM9并设置波特率为115200
# ser.write('voa 1 set 20\n'.encode())
# ser.write('VOA 2 SET 20\n'.encode())

# print(ser.stopbits, ser.parity, ser.bytesize)
# print(ser.read(200))

rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB::25::INSTR', timeout=500000)


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


inst.write("calc1:mark1:max")
inst.write("calc1:mark1:scen")
a = []


inst.write("calc:mark1:func:delt:stat on")
a = [inst.query("calc1:mark1:x?"), inst.query("calc1:mark1:y?")]


for i in range(9):
    c = (i+1)
    # print("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
    inst.write("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
    a.append([inst.query("calc1:mark1:x?"), inst.query("calc1:mark1:y?")])
    inst.write("calc:mark1:func:delt:x:offs " + "-0."+str(c)+"nm")
    a.append([inst.query("calc1:mark1:x?"), inst.query("calc1:mark1:y?")])

inst.write("calc1:aver:clear")
inst.write("calc1:aver:stat off")
print(a)



