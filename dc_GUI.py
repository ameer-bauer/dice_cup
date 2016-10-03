#!/usr/bin/env python3
#----------------
#Name: dc_GUI.py
#Version: 0.0.2
#Date: 2016-09-30
#----------------

import tkinter as tk
from tkinter import ttk
import subprocess
from datetime import datetime
from platform import system

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
HOST_SYS = system()
WIN_DEFAULT = ['cmd', '/C', 'dice_cup.py', '-q']
NIX_DEFAULT = ['./dice_cup.py', '-q']

def cli_msg(msg):
    print(msg)

def dc_run(params):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params, stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params, stdout=subprocess.PIPE)
    now = datetime.now()
    print(dc_out)
    dc_print = str(dc_out).split('stdout=b')
    dc_print = dc_print[1].replace('\\n',' ').replace('\\r', ' ')
    return now.strftime("<%Y-%m-%dT%H:%M:%S.%f> ")+str(params)+' '+dc_print.strip('\')')

def popup_wrn(title, msg):
    popup = tk.Tk()
    popup.wm_title(title)
    label = tk.Label(popup, text = msg, font = NORMAL_FONT)
    label.pack(pady = 10, padx= 30, side = "top", fill="x")
    button = tk.Button(popup, text = "Ok", command = popup.destroy)
    button.pack()
    popup.geometry("300x100")
    popup.mainloop()

def tab_config(self):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    default_flags = "-d 6,3;-g 6"
    
    listbox = tk.Listbox(self)
    scrolly = tk.Scrollbar(self)
    scrolly.config(command = listbox.yview)
    scrolly.pack(side = "right", fill = "y")
    scrollx = tk.Scrollbar(self)
    scrollx.config(command = listbox.xview, orient = "horizontal")
    scrollx.pack(side = "bottom", fill = "x")
    listbox.config(yscrollcommand = scrolly.set, xscrollcommand = scrollx.set, bg = "alice blue")
    listbox.pack(fill = "both", expand = 1)
    
    entry = tk.Entry(self, textvariable = entry_val)
    entry.config(bg = "alice blue")
    entry.pack(fill = "x")
    entry_val.set(default_flags)
    
    rollbutton = tk.Button(self, text = "|--> Roll <--|",\
    command = lambda: (listbox.insert(tk.END, dc_run(entry_val.get().split(';'))),\
    listbox.see(tk.END)))
    rollbutton.pack(side = "top", fill = "x")
    
    sbutton = tk.Checkbutton(self, text = "[Set]", indicatoron = 0, offvalue = 0, onvalue = 1,\
    variable = set_val, command = lambda: (cli_msg("[Set] button press, state = "+str(set_val.get()))),\
    selectcolor = "firebrick2")
    sbutton.pack(padx = 5, side = "left")
    
    button1 = tk.Button(self, text = "Preset 1",\
    command = lambda: (cli_msg("Button press: Preset 1"), entry_val.set("Preset 1")))
    button1.pack(padx = 5, side = "left")
    
    button2 = tk.Button(self, text = "Preset 2",\
    command = lambda: (cli_msg("Button press: Preset 2"), entry_val.set("Preset 2")))
    button2.pack(padx = 5, side = "left")
    
    button3 = tk.Button(self, text = "Preset 3",\
    command = lambda: (cli_msg("Button press: Preset 3"), entry_val.set("Preset 3")))
    button3.pack(padx = 5, side = "left")
    
    button4 = tk.Button(self, text = "Preset 4",\
    command = lambda: (cli_msg("Button press: Preset 4"), entry_val.set("Preset 4")))
    button4.pack(padx = 5, side = "left")
    
    button5 = tk.Button(self, text = "Preset 5",\
    command = lambda: (cli_msg("Button press: Preset 5"), entry_val.set("Preset 5")))
    button5.pack(padx = 5, side = "left")
    
    button6 = tk.Button(self, text = "Preset 6",\
    command = lambda: (cli_msg("Button press: Preset 6"), entry_val.set("Preset 6")))
    button6.pack(padx = 5, side = "left")
    
    button7 = tk.Button(self, text = "Preset 7",\
    command = lambda: (cli_msg("Button press: Preset 7"), entry_val.set("Preset 7")))
    button7.pack(padx = 5, side = "left")
    
    button8 = tk.Button(self, text = "Preset 8",\
    command = lambda: (cli_msg("Button press: Preset 8"), entry_val.set("Preset 8")))
    button8.pack(padx = 5, side = "left")

class GUITest(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "dc_GUI")
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        menubar = tk.Menu(container, relief = "flat")
        
        filemenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        filemenu.add_command(label = "Open...", command = lambda: popup_wrn("Open...", "Not supported yet."))
        filemenu.add_command(label = "Save As...", command = lambda: popup_wrn("Save As...", "Not supported yet."))
        filemenu.add_command(label = "Save", command = lambda: popup_wrn("Save", "Not supported yet."))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = quit)
        
        settingsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        settingsmenu.add_command(label = "Import...",\
        command = lambda: popup_wrn("Import...", "Not supported yet."))
        settingsmenu.add_command(label = "Export...",\
        command = lambda: popup_wrn("Export...", "Not supported yet."))
        settingsmenu.add_command(label = "Load Defaults",\
        command = lambda: popup_wrn("Load Defaults", "Not supported yet."))
        
        toolsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        toolsmenu.add_command(label = "Scratchpad",\
        command = lambda: popup_wrn("Scratchpad", "Not supported yet."))
        toolsmenu.add_command(label = "Formula Build",\
        command = lambda: popup_wrn("Formula Build", "Not supported yet."))
        
        helpmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        helpmenu.add_command(label = "About",\
        command = lambda: popup_wrn("About", "Not supported yet."))
        
        menubar.add_cascade(label = "File", menu = filemenu)
        menubar.add_cascade(label = "Settings", menu = settingsmenu)
        menubar.add_cascade(label = "Tools", menu = toolsmenu)
        menubar.add_cascade(label = "Help", menu = helpmenu)
        tk.Tk.config(self, menu = menubar)
        
        notebook = ttk.Notebook(container)
        note1 = ttk.Frame(notebook)
        note2 = ttk.Frame(notebook)
        note3 = ttk.Frame(notebook)
        note4 = ttk.Frame(notebook)
        note5 = ttk.Frame(notebook)
        notebook.add(note1, text='Ledger 1')
        tab_config(note1)
        notebook.add(note2, text='Ledger 2')
        tab_config(note2)
        notebook.add(note3, text='Ledger 3')
        tab_config(note3)
        notebook.add(note4, text='Ledger 4')
        tab_config(note4)
        notebook.add(note5, text='Ledger 5')
        tab_config(note5)
        notebook.pack(padx = 5, pady = 5, fill = "both", expand = 1)

print('Host OS:', HOST_SYS)
app = GUITest()
app.geometry("800x600")
app.mainloop()
