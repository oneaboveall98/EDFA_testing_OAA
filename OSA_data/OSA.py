import pyvisa
import serial
import numpy as np
import math
import re
import tkinter as tk
import scipy.constants as C

y_org = -26


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


def first_step():
    global y_org
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
    y_org = elog2float(inst.query("calc1:mark1:y?"))  # 这里读原谱的峰值功率密度
    max_power.set(str(round(y_org)))
    inst.write("calc1:aver:clear")
    inst.write("calc1:aver:stat off")


def second_step():
    global y_org
    # set the VOA
    ser = serial.Serial('COM9', 115200, timeout=0.5)  # 打开COM9并设置波特率为115200
    ser.write('voa 1 set 20\n'.encode())
    ser.write('VOA 2 SET 10\n'.encode())
    #
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
    x_center = elog2float(inst.query("calc1:mark1:x?"))
    x_data.append(x_center)
    y_center = elog2float(inst.query("calc1:mark1:y?"))
    y_data.append(y_center)

    # trace
    for i in range(9):
        c = (i + 1)
        # print("calc:mark1:func:delt:x:offs " + "0."+str(c)+"nm")
        inst.write("calc:mark1:func:delt:x:offs " + "0." + str(c) + "nm")
        x_data.append(elog2float(inst.query("calc1:mark1:x?")))
        y_data.append(elog2float(inst.query("calc1:mark1:y?")))
        inst.write("calc:mark1:func:delt:x:offs " + "-0." + str(c) + "nm")
        x_data.append(elog2float(inst.query("calc1:mark1:x?")))
        y_data.append(elog2float(inst.query("calc1:mark1:y?")))

    # print(x)
    # print(y)
    inst.write("calc1:aver:clear")
    inst.write("calc1:aver:stat off")
    # ------------------------------------------------------------

    # ployfit
    fit = np.polyfit(x_data, y_data, deg=1)
    gain_db = y_center - y_org  # gain in dB
    Gain = round(float(math.pow(10, gain_db / 10)))
    ase_db = x_center * fit[0] + fit[1]
    print(ase_db)
    ase = float(math.pow(10, ase_db / 10) * math.pow(10, 6)) / 0.01  # unit:dbm
    row = ase / 3 * math.pow(10, -26) * 1550 * 1550
    nf = round(10 * math.log10(1 / Gain + row * 1550 * math.pow(10, -9) / (Gain * C.h * C.c)))  # NF
    # nf = round(10 * math.log10(1 / Gain))
    NF.set(str(nf))
    gain.set(str(round(gain_db)))


def show_func():
    var = 'This software is designed to measuring the NF and GAIN automatically.Just press the MEASURE button to start!!!'
    t.delete('1.0', 'end')
    t.insert('insert', var)


def show_config():
    var = '''Center Wavelength:  1550nm              Power Input:        6.99dBm             VOA Attenustion:    VOA1:20dB  VOA2:10dB'''
    t.delete('1.0', 'end')
    t.insert('insert', var)


# 设置画布
window = tk.Tk()
window.title('My Window')
window.geometry('500x500')  # 这里的乘是小x
canvas = tk.Canvas(window, bg='blue', height=200, width=500)
# 说明图片位置，并导入图片到画布上
image_file = tk.PhotoImage(file='F:\Python\py\pic.gif')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
image = canvas.create_image(250, 0, anchor='n', image=image_file)
canvas.pack()
# 设置输出label
NF = tk.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
gain = tk.StringVar()
max_power = tk.StringVar()
l_NF = tk.Label(window, textvariable=NF, bg='white', fg='black', font=('Arial', 12), width=10, height=1)
l_NF_l = tk.Label(window, text='NF', bg='pink', fg='white', font=('Arial', 12), width=10, height=1)
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
l_gain = tk.Label(window, textvariable=gain, bg='white', fg='black', font=('Arial', 12), width=10, height=1)
l_gain_l = tk.Label(window, text='gain', bg='pink', fg='white', font=('Arial', 12), width=10, height=1)
l_gain_l.place(x=300, y=330, anchor='n')
l_gain.place(x=400, y=330, anchor='n')
l_NF_l.place(x=300, y=390, anchor='n')
l_NF.place(x=400, y=390, anchor='n')
peak_power = tk.Label(window, textvariable=max_power, bg='white', fg='black', font=('Arial', 12), width=10, height=1)
peak_power_1 = tk.Label(window, text='peak_power', bg='pink', fg='white', font=('Arial', 12), width=10, height=1)
peak_power_1.place(x=300, y=270, anchor='n')
peak_power.place(x=400, y=270, anchor='n')
measure = tk.Button(window, text='measure', font=('Arial', 12), width=10, height=1, command=second_step)
measure.place(x=420, y=210, anchor='n')
premeasure = tk.Button(window, text='premeasure', font=('Arial', 12), width=10, height=1, command=first_step)
premeasure.place(x=290, y=210, anchor='n')
menubar = tk.Menu(window)

# 第6步，创建一个File菜单项（默认不下拉，下拉内容包括New，Open，Save，Exit功能项）
filemenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='more', menu=filemenu)

# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
filemenu.add_command(label='function', command=show_func)
filemenu.add_command(label='configuration', command=show_config)
# filemenu.add_command(label='Save', command=do_job)
filemenu.add_separator()  # 添加一条分隔线
filemenu.add_command(label='Exit', command=window.quit)
window.config(menu=menubar)
t = tk.Text(window, width=20, height=10)
t.place(x=100, y=250, anchor='n')
show_config()
window.mainloop()
