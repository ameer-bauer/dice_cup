#!/usr/bin/env python3
#----------------
#Name: dc_GUI.py
#Version: 0.1.18
#Date: 2018-11-14
#----------------

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
from datetime import datetime
from platform import system
from sys import version_info

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 9)
SMALL_FONT = ("Verdana", 8)
HOST_SYS = system()
PY_VER = version_info
WIN_DEFAULT = ['cmd', '/C', 'dice_cup.py']
NIX_DEFAULT = ['./dice_cup.py']
VERSION = "0.1.18"

def config_read(f_name = 'defaults.cfg'):
    error_blk = "\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n"
    error_str = "ERROR"
    error_cli = "FileIn Error: Incorrect format of config file \'"+f_name+"\'."
    n = True
    n_list = []
    b_list = []
    l_count = 0
    cfg_in = []
    
    try:
        f_in = open(f_name, encoding = 'utf-8', mode = 'r')
    except:
        print(error_blk)
        print("FileIn Error: Can\'t properly open the config file \'"+f_name+"\'.")
        print("Please verify the filename, path, and permissions of the config file.")
        return error_str
    
    for line_in in f_in:
        cfg_in.append(line_in[:-1])
        l_count += 1
    f_in.close()
    if l_count % 2 != 0:
        print(error_blk)
        print(error_cli)
        print("ERROR: The config file must have an even number of lines.")
        return error_str
    l_count = 0
    for a in cfg_in:
        l_count += 1
        if n and (':' in a) and ((a[-1] == 'L') or (a[-1] == 'J')):
            n_list.append(a)
            n = False
        elif not n and ':' in a:
            b_list.append(a)
            n = True
        else:
            print(error_blk)
            print(error_cli)
            print("ERROR: Invalid config file syntax on line number "+str(l_count)+".")
            return error_str
    print("CfgFileParse: Successfully parsed", f_name)
    return [n_list, b_list]

def config_write(f_name, c_list):
    error_blk = "\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n"
    error_str = "ERROR"
    error_cli = "FileOutError: Unable to write to config file \'"+f_name+"\'."
    
    try:
        f_out = open(f_name, encoding = 'utf-8', mode = 'w')
    except:
        print(error_blk)
        print(error_cli)
        print("Please validate the filename and permissions.")
        return error_str
    c_count = f_out.write(c_list)
    f_out.close()
    print("CfgFileWrite:", c_count, "characters written to", f_name)
    return

def dc_run_q(params, formula = False, label = 'Roll Formula'):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params+['-q'], stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params+['-q'], stdout=subprocess.PIPE)
    now = datetime.now()
    str_dc_out = str(dc_out)
    if formula:
        str_params = '['+formula[:100]+']'
    else:
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
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+label+' '+str_params+'  '+dc_print.strip('b\')')[:2048]

def dc_run(params, formula = False, label = 'Roll Formula'):
    if HOST_SYS == 'Windows':
        dc_out = subprocess.run(WIN_DEFAULT+params, stdout=subprocess.PIPE)
    else:
        dc_out = subprocess.run(NIX_DEFAULT+params, stdout=subprocess.PIPE)
    now = datetime.now()
    str_dc_out = str(dc_out)
    if formula:
        str_params = '['+formula[:100]+']'
    else:
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
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f  ")+label+' '+str_params+'\n'+dc_print.strip('b\')')+'\n'

def popup_wrn(title, msg, geom = "250x80"):
    popup = tk.Toplevel()
    popup.wm_attributes("-topmost", True)
    popup.wm_title(title)
    label = tk.Label(popup, text = msg)
    label.pack(pady = 10, padx= 30, side = "top", fill="x")
    button1 = tk.Button(popup, text = "Ok",  command = popup.destroy)
    button1.pack(pady = 5)
    popup.geometry(geom)
    popup.mainloop()

def file_load(title):
    filename =  filedialog.askopenfilename(initialdir = ".", title = title,\
    filetypes = (("cfg Files","*.cfg"), ("All Files","*.*")))
    if not filename:
        print ("CfgFile Load: Cancelled")
        return False
    else:
        print ("CfgFile Load:", filename)
        return filename

def file_save(title):
    filename =  filedialog.asksaveasfilename(initialdir = ".", title = title,\
    filetypes = (("cfg Files","*.cfg"), ("All Files","*.*")))
    if not filename:
        print ("CfgFile Save: Cancelled")
        return False
    else:
        print ("CfgFile Save:", filename)
        return filename

def popup_rfhlp(title):
    popup = tk.Toplevel()
    popup.wm_title(title)
    text = tk.Text(popup, width = 80, height = 30)
    scroll = tk.Scrollbar(popup)
    text.insert(tk.END, "A \'Roll Formula\' is a flexible input mechanism for simulating various dice\n")
    text.insert(tk.END, "rolls.  It is designed to be intuitive and predictable in structure.  Below you\n")
    text.insert(tk.END, "will find the syntactical and variable definitions along with some examples.\n")
    text.insert(tk.END, "Please note that verbose error messages are printed to the CLI window.\n")
    text.insert(tk.END, "Roll Formulae have a maximum size of 100 characters.  At least one combination \n")
    text.insert(tk.END, "of dice must be defined to form a valid Roll Formula.\n\n")
    text.insert(tk.END, "SYNTAX\n  s^ g* c1dt1 ±c2dt2 ... ±cndtn ±m ±p% <±u >±l L|H I\n\n")
    text.insert(tk.END, "  NOTE: All input variables are either INTEGERS, or FLAGS which can be\n")
    text.insert(tk.END, "        present or omitted; empty spaces are optional.\n\n")
    text.insert(tk.END, "  INTEGERS\n    s = dice Set [POSITIVE ONLY]\n    g = dice Group [POSITIVE ONLY]\n\n")
    text.insert(tk.END, "    c1, c2, ... cn = the Combination of corresponding die Types to roll\n")
    text.insert(tk.END, "    t1, t2, ... tn = the Type(s) of dice to roll [POSITIVE ONLY]\n")
    text.insert(tk.END, "    NOTE: c1dt1 can not be preceded by a \'+\' or a \'-\' symbol.\n\n")
    text.insert(tk.END, "    m = Modifier\n    p = Percentage\n\n")
    text.insert(tk.END, "    u = Upper Boundary (is evaluated as \'total result\' <= u)\n")
    text.insert(tk.END, "    l = Lower Boundary (is evaluated as \'total result\' >= l)\n\n")
    text.insert(tk.END, "  FLAGS\n    L = drop the Lowest c1dt1 single die roll in the combination\n")
    text.insert(tk.END, "    H = drop the Highest c1dt1 single die roll in the combination\n")
    text.insert(tk.END, "    NOTE: either L or H can be set, but not both.\n\n")
    text.insert(tk.END, "    I = include Statistical Information\n\n")
    text.insert(tk.END, "EXAMPLES\n  1) Roll three six-sided dice.\n\n     Roll Formula Syntax: 3d6\n\n")
    text.insert(tk.END, "  2) Roll two Groups of three six-sided dice, plus one four-sided die, and\n")
    text.insert(tk.END, "     subtract a Modifier of five.\n\n")
    text.insert(tk.END, "     Roll Formula Syntax: 2*3d6+1d4-5\n\n")
    text.insert(tk.END, "  3) Roll five Sets of six Groups of four six-sided dice, add a Percentage of\n")
    text.insert(tk.END, "     fifteen (15%), Drop the Lowest single six-sided die from each Group, and\n")
    text.insert(tk.END, "     include Statistical Information.\n\n     Roll Formula Syntax: 5^6*4d6+15%LI\n\n")
    text.insert(tk.END, "  4) Roll twenty Groups of ten eight-sided dice, minus a Modifier of seventeen,\n")
    text.insert(tk.END, "     an Upper Boundary of sixty five, a Lower Boundary of negative ten, and\n")
    text.insert(tk.END, "     Drop the Highest single eight-sided die from each dice Group.\n\n")
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
    button1 = tk.Button(popup, text = "Ok",\
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
    entry.bind("<Return>",\
    lambda k: (popup.destroy(),\
    print("Parsed Flags:", formula_parse(popup_val.get().replace(' ', '')[:100], True))))
    entry.pack(padx = 20, pady = 5, fill = "x")
    popup_val.set("2^5*3d6+3")
    button1 = tk.Button(popup, text = "Ok",\
    command = lambda: (popup.destroy(),\
    print("Parsed Flags:", formula_parse(popup_val.get().replace(' ', '')[:100], True))))
    button1.pack(pady = 5)
    popup.geometry("250x110")
    popup.mainloop()

def formula_parse(params_in, verbose = False):
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
    params_str = params_in.replace(' ', '')[:100]#Strip spaces and limit input just in case
    error_blk = "\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n"
    error_str = ['ERROR']
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
        sm = False
        sp = False
        fm = False
        fp = False
        
        #Initial formula structure checking
        if (str_in[0] == '+' or str_in[0] == '-'):
            return "ERROR:"+str_in+'F'
        if 'd' not in str_in or str_in[0] == 'd':
            return "ERROR:"+str_in
        if '-' in str_in:
            sm = True
        if '+' in str_in:
            sp = True
        
        #Formula structure discovery
        if sm and sp:
            if str_in.find('-') < str_in.find('+'):
                str_f = str_in.split('-', maxsplit = 1)
                if 'd' in str_f[0]:
                    str_fm = str_f[0].split('d')
                    if str_fm[0].isnumeric() and str_fm[1].isnumeric():
                        d_str += str_fm[1]+','+str_fm[0]
                        fm = True
                    else:
                        return "ERROR:"+str_in
                else:
                    return "ERROR:"+str_in
            if str_in.find('-') > str_in.find('+'):
                str_f = str_in.split('+', maxsplit = 1)
                if 'd' in str_f[0]:
                    str_fp = str_f[0].split('d')
                    if str_fp[0].isnumeric() and str_fp[1].isnumeric():
                        d_str += str_fp[1]+','+str_fp[0]
                        fp = True
                    else:
                        return "ERROR:"+str_in
                else:
                    return "ERROR:"+str_in
        elif sm:
            str_f = str_in.split('-', maxsplit = 1)
            if 'd' in str_f[0]:
                str_fm = str_f[0].split('d')
                if str_fm[0].isnumeric() and str_fm[1].isnumeric():
                    d_str += str_fm[1]+','+str_fm[0]
                    fm = True
                else:
                    return "ERROR:"+str_in
            else:
                return "ERROR:"+str_in
        elif sp:
            str_f = str_in.split('+', maxsplit = 1)
            if 'd' in str_f[0]:
                str_fp = str_f[0].split('d')
                if str_fp[0].isnumeric() and str_fp[1].isnumeric():
                    d_str += str_fp[1]+','+str_fp[0]
                    fp = True
                else:
                    return "ERROR:"+str_in
            else:
                return "ERROR:"+str_in
        else:
            str_f = str_in.split('d')
            if str_f[0].isnumeric() and str_f[1].isnumeric():
                d_str += str_f[1]+','+str_f[0]
                return d_str
            else:
                return "ERROR:"+str_in
        
        #Modifier handling setup
        if str_in.rfind('+') > str_in.rfind('-'):#Positive Modifier handling
            z_add_m = str_in.rsplit('+', maxsplit = 1)
            if not z_add_m[0][-1].isnumeric():
                return "ERROR:"+str_in
            if 'd' not in z_add_m[1]:
                if z_add_m[1].isnumeric():
                    mp = True
                    if verbose:
                        print("Roll Formula: Positive Modifier Defined")
                    params.append('-m'+z_add_m[1])
                else:
                    return "ERROR:"+'+'+z_add_m[1]
        if str_in.rfind('-') > str_in.rfind('+'):#Negative Modifier handling
            z_sub_m = str_in.rsplit('-', maxsplit = 1)
            if not z_sub_m[0][-1].isnumeric():
                return "ERROR:"+str_in
            if 'd' not in z_sub_m[1]:
                if z_sub_m[1].isnumeric():
                    mm = True
                    if verbose:
                        print("Roll Formula: Negative Modifier Defined")
                    params.append('-m-'+z_sub_m[1])
                else:
                    return "ERROR:"+'-'+z_sub_m[1]
        
        #Dice handling setup
        if fp:
            if mp:
                z_tmp = z_add_m[0].split('+')
                z_add = z_tmp[1:]
            elif mm:
                z_tmp = z_sub_m[0].split('+')
                z_add = z_tmp[1:]
            else:
                z_add = str_f[1].split('+')
            for a in z_add:
                if 'd' in a:
                    d_tmp = a.split('d', maxsplit = 1)
                    if d_tmp[0].isnumeric() and d_tmp[1].isnumeric():
                        d_str += '+'+d_tmp[1]+','+d_tmp[0]
                    elif d_tmp[0].isnumeric() and ('-' in d_tmp[1]):
                        d_tmp_s = d_tmp[1].split('-')
                        if d_tmp_s[0].isnumeric():
                            d_str += '+'+d_tmp_s[0]+','+d_tmp[0]
                            for b in d_tmp_s[1:]:
                                if 'd' in b:
                                    d_tmp2 = b.split('d', maxsplit = 1)
                                    if d_tmp2[0].isnumeric() and d_tmp2[1].isnumeric():
                                        d_str += '+'+d_tmp2[1]+',-'+d_tmp2[0]
                                    else:
                                        return "ERROR:"+b
                        else:
                            return "ERROR:"+str_in
                    else:
                        return "ERROR:"+str_in
        elif fm:
            if mp:
                z_tmp = z_add_m[0].split('-')
                z_sub = z_tmp[1:]
            elif mm:
                z_tmp = z_sub_m[0].split('-')
                z_sub = z_tmp[1:]
            else:
                z_sub = str_f[1].split('-')
            for a in z_sub:
                if 'd' in a:
                    d_tmp = a.split('d', maxsplit = 1)
                    if d_tmp[0].isnumeric() and d_tmp[1].isnumeric():
                        d_str += '+'+d_tmp[1]+',-'+d_tmp[0]
                    elif d_tmp[0].isnumeric() and ('+' in d_tmp[1]):
                        d_tmp_p = d_tmp[1].split('+')
                        if d_tmp_p[0].isnumeric():
                            d_str += '+'+d_tmp_p[0]+',-'+d_tmp[0]
                            for b in d_tmp_p[1:]:
                                if 'd' in b:
                                    d_tmp2 = b.split('d', maxsplit = 1)
                                    if d_tmp2[0].isnumeric() and d_tmp2[1].isnumeric():
                                        d_str += '+'+d_tmp2[1]+','+d_tmp2[0]
                                    else:
                                        return "ERROR:"+b
                        else:
                            return "ERROR:"+str_in
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
        if verbose:
            print("Roll Formula: Statistical Information Enabled")
    
    #Drop Lowest handling
    if 'L' in params_str:
        L = True
        if I:
            params_str_L = params_str_I.replace('L', '')
        else:
            params_str_L = params_str.replace('L', '')
        params.append('-L')
        if verbose:
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
            if verbose:
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
        if verbose:
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
            if verbose:
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
        if verbose:
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
            if verbose:
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
        if verbose:
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
            if verbose:
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
            if verbose:
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
            if z_err[1][-1] == 'F':
                print("Roll Formula \'Dice Combination\' Syntax Error:", z_err[1][:-1])
                print("The first \'Dice Combination\' can not be preceded by a \'+\' or \'-\' symbol.")
            else:
                print("Roll Formula \'Dice Combination\' Syntax Error:", z_err[1])
            print(error_cli)
            return error_str
        else:
            if verbose:
                print("Roll Formula: Dice Combination Defined")
            params.append('-d'+z)
    
    return params

def ledger_config(self, configs = False):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    def_formula = "2^5*3d6+1d4-5"
    
    if not configs:
        b_count = 10
        b_names = ["1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100",\
        "2 Single d20s", "2d20 Drop Low", "2d20 Drop High"]
        b_presets = [["1d4"], ["1d6"], ["1d8"], ["1d10"], ["1d12"],\
        ["1d20"], ["1d100"], ["2*1d20"], ["2d20L"], ["2d20H"]]
    else:
        b_count = 0
        b_names = []
        b_presets = []
        b_list = configs.split(',')
        for c in b_list:
            c_list = c.split(':', maxsplit = 1)
            b_names.append(c_list[0])
            b_presets.append([c_list[1]])
            b_count += 1
    
    def button_press(value, label):
        listbox.insert(tk.END, dc_run_q(formula_parse(value[0]), value[0], label)),\
        listbox.see(tk.END)
        listbox.select_clear(0,tk.END)
        listbox.select_set(tk.END)
        return value[0]
    
    def formula_roll():
        str_in = entry_val.get().replace(' ', '')[:100]
        listbox.insert(tk.END, dc_run_q(formula_parse(str_in), str_in)),\
        listbox.see(tk.END)
        listbox.select_clear(0,tk.END)
        listbox.select_set(tk.END)
        return str_in
    
    def b_popup_config(self, title, value, parent):
        popup_lab = tk.StringVar()
        popup_val = tk.StringVar()
        def setvalue(self_in, value_in):
            value_in[0] = popup_val.get().replace(' ', '')[:100]
            self_in.entryconfigure(0, label = value[0])
            return value_in[0]
        def setname(self_in):
            text_in = popup_lab.get().replace(':', '')[:20]#Watch for length and ctrl chars
            self_in.configure(text = text_in)
            return text_in
        popup = tk.Toplevel()
        popup.wm_title(title)
        
        label1 = tk.Label(popup, text = "Button Label:")
        label1.pack(fill="x")
        entry_lab = tk.Entry(popup, textvariable = popup_lab)
        entry_lab.config(bg = "gray90")
        entry_lab.bind("<Return>",\
        lambda k1: (popup.destroy(), print("Button ReCfg:",\
        '\''+parent.cget("text")+'\',', "Revalue = "+setvalue(self, value)+',',\
        "Rename = \'"+setname(parent)+'\'')))
        entry_lab.pack(padx = 35, pady = 5, fill = "x")
        popup_lab.set(parent.cget("text"))
        
        label2 = tk.Label(popup, text = "Roll Formula:")
        label2.pack(fill="x")
        entry_val = tk.Entry(popup, textvariable = popup_val)
        entry_val.config(bg = "gray90")
        entry_val.bind("<Return>",\
        lambda k2: (popup.destroy(), print("Button ReCfg:",\
        '\''+parent.cget("text")+'\',', "Revalue = "+setvalue(self, value)+',',\
        "Rename = \'"+setname(parent)+'\'')))
        entry_val.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(value[0])
        
        button0 = tk.Button(popup, text = "OK",\
        command = lambda: (popup.destroy(), print("Button ReCfg:",\
        '\''+parent.cget("text")+'\',', "Revalue = "+setvalue(self, value)+',',\
        "Rename = \'"+setname(parent)+'\'')))
        button0.pack(padx = 35, pady = 5)
        #popup.geometry("200x80")
        popup.mainloop()
    
    def b_popup_del(self, title, parent):
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        label = tk.Label(popup, text = "Delete the button \'"+parent.cget("text")+"\' ?")
        label.pack(pady = 10, padx= 10, side = "top", fill="x")
        button1 = tk.Button(popup, text = "Ok",  command =\
        lambda: (popup.destroy(), print("ButtonDelete: \'"+parent.cget("text")+'\''), parent.destroy()))
        button1.pack(pady = 5)
        #popup.geometry("280x80")
        popup.mainloop()
    
    def b_popup_add(self, title):
        def b_make():
            value_in = []
            value_in.append(popup_val.get().replace(' ', '')[:100])
            name = popup_lab.get().replace(':', '')[:20]
            button = tk.Button(self, text = name,\
            command = lambda: (print("Button Press:", '\''+button.cget("text")+'\',',\
            "Value = "+button_press(value_in, button.cget("text")))))
            button.pack(side = "left")
            b_menu(button, name, value_in, self)
            print("ButtonCreate: \'"+name+'\',', "Value =", value_in[0])
        
        popup_lab = tk.StringVar()
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        label1 = tk.Label(popup, text = "Button Label:")
        label1.pack(fill="x")
        entry_lab = tk.Entry(popup, textvariable = popup_lab)
        entry_lab.config(bg = "gray90")
        entry_lab.bind("<Return>",\
        lambda k1: (popup.destroy(), b_make()))
        entry_lab.pack(padx = 35, pady = 5, fill = "x")
        popup_lab.set("New Button")
        
        label2 = tk.Label(popup, text = "Roll Formula:")
        label2.pack(fill="x")
        entry_val = tk.Entry(popup, textvariable = popup_val)
        entry_val.config(bg = "gray90")
        entry_val.bind("<Return>",\
        lambda k2: (popup.destroy(), b_make()))
        entry_val.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set("1d13")
        
        button0 = tk.Button(popup, text = "OK",\
        command = lambda: (popup.destroy(),\
        b_make()))
        button0.pack(padx = 35, pady = 5)
        popup.mainloop()
    
    def b_menu(self, name, value, parent = None):
        button_rc_popup = tk.Menu(self, tearoff = 0)
        button_rc_popup.add_command(label = value[0],\
        command = lambda: button_press(value))
        button_rc_popup.add_separator()
        button_rc_popup.add_command(label = "Configure",\
        command = lambda: b_popup_config(button_rc_popup, "Configure Button", value, self))
        button_rc_popup.add_command(label = "Create",\
        command = lambda: b_popup_add(parent, "Create Button"))
        button_rc_popup.add_command(label = "Delete",\
        command = lambda: b_popup_del(button_rc_popup, "Delete Button", self))
        button_rc_popup.bind("<Leave>", lambda b: button_rc_popup.unpost())
        if HOST_SYS == 'Darwin':
            self.bind("<Button-2>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
        else:
            self.bind("<Button-3>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
    
    def button_make(self, name, value):
        #name must be strings, value must be a single element list
        button = tk.Button(self, text = name,\
        command = lambda: (print("Button Press:", '\''+button.cget("text")+'\',',\
        "Value = "+button_press(value, button.cget("text")))))
        button.pack(side = "left")
        b_menu(button, button.cget("text"), value, self)
    
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
    entry.bind("<Return>", lambda k: print("Keyboard In.: \'[Execute Roll Formula]\', Value =", formula_roll()))
    entry.pack(fill = "x")
    entry_val.set(def_formula)
    
    rollbutton = tk.Button(self, text = "[Execute Roll Formula]", \
    command = lambda: print("Button Press: \'[Execute Roll Formula]\', Value =", formula_roll()))
    rollbutton.pack(side = "top", fill = "x")
    
    for a in range(0, b_count):
        button_make(self, b_names[a], b_presets[a])

def journal_config(self, configs = False):
    set_val = tk.IntVar()
    entry_val = tk.StringVar()
    def_formula = "2^5*3d6+1d4-5I"
    
    if not configs:
        b_count = 10
        b_names = ["1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100",\
        "2 Single d20s", "2d20 Drop Low", "2d20 Drop High"]
        b_presets = [["1d4"], ["1d6"], ["1d8"], ["1d10"], ["1d12"],\
        ["1d20"], ["1d100"], ["2*1d20"], ["2d20L"], ["2d20H"]]
    else:
        b_count = 0
        b_names = []
        b_presets = []
        b_list = configs.split(',')
        for c in b_list:
            c_list = c.split(':', maxsplit = 1)
            b_names.append(c_list[0])
            b_presets.append([c_list[1]])
            b_count += 1
    
    def button_press(value, label):
        text.insert(tk.END, dc_run(formula_parse(value[0]), value[0], label)),\
        text.see(tk.END)
        return value[0]
    
    def formula_roll():
        str_in = entry_val.get().replace(' ', '')[:100]
        text.insert(tk.END, dc_run(formula_parse(str_in), str_in)),\
        text.see(tk.END)
        return str_in
    
    def b_popup_config(self, title, value, parent):
        popup_lab = tk.StringVar()
        popup_val = tk.StringVar()
        def setvalue(self_in, value_in):
            value_in[0] = popup_val.get().replace(' ', '')[:100]
            self_in.entryconfigure(0, label = value[0])
            return value_in[0]
        def setname(self_in):
            text_in = popup_lab.get().replace(':', '')[:20]#Watch for length and ctrl chars
            self_in.configure(text = text_in)
            return text_in
        popup = tk.Toplevel()
        popup.wm_title(title)
        
        label1 = tk.Label(popup, text = "Button Label:")
        label1.pack(fill="x")
        entry_lab = tk.Entry(popup, textvariable = popup_lab)
        entry_lab.config(bg = "gray90")
        entry_lab.bind("<Return>",\
        lambda k1: (popup.destroy(), print("Button ReCfg:",\
        '\''+parent.cget("text")+'\',', "Revalue = "+setvalue(self, value)+',',\
        "Rename = \'"+setname(parent)+'\'')))
        entry_lab.pack(padx = 35, pady = 5, fill = "x")
        popup_lab.set(parent.cget("text"))
        
        label2 = tk.Label(popup, text = "Roll Formula:")
        label2.pack(fill="x")
        entry_val = tk.Entry(popup, textvariable = popup_val)
        entry_val.config(bg = "gray90")
        entry_val.bind("<Return>",\
        lambda k2: (popup.destroy(), print("Button ReCfg:",\
        '\''+parent.cget("text")+'\',', "Revalue = "+setvalue(self, value)+',',\
        "Rename = \'"+setname(parent)+'\'')))
        entry_val.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set(value[0])
        
        button0 = tk.Button(popup, text = "OK",\
        command = lambda: (popup.destroy(), print("Button ReCfg:",\
        '\''+parent.cget("text")+'\',', "Revalue = "+setvalue(self, value)+',',\
        "Rename = \'"+setname(parent)+'\'')))
        button0.pack(padx = 35, pady = 5)
        #popup.geometry("200x80")
        popup.mainloop()
    
    def b_popup_add(self, title):
        def b_make():
            value_in = []
            value_in.append(popup_val.get().replace(' ', '')[:100])
            name = popup_lab.get().replace(':', '')[:20]
            button = tk.Button(self, text = name,\
            command = lambda: (print("Button Press:", '\''+button.cget("text")+'\',',\
            "Value = "+button_press(value_in, button.cget("text")))))
            button.pack(side = "left")
            b_menu(button, name, value_in, self)
            print("ButtonCreate: \'"+name+'\',', "Value =", value_in[0])
        
        popup_lab = tk.StringVar()
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        label1 = tk.Label(popup, text = "Button Label:")
        label1.pack(fill="x")
        entry_lab = tk.Entry(popup, textvariable = popup_lab)
        entry_lab.config(bg = "gray90")
        entry_lab.bind("<Return>",\
        lambda k1: (popup.destroy(), b_make()))
        entry_lab.pack(padx = 35, pady = 5, fill = "x")
        popup_lab.set("New Button")
        
        label2 = tk.Label(popup, text = "Roll Formula:")
        label2.pack(fill="x")
        entry_val = tk.Entry(popup, textvariable = popup_val)
        entry_val.config(bg = "gray90")
        entry_val.bind("<Return>",\
        lambda k2: (popup.destroy(), b_make()))
        entry_val.pack(padx = 35, pady = 5, fill = "x")
        popup_val.set("1d13")
        
        button0 = tk.Button(popup, text = "OK",\
        command = lambda: (popup.destroy(),\
        b_make()))
        button0.pack(padx = 35, pady = 5)
        popup.mainloop()
    
    def b_popup_del(self, title, parent):
        popup_val = tk.StringVar()
        popup = tk.Toplevel()
        popup.wm_title(title)
        label = tk.Label(popup, text = "Delete the button \'"+parent.cget("text")+"\' ?")
        label.pack(pady = 10, padx= 10, side = "top", fill="x")
        button1 = tk.Button(popup, text = "Ok",  command =\
        lambda: (popup.destroy(), print("ButtonDelete: \'"+parent.cget("text")+'\''), parent.destroy()))
        button1.pack(pady = 5)
        #popup.geometry("280x80")
        popup.mainloop()
    
    def b_menu(self, name, value, parent = None):
        button_rc_popup = tk.Menu(self, tearoff = 0)
        button_rc_popup.add_command(label = value[0],\
        command = lambda: button_press(value))
        button_rc_popup.add_separator()
        button_rc_popup.add_command(label = "Configure",\
        command = lambda: b_popup_config(button_rc_popup, "Configure Button", value, self))
        button_rc_popup.add_command(label = "Create",\
        command = lambda: b_popup_add(parent, "Create Button"))
        button_rc_popup.add_command(label = "Delete",\
        command = lambda: b_popup_del(button_rc_popup, "Delete Button", self))
        button_rc_popup.bind("<Leave>", lambda b: button_rc_popup.unpost())
        if HOST_SYS == 'Darwin':
            self.bind("<Button-2>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
        else:
            self.bind("<Button-3>",\
            lambda e: button_rc_popup.post(e.x_root, e.y_root))
    
    def button_make(self, name, value):
        #name must be strings, value must be a single element list
        button = tk.Button(self, text = name,\
        command = lambda: (print("Button Press:", '\''+button.cget("text")+'\',',\
        "Value = "+button_press(value, button.cget("text")))))
        button.pack(side = "left")
        b_menu(button, button.cget("text"), value, self)
    
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
    entry.bind("<Return>", lambda k: print("Keyboard In.: \'[Execute Roll Formula]\', Value =", formula_roll()))
    entry.pack(fill = "x")
    entry_val.set(def_formula)
    
    rollbutton = tk.Button(self, text = "[Execute Roll Formula]",\
    command = lambda: print("Button Press: \'[Execute Roll Formula]\', Value =", formula_roll()))
    rollbutton.pack(side = "top", fill = "x")
    
    for a in range(0, b_count):
        button_make(self, b_names[a], b_presets[a])

class dc_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "dc_GUI  -  "+VERSION)
        
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
            entry.bind("<Return>",\
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
            entry.bind("<Return>",\
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
            label = tk.Label(popup, text = "Delete \'"+notebook.tab(target, 'text')+"\' ?")
            label.pack(pady = 10, padx= 10, side = "top", fill="x")
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), notebook.winfo_children()[target + 1].destroy()))
            button1.pack(pady = 5)
            #popup.geometry("250x80")
            popup.mainloop()
        
        notebook = ttk.Notebook(container)
        
        def init_cfgload():
            print("CfgFile Load: defaults.cfg")
            c_list = config_read()
            if 'ERROR' in c_list:#Load built-in defaults if the config file is missing or invalid
                print("Config Error: Incorrect configuration syntax, using built-in presets.")
                note1 = ttk.Frame(notebook)
                notebook.add(note1, text = "Journal 1")
                journal_config(note1)
                note2 = ttk.Frame(notebook)
                notebook.add(note2, text = "Journal 2")
                journal_config(note2)
                note3 = ttk.Frame(notebook)
                notebook.add(note3, text = "Journal 3")
                journal_config(note3)
                note4 = ttk.Frame(notebook)
                notebook.add(note4, text = "Journal 4")
                journal_config(note4)
                note5 = ttk.Frame(notebook)
                notebook.add(note5, text = "Ledger 1")
                ledger_config(note5)
            else:
                c_count = 0
                for a in c_list[0]:
                    n = a.split(':', maxsplit = 1)
                    note = ttk.Frame(notebook)
                    notebook.add(note, text = n[0])
                    if 'L' in n[1]:
                        ledger_config(note, c_list[1][c_count])
                    elif 'J' in n[1]:
                        journal_config(note, c_list[1][c_count])
                    else:
                        print("\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n")
                        print("Config Error: Incorrect configuration syntax.")
                        print("Please verify the syntax within the config file.")
                        print("!FatalError!: Exiting dc_GUI")
                        quit()
                    c_count += 1
        
        def cfg_load(title):
            f_in = file_load(title)
            f_run = True
            if f_in:
                c_list = config_read(f_in)
                if not 'ERROR' in c_list:
                    for c in notebook.winfo_children():
                        if f_run:
                            f_run = False
                        else:
                            c.destroy()
                    c_count = 0
                    for a in c_list[0]:
                        n = a.split(':', maxsplit = 1)
                        note = ttk.Frame(notebook)
                        notebook.add(note, text = n[0])
                        if 'L' in n[1]:
                            ledger_config(note, c_list[1][c_count])
                        elif 'J' in n[1]:
                            journal_config(note, c_list[1][c_count])
                        else:
                            print("\n!!!!!!!!!\n!!ERROR!!\n!!!!!!!!!\n")
                            print("Config Error: Incorrect configuration syntax.")
                            print("Please verify the syntax within the config file.")
                            print("!FatalError!: Exiting dc_GUI")
                            quit()
                        c_count += 1
        
        def cfg_save(title):
            f_name = file_save(title)
            c_list = ""
            t_names = []
            t_count = -1
            first_run = True
            for t in notebook.tabs():
                t_names.append(notebook.tab(t, 'text'))
            for c1 in notebook.winfo_children():
                if 'menu' not in str(c1):
                    if first_run:
                        t_count += 1
                        c_list += t_names[t_count]+':'
                        first_run = False
                    else:
                        t_count += 1
                        if c_list[-1] == ',':
                            c_list = c_list[:-1]
                        c_list += '\n'+t_names[t_count]+':'
                    for c2 in c1.winfo_children():
                        str_c2 = str(c2)
                        if 'listbox' in str_c2:
                            t_type = 'L'
                            c_list += t_type+'\n'
                        elif 'text' in str_c2:
                            t_type = 'J'
                            c_list += t_type+'\n'
                        elif 'button' in str_c2:
                            b_name = str(c2.cget('text'))
                            for c3 in c2.winfo_children():
                                if c3:
                                    c_list += b_name+':'
                                    b_type = str(c3.entrycget(0, 'label'))
                                    c_list += b_type+','
            if f_name:
                c_list = c_list[:-1]+'\n'
                status = config_write(f_name, c_list)
                if status:
                    print("CfgFile Save: Unsuccessful")
        
        def load_defaults():
            popup = tk.Toplevel()
            popup.wm_title("Built-in Defaults")
            label = tk.Label(popup, text =\
            "Are you sure you wish to\nload the built-in defaults?")
            label.pack(pady = 10, padx= 35, side = "top", fill="x")
            def reload_defaults():
                f_run = True
                for c in notebook.winfo_children():
                    if f_run:
                        f_run = False
                    else:
                        c.destroy()
                note1 = ttk.Frame(notebook)
                notebook.add(note1, text = "Journal 1")
                journal_config(note1)
                note2 = ttk.Frame(notebook)
                notebook.add(note2, text = "Journal 2")
                journal_config(note2)
                note3 = ttk.Frame(notebook)
                notebook.add(note3, text = "Journal 3")
                journal_config(note3)
                note4 = ttk.Frame(notebook)
                notebook.add(note4, text = "Journal 4")
                journal_config(note4)
                note5 = ttk.Frame(notebook)
                notebook.add(note5, text = "Ledger 1")
                ledger_config(note5)
                print("ConfigLoaded: Built-in Defaults")
            button0 = tk.Button(popup, text = "Yes", command =\
            lambda: (popup.destroy(), reload_defaults()))
            button0.pack(padx = 35, pady = 5, side = "left")
            button1 = tk.Button(popup, text = "No", command =\
            lambda: popup.destroy())
            button1.pack(padx = 35, pady = 5, side = "right")
            popup.mainloop()
        
        def n_popup_rename(title, target):
            popup_val = tk.StringVar()
            popup = tk.Toplevel()
            popup.wm_title(title)
            entry = tk.Entry(popup, textvariable = popup_val)
            entry.config(bg = "gray90")
            entry.bind("<Return>",\
            lambda k: (popup.destroy(), notebook.tab(target, text = popup_val.get()[:30])))
            entry.pack(padx = 20, pady = 10, fill = "x")
            popup_val.set(notebook.tab(notebook.select(), 'text'))
            button1 = tk.Button(popup, text = "Ok",  command =\
            lambda: (popup.destroy(), notebook.tab(target, text = popup_val.get()[:30])))
            button1.pack(pady = 5)
            popup.mainloop()
        
        menubar = tk.Menu(container, relief = "flat")
        
        filemenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        filemenu.add_command(label = "Open...",\
        command = lambda: popup_wrn("Open...", "Not supported yet."))
        filemenu.add_command(label = "Save As...",\
        command = lambda: popup_wrn("Save As...", "Not supported yet."))
        filemenu.add_command(label = "Save",\
        command = lambda: popup_wrn("Save", "Not supported yet."))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit",\
        command = lambda: (print("FMenu Action: Exiting dc_GUI"), quit()))
        
        settingsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        settingsmenu.add_command(label = "Load Config...",\
        command = lambda: cfg_load("Load Config File"))
        settingsmenu.add_command(label = "Save Config...",\
        command = lambda: cfg_save("Save Config File"))
        settingsmenu.add_command(label = "Built-in Defaults",\
        command = lambda: load_defaults())
        
        toolsmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        toolsmenu.add_command(label = "Roll Formula Test",\
        command = lambda: formula_get("Roll Formula Test", "Enter a Roll Formula to Validate"))
        
        helpmenu = tk.Menu(menubar, tearoff = 0, relief = "flat")
        helpmenu.add_command(label = "Roll Formula",\
        command = lambda: popup_rfhlp("Roll Formula Help"))
        helpmenu.add_command(label = "About",\
        command = lambda: popup_wrn("About", "dc_GUI version "+VERSION))
        
        menubar.add_cascade(label = "File",  menu = filemenu)
        menubar.add_cascade(label = "Settings",  menu = settingsmenu)
        menubar.add_cascade(label = "Tools",  menu = toolsmenu)
        menubar.add_cascade(label = "Help",  menu = helpmenu)
        tk.Tk.config(self, menu = menubar)
        
        #style = ttk.Style()
        #style.configure('.', font = NORMAL_FONT) #Change all default ttk styles
        
        note_rc_popup = tk.Menu(notebook, tearoff = 0)
        note_rc_popup.add_command(label = "Rename",\
        command = lambda: n_popup_rename("Rename Tab", notebook.select()))
        note_rc_popup.add_command(label = "Add Ledger",\
        command = lambda: n_popup_ladd(notebook, "Add Ledger"))
        note_rc_popup.add_command(label = "Add Journal",\
        command = lambda: n_popup_jadd(notebook, "Add Journal"))
        #note_rc_popup.add_separator()
        note_rc_popup.add_command(label = "Delete",\
        command = lambda: n_popup_tdel("Delete Tab", notebook.index(notebook.select())))
        note_rc_popup.bind("<Leave>", lambda p: note_rc_popup.unpost())
        if HOST_SYS == 'Darwin':
            notebook.bind("<Button-2>",\
            lambda n: note_rc_popup.post(n.x_root, n.y_root))
        else:
            notebook.bind("<Button-3>",\
            lambda n: note_rc_popup.post(n.x_root, n.y_root))
        
        init_cfgload()
        notebook.pack(fill = "both", expand = 1)
        
        if PY_VER[0] != 3 or PY_VER[1] < 6:
            l1 = "Warning, dc_GUI is designed to use Python 3.6.0 or greater.\n"
            l2 = "Please go to python.org and update your Python 3 installation."
            print("PyVerWarning: Incorrect version of Python 3 detected.")
            popup_wrn("Python Version Warning", l1 + l2, "450x100")

####Main Progam####
print("DetectHostOS:", HOST_SYS)
print("Detect PyVer:", "Python", str(PY_VER[0])+'.'+str(PY_VER[1])+'.'+str(PY_VER[2]))
app = dc_GUI()
app.mainloop()
