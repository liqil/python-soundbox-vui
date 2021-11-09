from os import X_OK
import threading
import time
from time import time
import tkinter
from   tkinter import *
from   tkinter import ttk
from   PIL import Image, ImageTk

class ToolsGUI:
    def __init__(self):
        self.window = tkinter.Tk()#(className='AI LOG')
        self.window.title("Python GUI")    # 添加标题
        window_width  = self.window.winfo_screenwidth()//3*2
        window_height = self.window.winfo_screenheight()//3*2
        place_x       = self.window.winfo_screenwidth()//6
        place_y       = self.window.winfo_screenheight()//6

        self.window.geometry(f'{window_width}x{window_height}+{place_x}+{place_y}')
        self.window.update()
        # self.window.attributes("-fullscreen", True)
        # self.window.attributes("-topmost", True)
        width = self.window.winfo_width()  # 获取屏幕宽度
        print(f'screen width:{width}')
        height = self.window.winfo_height()  # 获取屏幕高度
        print(f'screen height:{height}')

        def OnClose():
            self.SerialPortCloseCallback()
            self.window.destroy()
        self.window.protocol("WM_DELETE_WINDOW", OnClose)

        self.btn_clicked        = 0
        self.CreatSessionTimeout(100)
        self.StopSessionTimeout()


    def CreatSessionTimeout(self, timeout):
        def SessionTimerFunc():
            print("fuck uuuuuuuuuuuuu ")
            self.session_timer.cancel()
            self.lab_nlp.destroy()
            self.lab_nlp = Label(self.frame_vui, image=self.img_background_zoomed, \
                    font=('', 24), compound='center', justify='left', anchor='w')
            self.lab_nlp.pack()                
        self.session_timer = threading.Timer(timeout, SessionTimerFunc)
        self.session_timer.start()
    def StopSessionTimeout(self):
        self.session_timer.cancel()

    def SetWindowExitCallback(self, Callback):
        self.SerialPortCloseCallback = Callback

    def SetBtnConnectedCallback(self, Callback):
        self.BtnConnectedCallback = Callback

    def SetSerialPortSelectUpdateCallback(self, Callback):
        def UpdateCallback(event):
            print('value的值:{}'.format(self.SelectPort.get()))
            self.SerialPortUpdateCallback(format(self.SelectPort.get()))

        self.SerialPortUpdateCallback = Callback
        self.combobox.bind('<<ComboboxSelected>>', UpdateCallback)

    def UpdateLog(self, line, end):
        self.text_log.insert(INSERT,line)
        self.text_log.see(END)

    def Create(self, ports):
        frame_width = int(self.window.winfo_width()*0.6//1)
        frame_log_width  = int(self.window.winfo_width()*0.6//1)
        frame_log_height = int(self.window.winfo_height()//20*15)
        frame_set_width  = int(self.window.winfo_width()*0.4//1)
        frame_set_height = int(self.window.winfo_height()//20*10)
        frame_vui_width  = int(self.window.winfo_width()*0.4//1)
        frame_padx  = self.window.winfo_width()*0.01//1
        frame_pady  = 10
        frame_color = '#EEEEEE'
        print(f'1111 width:{frame_width}')
        print(f'2222 height:{self.window.winfo_height()//20*2}')
        print(f'2222 padx:{frame_padx}')

        ################## log view ##################
        self.frame_log = Frame(self.window, width=frame_log_width, height=frame_log_height, bg=frame_color, relief='flat')
        self.frame_log.pack_propagate(0)
        self.frame_log.pack(padx=frame_padx, pady=frame_pady, fill=Y, expand=NO, side=LEFT)
        self.frame_log.update()
        print(f'frame_log width:{self.frame_log.winfo_width()}')
        print(f'frame_log height:{self.frame_log.winfo_height()}')
        self.text_log = Text(self.frame_log, height=self.frame_log.winfo_height(), state='normal')
        self.text_log.pack(padx=frame_padx, pady=frame_pady, fill=X, expand=YES, side=LEFT)
        self.text_log.insert(INSERT,'')

        self.text_sb = Scrollbar(self.frame_log, orient=VERTICAL)
        self.text_sb.pack(side=RIGHT, fill=Y)
        self.text_sb.config(command=self.text_log.yview)
        self.text_log.config(yscrollcommand=self.text_sb.set)

        ################## sub2 view ##################
        self.frame_sub2 = Frame(self.window, width=frame_set_width-10, height=frame_set_height, bg=frame_color, relief=RAISED)
        self.frame_sub2.pack_propagate(0)
        self.frame_sub2.pack(pady=frame_pady, fill=Y, expand=YES)
        self.frame_sub2.update()

        ### com set
        if 1:
            self.frame_set = Frame(self.frame_sub2, bg=frame_color, relief=RAISED)
            # self.frame_set.pack_propagate(0)
            # self.frame_set.pack(padx=frame_padx, pady=frame_pady, fill=X, side=TOP, expand=YES)
            self.frame_set.grid(row=0, column=0)

            ### com select
            Label(self.frame_set,text="SerialCom: ").grid(row=0, column=0,  sticky=E+W)
            self.SelectPort = StringVar()
            self.combobox = ttk.Combobox(
                    master=self.frame_set,
                    #height=20,  # 高度,下拉显示的条目数量
                    width=50, #int(self.frame_set.winfo_width()*0.1//1),  # 宽度
                    state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
                    cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
                    #font=('', 16),  # 字体
                    textvariable=self.SelectPort,  # 通过StringVar设置可改变的值
                    values=ports,  # 设置下拉框的选项
                    )
            # print(combobox.keys())  # 可以查看支持的参数
            self.combobox.grid(row=0, column=1, sticky=E+W, columnspan=2)

            def BtnConnectedCallback():
                self.btn_clicked ^= 1
                ret = self.BtnConnectedCallback(self.combobox.get(), self.btn_clicked)
                if (ret and self.btn_clicked):
                    self.btn_connect.configure(text='disconnect')
                else:
                    self.btn_connect.configure(text='connect')
            self.btn_connect = ttk.Button(self.frame_set, text='connect', command=BtnConnectedCallback)
            self.btn_connect.grid(row=0, column=3, sticky=E+W)

            ### Log save
            Label(self.frame_set,text="Log Session:").grid(row=1, column=0, sticky=W)
            self.checkbox_logfile_var = 0
            self.entry_LogFileName = Entry(self.frame_set, relief=RIDGE, takefocus=YES)
            self.entry_LogFileName.delete(0, END)
            self.entry_LogFileName.insert(INSERT,'./esp32_debug_file.log')
            self.entry_LogFileName.grid(row=1, column=1, sticky=E+W, columnspan=2)

            self.checkbox_logfile = Checkbutton(self.frame_set, variable=self.checkbox_logfile_var, relief=RAISED)
            self.checkbox_logfile.grid(row=1, column=3, sticky=W)

            ### wakeup keywords
            Label(self.frame_set, text="WakeUp Words:").grid(row=2, column=0, sticky=W)
            self.entry_WakeupKeywords = Entry(self.frame_set, relief=RIDGE, takefocus=YES)
            self.entry_WakeupKeywords.delete(0, END)
            self.entry_WakeupKeywords.insert(INSERT,'---> EVENT_WAKEUP_TRIGGER status=1, words=小t小t')
            self.entry_WakeupKeywords.grid(row=2, column=1, sticky=E+W, columnspan=2)

            ### asr flow keywords
            Label(self.frame_set, text="Flow Words:").grid(row=3, column=0, sticky=W)
            self.entry_AsrFlowKeywords = Entry(self.frame_set, relief=RIDGE, takefocus=YES)
            self.entry_AsrFlowKeywords.delete(0, END)
            self.entry_AsrFlowKeywords.insert(INSERT,'Flow text voice')
            self.entry_AsrFlowKeywords.grid(row=3, column=1, sticky=E+W, columnspan=2)

            ### asr end keywords
            Label(self.frame_set, text="ASR Words:").grid(row=4, column=0, sticky=W)
            self.entry_AsrEndKeywords = Entry(self.frame_set, relief=RIDGE, takefocus=YES)
            self.entry_AsrEndKeywords.delete(0, END)
            self.entry_AsrEndKeywords.insert(INSERT,'Final asr end')
            self.entry_AsrEndKeywords.grid(row=4, column=1, sticky=E+W, columnspan=2)
            self.frame_set.update()

            ### nlp end keywords
            Label(self.frame_set, text="NLP Words:").grid(row=5, column=0, sticky=W)
            self.entry_NlpEndKeywords = Entry(self.frame_set, relief=RIDGE, takefocus=YES)
            self.entry_NlpEndKeywords.delete(0, END)
            self.entry_NlpEndKeywords.insert(INSERT,'Final nlp text end')
            self.entry_NlpEndKeywords.grid(row=5, column=1, sticky=E+W, columnspan=2)
            self.frame_set.update()

        if 0:
            self.frame_dummy = Frame(self.frame_sub2, bg=frame_color, relief=RIDGE)
            self.frame_dummy.pack_propagate(0)
            # self.frame_vui.pack(padx=frame_padx, side=BOTTOM)## grid(padx=frame_padx, pady=10, row=2, column=0, columnspan=100)
            self.frame_dummy.grid(row=1, column=0, sticky=N+S)

        ################## vui view ##################
        if 1:
            self.frame_vui = Frame(self.frame_sub2, width=frame_set_width-30, height=self.window.winfo_height()//20*3, bg=frame_color, relief='flat')
            self.frame_vui.pack_propagate(0)
            # self.frame_vui.pack(padx=frame_padx, side=BOTTOM)## grid(padx=frame_padx, pady=10, row=2, column=0, columnspan=100)
            self.frame_vui.grid(row=2, column=0, sticky=S)
            self.frame_vui.update()

            photo_wakeuped = Image.open('background.jpg').resize((self.frame_vui.winfo_width(),self.frame_vui.winfo_height()))
            self.img_background_zoomed = ImageTk.PhotoImage(photo_wakeuped)
            photo_wakeuped = Image.open('background_wakeuped.jpg').resize((self.frame_vui.winfo_width(),self.frame_vui.winfo_height()))
            self.img_wakeup_zoomed = ImageTk.PhotoImage(photo_wakeuped)

            self.ShowResultStr = StringVar()
            self.lab_nlp = Label(self.frame_vui, image=self.img_background_zoomed, \
                font=('', 12), compound='center', justify='left', anchor='w')
            self.lab_nlp.pack()
        return self.window

    def GetWakeupKeywords(self):
        return self.entry_WakeupKeywords.get()
    def GetAsrFlowKeywords(self):
        return self.entry_AsrFlowKeywords .get()
    def GetAsrEndKeywords(self):
        return self.entry_AsrEndKeywords.get()
    def GetNlpEndKeywords(self):
        return self.entry_NlpEndKeywords.get()

    def Wakeuped(self):
        #if(self.lab_nlp):
        self.StopSessionTimeout()
        self.CreatSessionTimeout(15)
        self.lab_nlp.destroy()
        self.lab_nlp = ttk.Label(self.frame_vui, image=self.img_wakeup_zoomed, textvariable=self.ShowResultStr, \
                font=('', 24), compound='center', justify='left', anchor='w')
        self.lab_nlp.pack()
        self.ShowResultStr.set(".......")

    def SessionEnd(self):
        self.CreatSessionTimeout(10)
        # def timer_func():

        # self.timer = 1.Timer(5, func)
        # timer.start()

    def ShowResult(self, str):
        print(str,end="")
        #self.lab_nlp.config(image=self.img_wakeup_zoomed)
        self.ShowResultStr.set(str)

    def MainLoop(self):
        self.window.mainloop()    