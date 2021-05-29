#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tkinter as tk
import tkinter.ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import gj


class UiApp(object):
    def __init__(self):
        self.topWindow = tk.Tk()
        self.actuator =  {}
        self.filename = ""
        #包含所有的frame
        self.frames = {}
        #存有含有输入框的frame参数
        self.framesParam = {}
    
    def __openFileWindow(self):
        self.filename = filedialog.askopenfilename(title = "选择数据文件")
        if(len(self.filename) == 0):
            return
        else:
            self.actuator = gj.Actuator(self.filename)

    def __showFrame(self,key,num=50):
        #调整界面的dax
        if(num > 50):
            self.topWindow.geometry("800x800+200+0")
        else:
            self.topWindow.geometry("800x520+200+200")
        for frameKey in self.frames:
            if frameKey == key:
                self.frames[frameKey].pack()
            else:
                self.frames[frameKey].pack_forget()
    #打开一个文件，并将文件中的内容写到text中
    def  __openReplaceWordFile(self,text):
        replaceWordFile = filedialog.askopenfilename(title="选择文件")
        if len(replaceWordFile) == 0:
            return
        else:
            #先清空文字，在插入文字
            text.delete(1.0,tk.END)
            with open(replaceWordFile, 'r') as replace:
                for line in replace.readlines():
                    text.insert(tk.INSERT,line)
    #打开文件夹
    def __openDirectory(self,entry):
        directory = filedialog.askdirectory(title="选择要存放的位置")
        if(len(directory) == 0):
            return
        else:
            entry.delete(0,tk.END)
            entry.insert(0,directory)

    def __createReplaceFrame(self):
        if("repalceWordFrame" in self.frames):
            return
        else:
        #调整界面
            replaceFrame = tk.Frame(self.topWindow)
            label1 = tk.Label(replaceFrame, text="输入替换后文字:")
            inputText1 = tk.Text(replaceFrame, width=80)
            button1 = tk.Button(replaceFrame, text="选择文件",
                                command=lambda: self.__openReplaceWordFile(inputText1))
            label1.grid(row=0, column=1)
            inputText1.grid(row=0, column=2)
            button1.grid(row=0, column=3)

            label2 = tk.Label(replaceFrame, text="替换后文件位置:")
            inputText2 = tk.Entry(replaceFrame, width=80)
            button2 = tk.Button(replaceFrame, text="存放位置",
                                command=lambda: self.__openDirectory(inputText2))

            button3 = tk.Button(replaceFrame, text="替换",
                                command=lambda: self.__replace(inputText1, inputText2))

            label2.grid(row=1, column=1)
            inputText2.grid(row=1, column=2)
            button2.grid(row=1, column=3)
            button3.grid(row=2, column=2)
            self.frames["repalceWordFrame"] = replaceFrame
            self.framesParam["repalceWordFrame"] = [inputText1,inputText2]
    #提取出输入内容,并组装成参数结构
    def __replace(self,inputWord,inputFileName):
        #拿到替换后文字和输出的文件位置
        #       outputFileName : 
        #       replaceWord : {}
        param = {}
        replaceWordStr = inputWord.get("1.0", "end")
        outputFileName = inputFileName.get()
        param["outputFileName"] = outputFileName
        param["replaceWord"] = self.__parseReplaceWord(replaceWordStr)

        #执行替换操作
        self.__checkFileName(lambda a:self.actuator.replace(a),param)
        

    def __checkFileName(self,fun,param):
        if(len(self.filename) == 0):
            self.filename = filedialog.askopenfilename(title="选择数据文件")
            self.actuator = gj.Actuator(self.filename)
        else:
            #执行回调
            fun(param)

    def __parseReplaceWord(self,replaceWordStr):
        wordList = replaceWordStr.split("\n")
        replaceWordDict = {}
        for word in wordList:
            words = word.split(":")
            if(len(words) == 2):
                replaceWordDict[words[0]] = words[1]
        return replaceWordDict


    def __replaceWord(self):      
        self.__createReplaceFrame()
        self.__showFrame("repalceWordFrame")

    def __createStatsFrame(self):
        if("statFrame" in self.frames):
            return
        else:
            statFrame = tk.Frame(self.topWindow)
            label1 = tk.Label(statFrame, text="统计结果存放地址:")
            inputText1 = tk.Entry(statFrame, width=80)
            button1 = tk.Button(statFrame, text="存放位置",
                                command=lambda: self.__openDirectory(inputText1))

            button2 = tk.Button(statFrame, text="统计", command=lambda: self.__stat(inputText1))

            label1.grid(row=0, column=1)
            inputText1.grid(row=0, column=2)
            button1.grid(row=0, column=3)
            button2.grid(row=1, column=2)
            self.frames["statFrame"] = statFrame
            self.framesParam["statFrame"] = [inputText1]
    def __stat(self, inputText):
        statResultFile = inputText.get()
        self.__checkFileName(lambda a: self.actuator.stat(a), statResultFile)

    def __stats(self):
        self.__createStatsFrame()
        self.__showFrame("statFrame")

    def __createImageFrame(self,num):
        imageFrame = tk.Frame(self.topWindow)

        self.actuator.statData()
        
        fig = self.actuator.showData(num)

        canvas = FigureCanvasTkAgg(fig, master=imageFrame)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(
            canvas, imageFrame, pack_toolbar=False)
        toolbar.update()

        canvas.mpl_connect(
            "key_press_event", lambda event: print("you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

        # button = tk.Button(master=self.topWindow, text="Quit", command=self.topWindow.quit)
        # button.pack(side=tk.BOTTOM)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.frames["imageFrame"] = imageFrame
    #画图
    def __drawPc(self):
        self.__createSelectImageFrame()
        self.__showFrame("selectImageFrame")
    def __createSelectImageFrame(self):
        if("selectImageFrame" in self.frames):
            return
        else:
            selectImageFrame = tk.Frame(self.topWindow)
            label1 = tk.Label(selectImageFrame, text="选择显示前几条单词:")
            combox1 = tk.ttk.Combobox(selectImageFrame, width=80)
            combox1.configure(state="readonly")


            combox1["values"] = [30,50,70]
            combox1.current(0)
            button1 = tk.Button(selectImageFrame, text="画图",
                                command=lambda: self.__checkFileName(lambda a: self.__draw(combox1),1))

            label1.grid(row=0, column=1)
            combox1.grid(row=0, column=2)
            button1.grid(row=1, column=2)
            self.frames["selectImageFrame"] = selectImageFrame
            self.framesParam["selectImageFrame"] = [combox1]
    def __draw(self,combox):
       num = int(combox.get())
       
       self.__createImageFrame(num)
       self.__showFrame("imageFrame",num)

    def run(self):
        
        self.topWindow.title("小工具")
        self.topWindow.geometry("800x520+200+200")
        #创建菜单
        menubar = tk.Menu(self.topWindow)

        #选择文件的按钮
        menubar.add_command(label="文件", command=self.__openFileWindow)
        #替换文件中的关键字
        menubar.add_command(label="替换文字", command=self.__replaceWord)
        #输出统计结果
        menubar.add_command(label="统计", command=self.__stats)
        #作出统计图的按钮
        menubar.add_command(label="画图", command=self.__drawPc)
        #添加退出按钮
        menubar.add_command(label="退出程序", command=self.topWindow.quit)

        self.topWindow.config(menu=menubar)
        self.topWindow.mainloop()
 
if __name__ == '__main__':
    app = UiApp()
    app.run()
    

