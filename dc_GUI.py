#!/usr/bin/env python3
#----------------
#Name: dc_GUI.py
#Version: 0.0.1
#Date: 2016-09-28
#----------------

import tkinter as tk
from tkinter import ttk
import subprocess
from time import strftime
from platform import system

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

def cli_msg(msg):
    print(msg)

def dc_run():
    hostsys = system()
    if hostsys == 'Windows':
        dc_out = subprocess.run(['cmd', '/C', 'dice_cup.py', '-d 6,3', '-g 3', '-q'], stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(['./dice_cup.py', '-d 6,3', '-g 3', '-q'], stdout=subprocess.PIPE)
    print(hostsys, dc_out)
    dc_print = str(dc_out).split('stdout=b')
    dc_print = dc_print[1].replace('\\n',' ').replace('\\r', ' ')
    return strftime("<%Y-%m-%dT%H:%M:%S> ")+dc_print.strip('\'\)')

def popup_wrn(msg):
    popup = tk.Tk()
    popup.wm_title("Warning")
    label = tk.Label(popup, text = msg, font = NORMAL_FONT)
    label.pack(pady = 10, padx= 30, side = "top", fill="x")
    button = tk.Button(popup, text = "Ok", command = popup.destroy)
    button.pack()
    popup.mainloop()

def tab_config(self):
    set_val = tk.IntVar()
    listbox = tk.Listbox(self)
    scrolly = tk.Scrollbar(self)
    scrolly.config(command = listbox.yview)
    scrolly.pack(side = "right", fill = "y")
    scrollx = tk.Scrollbar(self)
    scrollx.config(command = listbox.xview, orient = "horizontal")
    scrollx.pack(side = "bottom", fill = "x")
    listbox.config(yscrollcommand = scrolly.set, xscrollcommand = scrollx.set, bg = "ghost white")
    listbox.pack(fill = "both", expand = 1)
    entry = tk.Entry(self)
    entry.config(bg = "ghost white")
    entry.pack(fill = "x")
    rollbutton = tk.Button(self, text = "|--> Roll <--|",\
    command = lambda: (listbox.insert(tk.END, dc_run()), listbox.see(tk.END)))
    rollbutton.pack(side = "top", fill = "x")
    sbutton = tk.Checkbutton(self, text = "[Set]", indicatoron = 0, offvalue = 0, onvalue = 1,\
    variable = set_val, command = lambda: (cli_msg("The set button has been pressed, see below:"),\
    cli_msg(set_val.get())), selectcolor = "firebrick2")
    sbutton.pack(padx = 5, side = "left")
    button1 = tk.Button(self, text = "Preset 1", command = lambda: cli_msg("You clicked button 1!"))
    button1.pack(padx = 5, side = "left")
    button2 = tk.Button(self, text = "Preset 2", command = lambda: cli_msg("You clicked button 2!"))
    button2.pack(padx = 5, side = "left")
    button3 = tk.Button(self, text = "Preset 3", command = lambda: cli_msg("You clicked button 3!"))
    button3.pack(padx = 5, side = "left")
    button4 = tk.Button(self, text = "Preset 4", command = lambda: cli_msg("You clicked button 4!"))
    button4.pack(padx = 5, side = "left")
    button5 = tk.Button(self, text = "Preset 5", command = lambda: cli_msg("You clicked button 5!"))
    button5.pack(padx = 5, side = "left")
    button6 = tk.Button(self, text = "Preset 6", command = lambda: cli_msg("You clicked button 6!"))
    button6.pack(padx = 5, side = "left")
    button7 = tk.Button(self, text = "Preset 7", command = lambda: cli_msg("You clicked button 7!"))
    button7.pack(padx = 5, side = "left")
    button8 = tk.Button(self, text = "Preset 8", command = lambda: cli_msg("You clicked button 8!"))
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
        filemenu.add_command(label = "Import", command = lambda: popup_wrn("Not supported yet."))
        filemenu.add_command(label = "Export", command = lambda: popup_wrn("Not supported yet."))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = quit)
        
        settingsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        settingsmenu.add_command(label = "Option 1", command = lambda: popup_wrn("Not supported yet."))
        settingsmenu.add_command(label = "Option 2", command = lambda: popup_wrn("Not supported yet."))
        
        helpmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        helpmenu.add_command(label = "About", command = lambda: popup_wrn("Not supported yet."))
        menubar.add_cascade(label = "File", menu = filemenu)
        menubar.add_cascade(label = "Settings", menu = settingsmenu)
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

app = GUITest()
app.geometry("800x600")
app.mainloop()
