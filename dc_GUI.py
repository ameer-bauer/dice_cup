#!/usr/bin/env python3
#----------------
#Name: dc_GUI.py
#Version: 0.1.1
#Date: 2016-10-10
#----------------

import tkinter as tk
from tkinter import ttk
import subprocess
from datetime import datetime
from platform import system

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 9)
SMALL_FONT = ("Verdana", 8)
HOST_SYS = system()
WIN_DEFAULT = ['cmd', '/C', 'dice_cup.py']
NIX_DEFAULT = ['./dice_cup.py']
VERSION = "0.1.1"

def dc_run_q(params):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params+['-q'], stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params+['-q'], stdout=subprocess.PIPE)
    now = datetime.now()
    print(dc_out)
    dc_print = str(dc_out).split('stdout=')
    if HOST_SYS == 'Windows':
        dc_print = dc_print[1].replace('\\n', '  ').replace('\\r', '')
    else:
        dc_print = dc_print[1].replace('\\n', '  ')
    str_params = str(params).replace(' ', '').replace('\',\'', ';').replace('\'', '')
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+str_params+'  '+dc_print.strip('b\')')

def dc_run(params):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params, stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params, stdout=subprocess.PIPE)
    now = datetime.now()
    print(dc_out)
    dc_print = str(dc_out).split('stdout=')
    if HOST_SYS == 'Windows':
        dc_print = dc_print[1].replace('\\n', '\n').replace('\\r', '').replace('\\x08\\x08', '0')
    else:
        dc_print = dc_print[1].replace('\\n', '\n').replace('\\x08\\x08', '0')
    str_params = str(params).replace(' ', '').replace('\',\'', ';').replace('\'', '')
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+str_params+'\n'+dc_print.strip('b\')')+'\n'

def popup_wrn(title, msg):
    popup = tk.Toplevel()
    popup.wm_title(title)
    label = tk.Label(popup, text = msg)
    label.pack(pady = 10, padx= 30, side = "top", fill="x")
    button1 = tk.Button(popup, text = "Ok",  command = popup.destroy)
    button1.pack(pady = 5)
    popup.geometry("250x80")
    popup.mainloop()

def popup_get(title, msg):
    popup_val = tk.StringVar()
    popup = tk.Toplevel()
    popup.wm_title(title)
    label = tk.Label(popup, text = msg)
    label.pack(padx = 10, pady= 10, side = "top", fill="x")
    entry = tk.Entry(popup, textvariable = popup_val)
    entry.config(bg = "gray90")
    entry.pack(padx = 10, pady = 5, fill = "x")
    popup_val.set("Default")
    button1 = tk.Button(popup, text = "Ok",  command = lambda: print("Value: ", popup_val.get()))
    button1.pack(padx = 10, pady = 5, side = 'left')
    button2 = tk.Button(popup, text = "Close",  command = popup.destroy())
    button2.pack(padx = 10, pady = 5, side = 'right')
    #popup.geometry("250x100")
    popup.mainloop()

def formula_parse(param_str):
    foo = []
    if params_str.find('+') != -1:
        a = True
        v = params_str.split('+')
    if params_str.find('-') != -1:
        m = True
        w = params_str.split('+')
    if params_str.find('*') != -1:
        g = True
        x = params_str.split('+')
    if params_str.find('^') != -1:
        s = True
        y = params_str.split('+')
    if params_str.find('%') != -1:
        p = True
        z = params_str.split('+')
    if (not (a and m and g and s and p)) and (param_str.find('d') != -1):
        params = param_str.split('d')
    print("params:", params)
    return params

def ledger_config(self):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    default_flags = "-d6,3+4,1;-m2;-g6;-s2"
    key1 = ["Default"]
    b_names = ["One d4", "One d6", "One d8", "One d10", "One d12", "One d20", "One d100", \
    "Two Single d20s", "Two d20s Drop Low", "Two d20s Drop High"]
    preset1 = ["-d4,1"]
    preset2 = ["-d6,1"]
    preset3 = ["-d8,1"]
    preset4 = ["-d10,1"]
    preset5 = ["-d12,1"]
    preset6 = ["-d20,1"]
    preset7 = ["-d100,1"]
    preset8 = ["-d20,1;-g2"]
    preset9 = ["-d20,2;-L"]
    preset10 = ["-d20,2;-H"]
    
    def button_press(value):
        listbox.insert(tk.END, dc_run_q(value[0].split(';'))),\
        listbox.see(tk.END)
        listbox.select_clear(0,tk.END)
        listbox.select_set(tk.END)
        return value[0]
    
    def b_menu(self, name, value):
        button_popup = tk.Menu(self, tearoff = 0)
        button_popup.add_command(label = value[0],\
        command = lambda: button_press(value))
        button_popup.add_separator()
        button_popup.add_command(label = "Rename",\
        command = lambda: b_popup_rename(self, "Rename Button"))
        button_popup.add_command(label = "Revalue",\
        command = lambda: b_popup_revalue(button_popup, "Enter New Value", value, self))
        button_popup.add_command(label = "Cancel")
        if HOST_SYS == 'Darwin':
            self.bind("<Button-2>",\
            lambda e: button_popup.post(e.x_root, e.y_root))
        else:
            self.bind("<Button-3>",\
            lambda e: button_popup.post(e.x_root, e.y_root))
    
    def key_roll(k_in):
        k_in[0] = entry_val.get()
        listbox.insert(tk.END, dc_run_q(k_in[0].split(';'))),\
        listbox.see(tk.END)
        listbox.select_clear(0,tk.END)
        listbox.select_set(tk.END)
    
    def b_popup_rename(self, title):
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(self.cget("text"))
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), self.configure(text = popup_val.get())))
        button1.pack(pady = 5)
        #popup.geometry("250x80")
        popup.mainloop()
    
    def b_popup_revalue(self, title, value, parent):
        popup_val = tk.StringVar()
        def setvalue(self_in, value_in):
            value_in[0] = popup_val.get()
            self_in.entryconfigure(0, label = value[0])
            return value_in[0]
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(value[0])
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), print(parent.cget("text"), ": Revalue = "+setvalue(self, value))))
        button1.pack(pady = 5)
        #popup.geometry("200x80")
        popup.mainloop()
    
    listbox = tk.Listbox(self, height = 30)
    scrolly = tk.Scrollbar(self)
    scrolly.config(command = listbox.yview)
    scrolly.pack(side = "right", fill = "y")
    scrollx = tk.Scrollbar(self)
    scrollx.config(command = listbox.xview, orient = "horizontal")
    scrollx.pack(side = "bottom", fill = "x")
    listbox.config(yscrollcommand = scrolly.set, xscrollcommand = scrollx.set,  bg = "gray90")
    listbox.pack(fill = "both", expand = 1)
    
    entry = tk.Entry(self, textvariable = entry_val)
    entry.config(bg = "gray90")
    entry.bind("<Return>", lambda k: key_roll(key1))
    entry.pack(fill = "x")
    entry_val.set(default_flags)
    
    rollbutton = tk.Button(self, text = "[Formula Roll]", \
    command = lambda: key_roll(key1))
    rollbutton.pack(side = "top", fill = "x")
    
    button1 = tk.Button(self, text = b_names[0], \
    command = lambda: (print(button1.cget("text"), ": Button Press, Value = "+button_press(preset1))))
    button1.pack(side = "left")
    b_menu(button1, button1.cget("text"), preset1)
    
    button2 = tk.Button(self, text = b_names[1], \
    command = lambda: (print(button2.cget("text"), ": Button Press, Value = "+button_press(preset2))))
    button2.pack(side = "left")
    b_menu(button2, button2.cget("text"), preset2)
    
    button3 = tk.Button(self, text = b_names[2], \
    command = lambda: (print(button3.cget("text"), ": Button Press, Value = "+button_press(preset3))))
    button3.pack(side = "left")
    b_menu(button3, button3.cget("text"), preset3)
    
    button4 = tk.Button(self, text = b_names[3], \
    command = lambda: (print(button4.cget("text"), ": Button Press, Value = "+button_press(preset4))))
    button4.pack(side = "left")
    b_menu(button4, button4.cget("text"), preset4)
    
    button5 = tk.Button(self, text = b_names[4], \
    command = lambda: (print(button5.cget("text"), ": Button Press, Value = "+button_press(preset5))))
    button5.pack(side = "left")
    b_menu(button5, button5.cget("text"), preset5)
    
    button6 = tk.Button(self, text = b_names[5], \
    command = lambda: (print(button6.cget("text"), ": Button Press, Value = "+button_press(preset6))))
    button6.pack(side = "left")
    b_menu(button6, button6.cget("text"), preset6)
    
    button7 = tk.Button(self, text = b_names[6], \
    command = lambda: (print(button7.cget("text"), ": Button Press, Value = "+button_press(preset7))))
    button7.pack(side = "left")
    b_menu(button7, button7.cget("text"), preset7)
    
    button8 = tk.Button(self, text = b_names[7], \
    command = lambda: (print(button8.cget("text"), ": Button Press, Value = "+button_press(preset8))))
    button8.pack(side = "left")
    b_menu(button8, button8.cget("text"), preset8)
    
    button9 = tk.Button(self, text = b_names[8], \
    command = lambda: (print(button9.cget("text"), ": Button Press, Value = "+button_press(preset9))))
    button9.pack(side = "left")
    b_menu(button9, button9.cget("text"), preset9)
    
    button10 = tk.Button(self, text = b_names[9], \
    command = lambda: (print(button10.cget("text"), ": Button Press, Value = "+button_press(preset10))))
    button10.pack(side = "left")
    b_menu(button10, button10.cget("text"), preset10)

def journal_config(self):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    default_flags = "-d6,3+4,1;-m2;-g6;-s2"
    b_names = ["One d4", "One d6", "One d8", "One d10", "One d12", "One d20", "One d100", \
    "Two Single d20s", "Two d20s Drop Low", "Two d20s Drop High"]
    key1 = ["test"]
    preset1 = ["-d4,1"]
    preset2 = ["-d6,1"]
    preset3 = ["-d8,1"]
    preset4 = ["-d10,1"]
    preset5 = ["-d12,1"]
    preset6 = ["-d20,1"]
    preset7 = ["-d100,1"]
    preset8 = ["-d20,1;-g2"]
    preset9 = ["-d20,2;-L"]
    preset10 = ["-d20,2;-H"]
    
    def button_press(value):
        text.insert(tk.END, dc_run(value[0].split(';'))),\
        text.see(tk.END)
        return value[0]
    
    def b_menu(self, name, value):
        button_popup = tk.Menu(self, tearoff = 0)
        button_popup.add_command(label = value[0],\
        command = lambda: button_press(value))
        button_popup.add_separator()
        button_popup.add_command(label = "Rename",\
        command = lambda: b_popup_rename(self, "Rename Button"))
        button_popup.add_command(label = "Revalue", \
        command = lambda: b_popup_revalue(button_popup, "Enter New Value", value, self))
        button_popup.add_command(label = "Cancel")
        if HOST_SYS == 'Darwin':
            self.bind("<Button-2>",\
            lambda e: button_popup.post(e.x_root, e.y_root))
        else:
            self.bind("<Button-3>",\
            lambda e: button_popup.post(e.x_root, e.y_root))
    
    def key_roll(k_in):
        k_in[0] = entry_val.get()
        text.insert(tk.END, dc_run(k_in[0].split(';'))),\
        text.see(tk.END)
    
    def b_popup_rename(self, title):
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(self.cget("text"))
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), self.configure(text = popup_val.get())))
        button1.pack(pady = 5)
        #popup.geometry("250x80")
        popup.mainloop()
    
    def b_popup_revalue(self, title, value, parent):
        popup_val = tk.StringVar()
        def setvalue(self_in, value_in):
            value_in[0] = popup_val.get()
            self_in.entryconfigure(0, label = value[0])
            return value_in[0]
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(value[0])
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), print(parent.cget("text"), ": Revalue = "+setvalue(self, value))))
        button1.pack(pady = 5)
        #popup.geometry("200x80")
        popup.mainloop()
    
    text = tk.Text(self, height = 30)
    scrolly = tk.Scrollbar(self)
    scrolly.config(command = text.yview)
    scrolly.pack(side = "right", fill = "y")
    scrollx = tk.Scrollbar(self)
    scrollx.config(command = text.xview, orient = "horizontal")
    scrollx.pack(side = "bottom", fill = "x")
    text.config(yscrollcommand = scrolly.set, xscrollcommand = scrollx.set, bg = "gray90",\
    wrap = "word")
    text.pack(fill = "both", expand = 1)
    
    entry = tk.Entry(self, textvariable = entry_val)
    entry.config(bg = "gray90")
    entry.bind("<Return>", lambda k: key_roll(key1))
    entry.pack(fill = "x")
    entry_val.set(default_flags)
    
    rollbutton = tk.Button(self, text = "[Formula Roll]", \
    command = lambda: key_roll(key1))
    rollbutton.pack(side = "top", fill = "x")
    
    button1 = tk.Button(self, text = b_names[0], \
    command = lambda: (print(button1.cget("text"), ": Button Press, Value = "+button_press(preset1))))
    button1.pack(side = "left")
    b_menu(button1, button1.cget("text"), preset1)
    
    button2 = tk.Button(self, text = b_names[1], \
    command = lambda: (print(button2.cget("text"), ": Button Press, Value = "+button_press(preset2))))
    button2.pack(side = "left")
    b_menu(button2, button2.cget("text"), preset2)
    
    button3 = tk.Button(self, text = b_names[2], \
    command = lambda: (print(button3.cget("text"), ": Button Press, Value = "+button_press(preset3))))
    button3.pack(side = "left")
    b_menu(button3, button3.cget("text"), preset3)
    
    button4 = tk.Button(self, text = b_names[3], \
    command = lambda: (print(button4.cget("text"), ": Button Press, Value = "+button_press(preset4))))
    button4.pack(side = "left")
    b_menu(button4, button4.cget("text"), preset4)
    
    button5 = tk.Button(self, text = b_names[4], \
    command = lambda: (print(button5.cget("text"), ": Button Press, Value = "+button_press(preset5))))
    button5.pack(side = "left")
    b_menu(button5, button5.cget("text"), preset5)
    
    button6 = tk.Button(self, text = b_names[5], \
    command = lambda: (print(button6.cget("text"), ": Button Press, Value = "+button_press(preset6))))
    button6.pack(side = "left")
    b_menu(button6, button6.cget("text"), preset6)
    
    button7 = tk.Button(self, text = b_names[6], \
    command = lambda: (print(button7.cget("text"), ": Button Press, Value = "+button_press(preset7))))
    button7.pack(side = "left")
    b_menu(button7, button7.cget("text"), preset7)
    
    button8 = tk.Button(self, text = b_names[7], \
    command = lambda: (print(button8.cget("text"), ": Button Press, Value = "+button_press(preset8))))
    button8.pack(side = "left")
    b_menu(button8, button8.cget("text"), preset8)
    
    button9 = tk.Button(self, text = b_names[8], \
    command = lambda: (print(button9.cget("text"), ": Button Press, Value = "+button_press(preset9))))
    button9.pack(side = "left")
    b_menu(button9, button9.cget("text"), preset9)
    
    button10 = tk.Button(self, text = b_names[9], \
    command = lambda: (print(button10.cget("text"), ": Button Press, Value = "+button_press(preset10))))
    button10.pack(side = "left")
    b_menu(button10, button10.cget("text"), preset10)

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
        filemenu.add_command(label = "Open...", \
        command = lambda: popup_wrn("Open...", "Not supported yet."))
        filemenu.add_command(label = "Save As...", \
        command = lambda: popup_wrn("Save As...", "Not supported yet."))
        filemenu.add_command(label = "Save", \
        command = lambda: popup_wrn("Save", "Not supported yet."))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", \
        command = quit)
        
        settingsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        settingsmenu.add_command(label = "Import...", \
        command = lambda: popup_wrn("Import...", "Not supported yet."))
        settingsmenu.add_command(label = "Export...", \
        command = lambda: popup_wrn("Export...", "Not supported yet."))
        settingsmenu.add_command(label = "Load Defaults", \
        command = lambda: popup_wrn("Load Defaults", "Not supported yet."))
        
        toolsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        toolsmenu.add_command(label = "Scratchpad", \
        command = lambda: popup_wrn("Scratchpad", "Not supported yet."))
        toolsmenu.add_command(label = "Formula Build", \
        command = lambda: popup_wrn("Formula Build", "Not supported yet."))
        
        helpmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        helpmenu.add_command(label = "About", \
        command = lambda: popup_wrn("About", "dc_GUI version "+VERSION))
        
        menubar.add_cascade(label = "File",  menu = filemenu)
        menubar.add_cascade(label = "Settings",  menu = settingsmenu)
        menubar.add_cascade(label = "Tools",  menu = toolsmenu)
        menubar.add_cascade(label = "Help",  menu = helpmenu)
        tk.Tk.config(self, menu = menubar)
        
        #style = ttk.Style()
        #style.configure('.', font = NORMAL_FONT) #Change all default ttk styles
        notebook = ttk.Notebook(container)
        note1 = ttk.Frame(notebook)
        note2 = ttk.Frame(notebook)
        note3 = ttk.Frame(notebook)
        note4 = ttk.Frame(notebook)
        note5 = ttk.Frame(notebook)
        note6 = ttk.Frame(notebook)
        note7 = ttk.Frame(notebook)
        note8 = ttk.Frame(notebook)
        note9 = ttk.Frame(notebook)
        note10 = ttk.Frame(notebook)
        
        def n_popup_get(title):
            popup_val = tk.StringVar()
            popup = tk.Toplevel()
            popup.wm_title(title)
            entry = tk.Entry(popup, textvariable = popup_val)
            entry.config(bg = "gray90")
            entry.pack(padx = 20, pady = 10, fill = "x")
            popup_val.set(notebook.tab(notebook.select(), 'text'))
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), notebook.tab(notebook.select(), text = popup_val.get())))
            button1.pack(pady = 5)
            #popup.geometry("200x80")
            popup.mainloop()
        
        note_popup = tk.Menu(notebook, tearoff = 0)
        note_popup.add_command(label = "Rename",\
        command = lambda: n_popup_get("Rename Tab"))
        #note_popup.add_separator()
        note_popup.add_command(label = "Cancel")
        if HOST_SYS == 'Darwin':
            notebook.bind("<Button-2>",\
            lambda n: note_popup.post(n.x_root, n.y_root))
        else:
            notebook.bind("<Button-3>",\
            lambda n: note_popup.post(n.x_root, n.y_root))
        
        notebook.add(note1, text = "Ledger 1")
        ledger_config(note1)
        
        notebook.add(note2, text = "Ledger 2")
        ledger_config(note2)
        
        notebook.add(note3, text = "Ledger 3")
        ledger_config(note3)
        
        notebook.add(note4, text = "Ledger 4")
        ledger_config(note4)
        
        notebook.add(note5, text = "Ledger 5")
        ledger_config(note5)
        
        notebook.add(note6, text = "Journal 1")
        journal_config(note6)
        
        notebook.add(note7, text = "Journal 2")
        journal_config(note7)
        
        notebook.add(note8, text = "Journal 3")
        journal_config(note8)
        
        notebook.add(note9, text = "Journal 4")
        journal_config(note9)
        
        notebook.add(note10, text = "Journal 5")
        journal_config(note10)
        
        notebook.pack(fill = "both", expand = 1)

print('Host OS:', HOST_SYS)
app = GUITest()
#app.geometry("1000x650")
app.mainloop()
