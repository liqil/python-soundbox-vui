#!/usr/bin/python3
import  re
from tkinter.constants import TOP
import 	NativeGui
from   	NativeGui import ToolsGUI
import 	NativeSerial
from   	NativeSerial import SerialCommunication, SerialPorts

SerialModule   = SerialCommunication()

# the callback for the combolist of the serial port list
def EventSerialPortSelectUpdate(port):
    print('selected port: ', port)

def EventBtnConnectedCallback(port, connect):
    print('prepare to open selected port: ', port)
    SerialModule.CloseEngine()
    ret = SerialModule.OpenEngine(port, 921600, 0.5)
    return ret
    # SerialModule.Print_Name()

def EventSerialPortReadLineCallback(line):
    ## print(f'aa {line}')
    # TopGui.UpdateLog("aa "+line, 0)
    color_sch_str = '''\033'''
    line     = re.sub(pattern="\[0m", repl="", string=line)
    # TopGui.UpdateLog("bb "+line, 0)
    line     = re.sub(pattern="\[0;3[0-9]m", repl="", string=line, count=1)
    
    # to update print erea
    TopGui.UpdateLog(line, 0)

    wakeup_str = TopGui.GetWakeupKeywords()
    flow_str   = TopGui.GetAsrFlowKeywords()
    asr_str    = TopGui.GetAsrEndKeywords()
    nlp_str    = TopGui.GetNlpEndKeywords()

    if  line.find(wakeup_str) > -1:
        TopGui.Wakeuped()
    elif line.find(flow_str) > -1 or line.find(asr_str) > -1:
        split_result = (line.split(' '))
        # print (split_result[-1])
        TopGui.ShowResult(split_result[-1])
        #print(f'{line[-1]}')
    elif line.find(nlp_str) > -1:
        print("11111111111111111111")
        split_result = (line.split(' '))
        TopGui.ShowResult(split_result[-1])
        TopGui.SessionEnd()

def EventWindowExit():
    #SerialModule.Close()
    SerialModule.CloseEngine()

TopGui = ToolsGUI()

TopGui.Create(SerialCommunication.GetComList())
TopGui.SetSerialPortSelectUpdateCallback    (EventSerialPortSelectUpdate)
TopGui.SetWindowExitCallback                (EventWindowExit)
TopGui.SetBtnConnectedCallback              (EventBtnConnectedCallback)
SerialModule.SetSerialPortReadLineCallback  (EventSerialPortReadLineCallback)

#进入消息循环体
TopGui.MainLoop()