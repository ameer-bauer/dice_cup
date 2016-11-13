#!/usr/bin/env python3
#----------------
#Name: dc_GUI.py
#Version: 0.1.6
#Date: 2016-11-12
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
VERSION = "0.1.6"

def dc_run_q(params):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params+['-q'], stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params+['-q'], stdout=subprocess.PIPE)
    now = datetime.now()
    str_dc_out = str(dc_out)
    str_params = str(params).replace(' ', '').replace('\',\'', ';').replace('\'', '')
    if str_dc_out.find('returncode=0') == -1:
        print('\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n',dc_out, sep = '\n')
        return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+str_params+'  '+\
        "!!ERROR!!  Please check your \'Roll Formula\' syntax."
    dc_print = str_dc_out.split('stdout=')
    if HOST_SYS == 'Windows':
        dc_print = dc_print[1].replace('\\n', '  ').replace('\\r', '')
    else:
        dc_print = dc_print[1].replace('\\n', '  ')
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+str_params+'  '+dc_print.strip('b\')')[:2048]

def dc_run(params):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params, stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params, stdout=subprocess.PIPE)
    now = datetime.now()
    str_dc_out = str(dc_out)
    str_params = str(params).replace(' ', '').replace('\',\'', ';').replace('\'', '')
    dc_print = str(dc_out).split('stdout=')
    if str_dc_out.find('returncode=0') == -1:
        print('\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n', dc_out, sep = '\n')
        return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+str_params+'\n'+\
        "!!ERROR!!  Please check your \'Roll Formula\' syntax.\n\n"
    if HOST_SYS == 'Windows':
        dc_print = dc_print[1].replace('\\n', '\n').replace('\\r', '').replace('\\x08\\x08', '0')
    else:
        dc_print = dc_print[1].replace('\\n', '\n').replace('\\x08\\x08', '0')
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

def popup_rfhlp(title):
    popup = tk.Toplevel()
    popup.wm_title(title)
    text = tk.Text(popup, width = 80, height = 30)
    scroll = tk.Scrollbar(popup)
    text.insert(tk.END, "A \'Roll Formula\' is a flexible input mechanism for simulating various dice\n")
    text.insert(tk.END, "rolls.  It is designed to be intuitive and predictable in structure.  Below you\n")
    text.insert(tk.END, "will find the syntactical and variable definitions along with some examples.\n")
    text.insert(tk.END, "Please note that verbose error messages are printed to the CLI window; if your\n")
    text.insert(tk.END, "input syntax has an error.  Roll Formulae have a maximum size of 100 characters.\n")
    text.insert(tk.END, "At least one combination of dice must be defined to form a valid Roll Formula.\n\n")
    text.insert(tk.END, "SYNTAX\n  s^ g* c1dt1 ±c2dt2 ... ±cndtn ±m ±p% <±u >±l L|H I\n\n")
    text.insert(tk.END, "  NOTE: All input variables are either INTEGERS, or FLAGS which can be\n")
    text.insert(tk.END, "        present or omitted; empty spaces are optional.\n\n")
    text.insert(tk.END, "  INTEGERS\n    s = dice Set [POSITIVE ONLY]\n    g = dice Group [POSITIVE ONLY]\n")
    text.insert(tk.END, "    c1, c2, ... cn = the Combination of corresponding die Types to roll\n")
    text.insert(tk.END, "    t1, t2, ... tn = the Type(s) of dice to roll [POSITIVE ONLY]\n")
    text.insert(tk.END, "        NOTE: c1dt1 can not be preceded by a \'+\' or a \'-\' symbol.\n")
    text.insert(tk.END, "    m = Modifier\n    p = Percentage\n    u = Upper Boundary\n    l = Lower Boundary\n\n")
    text.insert(tk.END, "  FLAGS\n    L = drop the Lowest c1dt1 single die roll in the combination\n")
    text.insert(tk.END, "    H = drop the Highest c1dt1 single die roll in the combination\n")
    text.insert(tk.END, "    I = include Statistical Information\n")
    text.insert(tk.END, "        NOTE: Either L or H can be set, but not both.\n\n")
    text.insert(tk.END, "EXAMPLES\n  1) Roll three six-sided dice.\n     Roll Formula Syntax: 3d6\n\n")
    text.insert(tk.END, "  2) Roll two Groups of three six-sided dice, plus one four-sided die, and\n")
    text.insert(tk.END, "     subtract a modifier of five.\n")
    text.insert(tk.END, "     Roll Formula Syntax: 2*3d6+1d4-5\n\n")
    text.insert(tk.END, "  3) Roll five Sets of six Groups of four six-sided dice, add a Percentage of\n")
    text.insert(tk.END, "     fifteen (15%), drop the lowest single six-sided die from each Group, and\n")
    text.insert(tk.END, "     include Statistical Information.\n     Roll Formula Syntax: 5^6*4d6+15%LI\n\n")
    text.insert(tk.END, "  4) Roll twenty Groups of ten eight-sided dice, minus a Modifier of seventeen,\n")
    text.insert(tk.END, "     an upper boundary of sixty five, a lower boundary of negative ten, and drop\n")
    text.insert(tk.END, "     the highest single eight-sided die from each dice Group.\n")
    text.insert(tk.END, "     Roll Formula Syntax: 20*10d8-17<65>-10H\n\n")
    scroll.config(command = text.yview)
    scroll.pack(side = "right", fill = "y")
    text.config(state = "disabled", yscrollcommand = scroll.set)
    text.pack(padx= 5, side = "top", fill="x")
    button1 = tk.Button(popup, text = "OK",  command = popup.destroy)
    button1.pack(pady = 5)
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
    button1 = tk.Button(popup, text = "Ok", \
    command = lambda: (popup.destroy(), print("Value: ", popup_val.get())))
    button1.pack(pady = 5)
    #popup.geometry("250x100")
    popup.mainloop()

def formula_get(title, msg):
    popup_val = tk.StringVar()
    popup = tk.Toplevel()
    popup.wm_title(title)
    label = tk.Label(popup, text = msg)
    label.pack(padx = 10, pady= 10, side = "top", fill="x")
    entry = tk.Entry(popup, textvariable = popup_val)
    entry.config(bg = "gray90")
    entry.bind("<Return>", \
    lambda k: (popup.destroy(), formula_parse(popup_val.get())))
    entry.pack(padx = 20, pady = 5, fill = "x")
    popup_val.set("2^5*3d6")
    button1 = tk.Button(popup, text = "Ok", \
    command = lambda: (popup.destroy(), formula_parse(popup_val.get()[:150])))
    button1.pack(pady = 5)
    popup.geometry("250x110")
    popup.mainloop()

def formula_parse(params_in):
    ###########################################################################
    #SYNTAX
    #  s^ g* c1dt1 ±c2dt2 ... ±cndtn ±m ±p% <±u >±l L|H I
    #
    #NOTE: All input variables are either INTEGERS, or FLAGS which can be
    #      present or omitted.
    #
    #  INTEGERS
    #    s = dice Set [POSITIVE ONLY]
    #    g = dice Group [POSITIVE ONLY]
    #    c1, c2, ... cn = the Number/Combo of corresponding die Types to roll
    #    t1, t2, ... tn = the Type(s) of dice to roll [POSITIVE ONLY]
    #    m = Modifier
    #    p = Percentage
    #    u = Upper Boundary
    #    l = Lower Boundary
    #
    #  FLAGS
    #    L = drop the Lowest c1dt1 single die roll in the combination
    #    H = drop the Highest c1dt1 single die roll in the combination
    #        NOTE: Either L or H can be set, but not both.
    #    I = include Statistical Information
    #
    #NOTE: See the dice_cup help page for detailed definitions and examples.
    ###########################################################################
    #NOTE: formula_parse input is limited to 100 characters.
    ###########################################################################
    #EXAMPLES
    #--Roll three six-sided dice:
    #    3d6
    #
    #--Roll two Groups of three six-sided dice, plus one
    #  four-sided die, and subtract a modifier of five:
    #    2*3d6+1d4-5
    #
    #--Roll five Sets of six Groups of four six-sided dice, add a Percentage of
    #  fifteen (15%), drop the lowest single six-sided die from each Group, and
    #  include Statistical Information:
    #    5^6*4d6+15%LI
    #
    #--Roll twenty Groups of ten eight-sided dice, minus a Modifier of
    #  seventeen, an upper boundary of sixty five, a lower boundary of negative
    #  ten, and drop the highest single eight-sided die from each dice Group:
    #    20*10d8-17<65>-10H
    ###########################################################################
    params = []
    params_str = params_in.replace(' ', '')[:100]#Strip spaces and limit input
    error_blk = "\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!"
    error_str = "ERROR"
    error_cli = "Please verify the input Roll Formula's syntax.\n"
    
    d = True
    s = False
    g = False
    p = False
    l = False
    u = False
    lu = False
    ul = False
    L = False
    H = False
    I = False
    
    def die_parse(str_in):
        d_str = ""
        z_tmp = []
        first_run = True
        dp = False
        dm = False
        mp = False
        mm = False
        if (str_in[0] == '+' or str_in[0] == '-'):
            return "ERROR:"+str_in
        if '+' in str_in:#Positive Modifier handling
            dp = True
            z_add_m = str_in.split('+')
            if ('d' not in z_add_m[-1]) and (z_add_m[-1].isnumeric()):
                mp = True
                print("Roll Formula: Modifier Defined")
                params.append('-m'+z_add_m[-1])
        if '-' in str_in:#Negative Modifier handling
            dm = True
            z_sub_m = str_in.split('-')
            if ('d' not in z_sub_m[-1]) and (z_sub_m[-1].isnumeric()):
                mm = True
                print("Roll Formula: Modifier Defined")
                params.append('-m-'+z_sub_m[-1])
        if dp:
            if mp:
                z_add = z_add_m[:-1]
            elif mm:
                z_add = z_sub_m[:-1]
            else:
                z_add = z_add_m
            for a in z_add:
                if 'd' in a:
                    z_tmp = a.split('d', maxsplit = 1)
                    if z_tmp[0].isnumeric() and z_tmp[1].isnumeric():
                        if first_run:#Assume first dice combo is positive
                            d_str += z_tmp[1]+','+z_tmp[0]
                            first_run = False
                        else:
                            d_str += '+'+z_tmp[1]+','+z_tmp[0]
                    elif z_tmp[0].isnumeric() and ('-' in z_tmp[1]):
                        z_tmp_s = z_tmp[1].split('-', maxsplit = 1)
                        if z_tmp_s[0].isnumeric():
                            if first_run:
                                d_str += z_tmp_s[0]+','+z_tmp[0]
                                first_run = False
                            else:
                                d_str += '+'+z_tmp_s[0]+','+z_tmp[0]
                        else:
                            return "ERROR:"+str_in
                    else:
                        return "ERROR:"+str_in
        if dm:
            if mp:
                z_sub = z_add_m[:-1]
            elif mm:
                z_sub = z_sub_m[:-1]
            else:
                z_sub = z_sub_m
        if not (dp or dm):
            z_add = str_in.split('d')
            if z_add[0].isnumeric() and z_add[1].isnumeric():
                d_str += z_add[1]+','+z_add[0]
            else:
                return "ERROR:"+str_in
        return d_str
    
    #Initial sanity check
    if 'd' not in params_str:
        d = False
        print(error_blk)
        print("Roll Formula Syntax Error:", params_str)
        print("No \'Dice Combination\' is defined within the Roll Formula.")
        print(error_cli)
        return error_str
    
    #Statistical flag handling
    if 'I' in params_str:
        I = True
        params_str_I = params_str.replace('I', '')
        params.append('-i')
        print("Roll Formula: Statistical Information Enabled")
    
    #Drop Lowest handling
    if 'L' in params_str:
        L = True
        if I:
            params_str_L = params_str_I.replace('L', '')
        else:
            params_str_L = params_str.replace('L', '')
        params.append('-L')
        print("Roll Formula: Drop Lowest Enabled")
    
    #Drop Highest handling
    if 'H' in params_str:
        if not L:
            H = True
            if I:
                params_str_H = params_str_I.replace('H', '')
            else:
                params_str_H = params_str.replace('H', '')
            params.append('-H')
            print("Roll Formula: Drop Highest Enabled")
        else:
            print(error_blk)
            print("Roll Formula Syntax Error:", params_str)
            print("Both \'Drop Lowest\' and \'Drop Highest\' flags are enabled.")
            print("Please choose either the \'Drop Lowest\' or \'Drop Highest\' flag.")
            print(error_cli)
            return error_str
    
    #Upper Bound and Lower Bound handling combo 1
    if params_str.rfind('>') > params_str.rfind('<'):#<u >l syntax order
        ul = True
        l = True
        if L:
            lb = params_str_L.rsplit('>', maxsplit = 1)
        elif H:
            lb = params_str_H.rsplit('>', maxsplit = 1)
        elif I:
            lb = params_str_I.rsplit('>', maxsplit = 1)
        else:
            lb = params_str.rsplit('>', maxsplit = 1)
        if '+' in lb[1]:
            lbv = lb[1].rsplit('+', maxsplit = 1)
            if lbv[1].isnumeric():
                params.append('-l'+lbv[1])
            else:
                print(error_blk)
                print("Roll Formula \'Lower Boundary\' Syntax Error:", '>+'+lbv[1])
                print(error_cli)
                return error_str
        elif '-' in lb[1]:
            lbv = lb[1].rsplit('-', maxsplit = 1)
            if lbv[1].isnumeric():
                params.append('-l-'+lbv[1])
            else:
                print(error_blk)
                print("Roll Formula \'Lower Boundary\' Syntax Error:", '>-'+lbv[1])
                print(error_cli)
                return error_str
        elif lb[1].isnumeric():#Assume positive number
            params.append('-l'+lb[1])
        else:
            print(error_blk)
            print("Roll Formula \'Lower Boundary\' Syntax Error:", '>'+lb[1])
            print(error_cli)
            return error_str
        print("Roll Formula: Lower Boundary Defined")
        if '<' in params_str:
            u = True
            ub = lb[0].rsplit('<', maxsplit = 1)
            if '+' in ub[1]:
                ubv = ub[1].rsplit('+', maxsplit = 1)
                if ubv[1].isnumeric():
                    params.append('-u'+ubv[1])
                else:
                    print(error_blk)
                    print("Roll Formula \'Upper Boundary\' Syntax Error:", '<+'+ubv[1])
                    print(error_cli)
                    return error_str
            elif '-' in ub[1]:
                ubv = ub[1].rsplit('-', maxsplit = 1)
                if ubv[1].isnumeric():
                    params.append('-u-'+ubv[1])
                else:
                    print(error_blk)
                    print("Roll Formula \'Upper Boundary\' Syntax Error:", '<-'+ubv[1])
                    print(error_cli)
                    return error_str
            elif ub[1].isnumeric():#Assume positive number
                params.append('-u'+ub[1])
            else:
                print(error_blk)
                print("Roll Formula \'Upper Boundary\' Syntax Error:", '<'+ub[1])
                print(error_cli)
                return error_str
            print("Roll Formula: Upper Boundary Defined")
    
    #Upper Bound and Lower Bound handling combo 2
    if params_str.rfind('>') < params_str.rfind('<'):#>l <u syntax order
        lu = True
        u = True
        if L:
            ub = params_str_L.rsplit('<', maxsplit = 1)
        elif H:
            ub = params_str_H.rsplit('<', maxsplit = 1)
        elif I:
            ub = params_str_I.rsplit('<', maxsplit = 1)
        else:
            ub = params_str.rsplit('<', maxsplit = 1)
        if '+' in ub[1]:
            ubv = ub[1].rsplit('+', maxsplit = 1)
            if ubv[1].isnumeric():
                params.append('-u'+ubv[1])
            else:
                print(error_blk)
                print("Roll Formula \'Upper Boundary\' Syntax Error:", '<+'+ubv[1])
                print(error_cli)
                return error_str
        elif '-' in ub[1]:
            ubv = ub[1].rsplit('-', maxsplit = 1)
            if ubv[1].isnumeric():
                params.append('-u-'+ubv[1])
            else:
                print(error_blk)
                print("Roll Formula \'Upper Boundary\' Syntax Error:", '<-'+ubv[1])
                print(error_cli)
                return error_str
        elif ub[1].isnumeric():#Assume positive number
            params.append('-u'+ub[1])
        else:
            print(error_blk)
            print("Roll Formula \'Upper Boundary\' Syntax Error:", '<'+ub[1])
            print(error_cli)
            return error_str
        print("Roll Formula: Upper Boundary Defined")
        if '>' in params_str:
            l = True
            lb = ub[0].rsplit('>', maxsplit = 1)
            if '+' in lb[1]:
                lbv = lb[1].rsplit('+', maxsplit = 1)
                if lbv[1].isnumeric():
                    params.append('-l'+lbv[1])
                else:
                    print(error_blk)
                    print("Roll Formula \'Lower Boundary\' Syntax Error:", '>+'+lbv[1])
                    print(error_cli)
                    return error_str
            elif '-' in lb[1]:
                lbv = lb[1].rsplit('-', maxsplit = 1)
                if lbv[1].isnumeric():
                    params.append('-l-'+lbv[1])
                else:
                    print(error_blk)
                    print("Roll Formula \'Lower Boundary\' Syntax Error:", '>-'+lbv[1])
                    print(error_cli)
                    return error_str
            elif lb[1].isnumeric():#Assume positive number
                params.append('-l'+lb[1])
            else:
                print(error_blk)
                print("Roll Formula \'Lower Boundary\' Syntax Error:", '>'+lb[1])
                print(error_cli)
                return error_str
            print("Roll Formula: Lower Boundary Defined")
    
    #Percentage handling
    if '%' in params_str:
        p = True
        if (ul and u) or (lu and not l):
            v = ub[0].rsplit('%', maxsplit = 1)
        elif (lu and l) or (ul and not u):
            v = lb[0].rsplit('%', maxsplit = 1)
        elif L:
            v = params_str_L.rsplit('%', maxsplit = 1)
        elif H:
            v = params_str_H.rsplit('%', maxsplit = 1)
        elif I:
            v = params_str_I.rsplit('%', maxsplit = 1)
        else:
            v = params_str.rsplit('%', maxsplit = 1)
        if v[0].rfind('+') > v[0].rfind('-'):
            w = v[0].rsplit('+', maxsplit = 1)
            if w[1].isnumeric():
                params.append('-p'+w[1])
            else:
                print(error_blk)
                print("Roll Formula \'Percentage\' Syntax Error:", '+'+w[1]+'%')
                print(error_cli)
                return error_str
        elif v[0].rfind('+') < v[0].rfind('-'):
            w = v[0].rsplit('-', maxsplit = 1)
            if w[1].isnumeric():
                params.append('-p-'+w[1])
            else:
                print(error_blk)
                print("Roll Formula \'Percentage\' Syntax Error:", '-'+w[1]+'%')
                print(error_cli)
                return error_str
        else:
            print(error_blk)
            print("Roll Formula \'Percentage\' Syntax Error:", v[0]+'%')
            print(error_cli)
            return error_str
        print("Roll Formula: Percentage Modifier Defined")
    
    #Set handling
    if '^' in params_str:
        s = True
        if p:
            y = w[0].split('^', maxsplit = 1)
        elif (ul and u) or (lu and not l):
            y = ub[0].split('^', maxsplit = 1)
        elif (lu and l) or (ul and not u):
            y = lb[0].split('^', maxsplit = 1)
        elif L:
            y = params_str_L.split('^', maxsplit = 1)
        elif H:
            y = params_str_H.split('^', maxsplit = 1)
        elif I:
            y = params_str_I.split('^', maxsplit = 1)
        else:
            y = params_str.split('^', maxsplit = 1)
        if y[0].isnumeric():
            params.append('-s'+y[0])
            print("Roll Formula: Dice Set Defined")
        else:
            print(error_blk)
            print("Roll Formula \'Set\' Syntax Error:", y[0]+'^')
            print(error_cli)
            return error_str
    
    #Group handling
    if '*' in params_str:
        g = True
        if s:
            x = y[1].split('*', maxsplit = 1)
        elif p:
            x = w[0].split('*', maxsplit = 1)
        elif (ul and u) or (lu and not l):
            x = ub[0].split('*', maxsplit = 1)
        elif (lu and l) or (ul and not u):
            x = lb[0].split('*', maxsplit = 1)
        elif L:
            x = params_str_L.split('*', maxsplit = 1)
        elif H:
            x = params_str_H.split('*', maxsplit = 1)
        elif I:
            x = params_str_I.split('*', maxsplit = 1)
        else:
            x = params_str.split('*', maxsplit = 1)
        if x[0].isnumeric():
            params.append('-g'+x[0])
            print("Roll Formula: Dice Group Defined")
        else:
            print(error_blk)
            print("Roll Formula \'Group\' Syntax Error:", x[0]+'*')
            print(error_cli)
            return error_str
    
    #Dice and Modifier handling
    if d:
        if g:
            z = die_parse(x[1])
        elif s:
            z = die_parse(y[1])
        elif p:
            z = die_parse(w[0])
        elif (ul and u) or (lu and not l):
            z = die_parse(ub[0])
        elif (lu and l) or (ul and not u):
            z = die_parse(lb[0])
        elif L:
            z = die_parse(params_str_L)
        elif H:
            z = die_parse(params_str_H)
        elif I:
            z = die_parse(params_str_I)
        else:
            z = die_parse(params_str)
        if "ERROR" in z:
            z_err = z.split(':', maxsplit = 1)
            print(error_blk)
            print("Roll Formula \'Dice Combination\' Syntax Error:", z_err[1])
            if (z_err[1][0] == '+') or (z_err[1][0] == '-'):
                print("The first \'Dice Combination\' can not be preceded by a \'+\' or \'-\' symbol.")
            print(error_cli)
            return error_str
        else:
            print("Roll Formula: Dice Combination Defined")
            params.append('-d'+z)
    
    print("Parsed dice_cup Parameter List:", params)
    return params

def ledger_config(self):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    default_flags = "-d6,3+4,1;-m2;-g6;-s2"
    b_names = ["1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100", \
    "2 Single 1d20s", "2d20 Drop Low", "2d20 Drop High"]
    b_presets = [["-d4,1"], ["-d6,1"], ["-d8,1"], ["-d10,1"], ["-d12,1"], \
    ["-d20,1"], ["-d100,1"], ["-d20,1;-g2"], ["-d20,2;-L"], ["-d20,2;-H"]]
    
    def button_press(value):
        listbox.insert(tk.END, dc_run_q(value[0].split(';'))),\
        listbox.see(tk.END)
        listbox.select_clear(0,tk.END)
        listbox.select_set(tk.END)
        return value[0]
    
    def b_menu(self, name, value):
        button_rc_popup = tk.Menu(self, tearoff = 0)
        button_rc_popup.add_command(label = value[0],\
        command = lambda: button_press(value))
        button_rc_popup.add_separator()
        button_rc_popup.add_command(label = "Rename",\
        command = lambda: b_popup_rename(self, "Rename Button"))
        button_rc_popup.add_command(label = "Revalue",\
        command = lambda: b_popup_revalue(button_rc_popup, "Enter New Value", value, self))
        button_rc_popup.bind("<Leave>", lambda b: button_rc_popup.unpost())
        if HOST_SYS == 'Darwin':
            self.bind("<Button-2>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
        else:
            self.bind("<Button-3>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
    
    def formula_roll():
        k_in = ["Test"]
        str_in = entry_val.get()
        k_in[0] = str_in.replace(' ', '') #Strip spaces out
        listbox.insert(tk.END, dc_run_q(k_in[0].split(';'))),\
        listbox.see(tk.END)
        listbox.select_clear(0,tk.END)
        listbox.select_set(tk.END)
        return k_in[0]
    
    def b_popup_rename(self, title):
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.bind("<Return>", \
        lambda k: (popup.destroy(), self.configure(text = popup_val.get()[:20])))
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(self.cget("text"))
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), self.configure(text = popup_val.get()[:20])))
        button1.pack(pady = 5)
        #popup.geometry("250x80")
        popup.mainloop()
    
    def b_popup_revalue(self, title, value, parent):
        popup_val = tk.StringVar()
        def setvalue(self_in, value_in):
            str_in = popup_val.get()
            value_in[0] = str_in.replace(' ', '') #Strip spaces out
            self_in.entryconfigure(0, label = value[0])
            return value_in[0]
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.bind("<Return>", \
        lambda k: (popup.destroy(), print(parent.cget("text")+',', "Revalue = "+setvalue(self, value))))
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(value[0])
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), print(parent.cget("text")+',', "Revalue = "+setvalue(self, value))))
        button1.pack(pady = 5)
        #popup.geometry("200x80")
        popup.mainloop()
    
    listbox = tk.Listbox(self, width = 90, height = 30)
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
    entry.bind("<Return>", lambda k: print("Keyboard Input: Execute Roll Formula, Value =", formula_roll()))
    entry.pack(fill = "x")
    entry_val.set(default_flags)
    
    rollbutton = tk.Button(self, text = "[Execute Roll Formula]", \
    command = lambda: print("Button Press: [Execute Roll Formula], Value =", formula_roll()))
    rollbutton.pack(side = "top", fill = "x")
    
    button1 = tk.Button(self, text = b_names[0], \
    command = lambda: (print("Button Press:", button1.cget("text")+',', "Value = "+button_press(b_presets[0]))))
    button1.pack(side = "left")
    b_menu(button1, button1.cget("text"), b_presets[0])
    
    button2 = tk.Button(self, text = b_names[1], \
    command = lambda: (print("Button Press:", button2.cget("text")+',', "Value = "+button_press(b_presets[1]))))
    button2.pack(side = "left")
    b_menu(button2, button2.cget("text"), b_presets[1])
    
    button3 = tk.Button(self, text = b_names[2], \
    command = lambda: (print("Button Press:", button3.cget("text")+',', "Value = "+button_press(b_presets[2]))))
    button3.pack(side = "left")
    b_menu(button3, button3.cget("text"), b_presets[2])
    
    button4 = tk.Button(self, text = b_names[3], \
    command = lambda: (print("Button Press:", button4.cget("text")+',', "Value = "+button_press(b_presets[3]))))
    button4.pack(side = "left")
    b_menu(button4, button4.cget("text"), b_presets[3])
    
    button5 = tk.Button(self, text = b_names[4], \
    command = lambda: (print("Button Press:", button5.cget("text")+',', "Value = "+button_press(b_presets[4]))))
    button5.pack(side = "left")
    b_menu(button5, button5.cget("text"), b_presets[4])
    
    button6 = tk.Button(self, text = b_names[5], \
    command = lambda: (print("Button Press:", button6.cget("text")+',', "Value = "+button_press(b_presets[5]))))
    button6.pack(side = "left")
    b_menu(button6, button6.cget("text"), b_presets[5])
    
    button7 = tk.Button(self, text = b_names[6], \
    command = lambda: (print("Button Press:", button7.cget("text")+',', "Value = "+button_press(b_presets[6]))))
    button7.pack(side = "left")
    b_menu(button7, button7.cget("text"), b_presets[6])
    
    button8 = tk.Button(self, text = b_names[7], \
    command = lambda: (print("Button Press:", button8.cget("text")+',', "Value = "+button_press(b_presets[7]))))
    button8.pack(side = "left")
    b_menu(button8, button8.cget("text"), b_presets[7])
    
    button9 = tk.Button(self, text = b_names[8], \
    command = lambda: (print("Button Press:", button9.cget("text")+',', "Value = "+button_press(b_presets[8]))))
    button9.pack(side = "left")
    b_menu(button9, button9.cget("text"), b_presets[8])
    
    button10 = tk.Button(self, text = b_names[9], \
    command = lambda: (print("Button Press:", button10.cget("text")+',', "Value = "+button_press(b_presets[9]))))
    button10.pack(side = "left")
    b_menu(button10, button10.cget("text"), b_presets[9])

def journal_config(self):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    default_flags = "-d6,3+4,1;-m2;-g6;-s2"
    b_names = ["1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100", \
    "2 Single 1d20s", "2d20 Drop Low", "2d20 Drop High"]
    b_presets = [["-d4,1"], ["-d6,1"], ["-d8,1"], ["-d10,1"], ["-d12,1"], \
    ["-d20,1"], ["-d100,1"], ["-d20,1;-g2"], ["-d20,2;-L"], ["-d20,2;-H"]]
    
    def button_press(value):
        text.insert(tk.END, dc_run(value[0].split(';'))),\
        text.see(tk.END)
        return value[0]
    
    def b_menu(self, name, value):
        button_rc_popup = tk.Menu(self, tearoff = 0)
        button_rc_popup.add_command(label = value[0],\
        command = lambda: button_press(value))
        button_rc_popup.add_separator()
        button_rc_popup.add_command(label = "Rename",\
        command = lambda: b_popup_rename(self, "Rename Button"))
        button_rc_popup.add_command(label = "Revalue", \
        command = lambda: b_popup_revalue(button_rc_popup, "Enter New Value", value, self))
        button_rc_popup.bind("<Leave>", lambda b: button_rc_popup.unpost())
        if HOST_SYS == 'Darwin':
            self.bind("<Button-2>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
        else:
            self.bind("<Button-3>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
    
    def formula_roll():
        k_in = ["Test"]
        str_in = entry_val.get()
        k_in[0] = str_in.replace(' ', '') #Strip spaces out
        text.insert(tk.END, dc_run(k_in[0].split(';'))),\
        text.see(tk.END)
        return k_in[0]
    
    def b_popup_rename(self, title):
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.bind("<Return>", \
        lambda k: (popup.destroy(), self.configure(text = popup_val.get()[:20])))
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(self.cget("text"))
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), self.configure(text = popup_val.get()[:20])))
        button1.pack(pady = 5)
        #popup.geometry("250x80")
        popup.mainloop()
    
    def b_popup_revalue(self, title, value, parent):
        popup_val = tk.StringVar()
        def setvalue(self_in, value_in):
            str_in = popup_val.get()
            value_in[0] = str_in.replace(' ', '') #Strip spaces out
            self_in.entryconfigure(0, label = value[0])
            return value_in[0]
        popup = tk.Toplevel()
        popup.wm_title(title)
        entry = tk.Entry(popup, textvariable = popup_val)
        entry.config(bg = "gray90")
        entry.bind("<Return>", \
        lambda k: (popup.destroy(), print(parent.cget("text")+',', "Revalue = "+setvalue(self, value))))
        entry.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(value[0])
        button1 = tk.Button(popup, text = "Ok",\
        command = lambda: (popup.destroy(), print(parent.cget("text")+',', "Revalue = "+setvalue(self, value))))
        button1.pack(pady = 5)
        #popup.geometry("200x80")
        popup.mainloop()
    
    text = tk.Text(self, width = 90, height = 30)
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
    entry.bind("<Return>", lambda k: print("Keyboard Input: Execute Roll Formula, Value =", formula_roll()))
    entry.pack(fill = "x")
    entry_val.set(default_flags)
    
    rollbutton = tk.Button(self, text = "[Execute Roll Formula]", \
    command = lambda: print("Button Press: [Execute Roll Formula], Value =", formula_roll()))
    rollbutton.pack(side = "top", fill = "x")
    
    button1 = tk.Button(self, text = b_names[0], \
    command = lambda: (print("Button Press:", button1.cget("text")+',', "Value = "+button_press(b_presets[0]))))
    button1.pack(side = "left")
    b_menu(button1, button1.cget("text"), b_presets[0])
    
    button2 = tk.Button(self, text = b_names[1], \
    command = lambda: (print("Button Press:", button2.cget("text")+',', "Value = "+button_press(b_presets[1]))))
    button2.pack(side = "left")
    b_menu(button2, button2.cget("text"), b_presets[1])
    
    button3 = tk.Button(self, text = b_names[2], \
    command = lambda: (print("Button Press:", button3.cget("text")+',', "Value = "+button_press(b_presets[2]))))
    button3.pack(side = "left")
    b_menu(button3, button3.cget("text"), b_presets[2])
    
    button4 = tk.Button(self, text = b_names[3], \
    command = lambda: (print("Button Press:", button4.cget("text")+',', "Value = "+button_press(b_presets[3]))))
    button4.pack(side = "left")
    b_menu(button4, button4.cget("text"), b_presets[3])
    
    button5 = tk.Button(self, text = b_names[4], \
    command = lambda: (print("Button Press:", button5.cget("text")+',', "Value = "+button_press(b_presets[4]))))
    button5.pack(side = "left")
    b_menu(button5, button5.cget("text"), b_presets[4])
    
    button6 = tk.Button(self, text = b_names[5], \
    command = lambda: (print("Button Press:", button6.cget("text")+',', "Value = "+button_press(b_presets[5]))))
    button6.pack(side = "left")
    b_menu(button6, button6.cget("text"), b_presets[5])
    
    button7 = tk.Button(self, text = b_names[6], \
    command = lambda: (print("Button Press:", button7.cget("text")+',', "Value = "+button_press(b_presets[6]))))
    button7.pack(side = "left")
    b_menu(button7, button7.cget("text"), b_presets[6])
    
    button8 = tk.Button(self, text = b_names[7], \
    command = lambda: (print("Button Press:", button8.cget("text")+',', "Value = "+button_press(b_presets[7]))))
    button8.pack(side = "left")
    b_menu(button8, button8.cget("text"), b_presets[7])
    
    button9 = tk.Button(self, text = b_names[8], \
    command = lambda: (print("Button Press:", button9.cget("text")+',', "Value = "+button_press(b_presets[8]))))
    button9.pack(side = "left")
    b_menu(button9, button9.cget("text"), b_presets[8])
    
    button10 = tk.Button(self, text = b_names[9], \
    command = lambda: (print("Button Press:", button10.cget("text")+',', "Value = "+button_press(b_presets[9]))))
    button10.pack(side = "left")
    b_menu(button10, button10.cget("text"), b_presets[9])

class GUITest(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "dc_GUI")
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        
        def n_popup_ladd(self, title):
            def new_ltab(n_title):
                new_ledger = ttk.Frame(self)
                notebook.add(new_ledger, text = n_title)
                ledger_config(new_ledger)
            popup_val = tk.StringVar()
            popup = tk.Toplevel()
            popup.wm_title(title)
            entry = tk.Entry(popup, textvariable = popup_val)
            entry.config(bg = "gray90")
            entry.bind("<Return>", \
            lambda k: (popup.destroy(), new_ltab(popup_val.get()[:30])))
            entry.pack(padx = 20, pady = 10, fill = "x")
            popup_val.set("New Ledger")
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), new_ltab(popup_val.get()[:30])))
            button1.pack(pady = 5)
            popup.mainloop()
        
        def n_popup_jadd(self, title):
            def new_jtab(n_title):
                new_journal = ttk.Frame(self)
                notebook.add(new_journal, text = n_title)
                journal_config(new_journal)
            popup_val = tk.StringVar()
            popup = tk.Toplevel()
            popup.wm_title(title)
            entry = tk.Entry(popup, textvariable = popup_val)
            entry.config(bg = "gray90")
            entry.bind("<Return>", \
            lambda k: (popup.destroy(), new_jtab(popup_val.get()[:30])))
            entry.pack(padx = 20, pady = 10, fill = "x")
            popup_val.set("New Journal")
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), new_jtab(popup_val.get()[:30])))
            button1.pack(pady = 5)
            popup.mainloop()
        
        def n_popup_tdel(title, target):
            popup_val = tk.StringVar()
            popup = tk.Toplevel()
            popup.wm_title(title)
            label = tk.Label(popup, text = "Delete "+notebook.tab(target, 'text')+"?")
            label.pack(pady = 10, padx= 10, side = "top", fill="x")
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), notebook.forget(target)))
            button1.pack(pady = 5)
            popup.geometry("250x80")
            popup.mainloop()
        
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
        toolsmenu.add_command(label = "Roll Formula Builder", \
        #command = lambda: popup_wrn("Formula Build", "Not supported yet."))
        command = lambda: formula_get("Roll Formula Builder", "Enter a test Roll Formula:"))
        
        helpmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        helpmenu.add_command(label = "Roll Formula", \
        command = lambda: popup_rfhlp("Roll Formula Help Topics"))
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
        
        def n_popup_rename(title, target):
            popup_val = tk.StringVar()
            popup = tk.Toplevel()
            popup.wm_title(title)
            entry = tk.Entry(popup, textvariable = popup_val)
            entry.config(bg = "gray90")
            entry.bind("<Return>", \
            lambda k: (popup.destroy(), notebook.tab(target, text = popup_val.get()[:30])))
            entry.pack(padx = 20, pady = 10, fill = "x")
            popup_val.set(notebook.tab(notebook.select(), 'text'))
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), notebook.tab(target, text = popup_val.get()[:30])))
            button1.pack(pady = 5)
            #popup.geometry("200x80")
            popup.mainloop()
        
        note_rc_popup = tk.Menu(notebook, tearoff = 0)
        note_rc_popup.add_command(label = "Rename",\
        command = lambda: n_popup_rename("Rename Tab", notebook.select()))
        note_rc_popup.add_command(label = "Add Ledger",\
        command = lambda: n_popup_ladd(notebook, "Add Ledger"))
        note_rc_popup.add_command(label = "Add Journal",\
        command = lambda: n_popup_jadd(notebook, "Add Journal"))
        #note_rc_popup.add_separator()
        note_rc_popup.add_command(label = "Delete",\
        command = lambda: n_popup_tdel("Delete Tab", notebook.select()))
        note_rc_popup.bind("<Leave>", lambda p: note_rc_popup.unpost())
        if HOST_SYS == 'Darwin':
            notebook.bind("<Button-2>",\
            lambda n: note_rc_popup.post(n.x_root, n.y_root))
        else:
            notebook.bind("<Button-3>",\
            lambda n: note_rc_popup.post(n.x_root, n.y_root))
        
        notebook.add(note1, text = "Ledger 1")
        ledger_config(note1)
        
        notebook.add(note2, text = "Ledger 2")
        ledger_config(note2)
        
        notebook.add(note3, text = "Journal 1")
        journal_config(note3)
        
        notebook.add(note4, text = "Journal 2")
        journal_config(note4)
        
        notebook.add(note5, text = "Journal 3")
        journal_config(note5)
        
        notebook.pack(fill = "both", expand = 1)

print('Host OS:', HOST_SYS)
app = GUITest()
#app.geometry("1000x650")
app.mainloop()
