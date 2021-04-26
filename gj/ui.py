#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import gj


class UiApp(object):
    def __init__(self):
        self.topWindow = tk.Tk()
        self.actuator =  {}
        self.filename = ""
    
    def __openFileWindow(self):
        self.filename = filedialog.askopenfilename(title = "选择数据文件")

    #画图
    def __drawPc(self):
        if(len(self.filename)==0):
            tk.messagebox.showinfo('提醒', '选择一份数据文件')
        else:
            actuator = gj.Actuator(self.filename)
            actuator.readData()
            actuator.produceVocabSet()
            actuator.countYearWordNum()
            wordList = actuator.searchTopWords(30)
            actuator.dealData(wordList)
            fig = actuator.showData(wordList)
            
            canvas = FigureCanvasTkAgg(fig, master=self.topWindow)
            canvas.draw()

            toolbar = NavigationToolbar2Tk(canvas, self.topWindow, pack_toolbar=False)
            toolbar.update()

            canvas.mpl_connect(
                "key_press_event", lambda event: print(f"you pressed {event.key}"))
            canvas.mpl_connect("key_press_event", key_press_handler)

            # button = tk.Button(master=self.topWindow, text="Quit", command=self.topWindow.quit)
            # button.pack(side=tk.BOTTOM)
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def run(self):
        
        self.topWindow.title("小工具")
        self.topWindow.geometry("800x520+200+200")
        #创建菜单
        menubar = tk.Menu(self.topWindow)

        #选择文件的按钮
        menubar.add_command(label="文件", command=self.__openFileWindow)
        #作出统计图的按钮
        menubar.add_command(label="统计图", command=self.__drawPc)
        #添加退出按钮
        menubar.add_command(label="退出程序", command=self.topWindow.quit)

        self.topWindow.config(menu=menubar)
        self.topWindow.mainloop()
 
if __name__ == '__main__':
    app = UiApp()
    app.run()
    

