#!/usr/bin/env python3
#----------------
#Name: dice_cup
#Version: 1.1.4
#Date: 2016-03-17
#----------------

import os
import sys
import argparse
import random

version = "1.1.4"

def pos_int(p): #a function for argparse 'type' to call for checking input values
    int_p = int(p)
    if int_p <= 0:
        msg = "%r is not a positive integer." % p
        raise argparse.ArgumentTypeError(msg)
    return int_p

def d_roll(s, t = 6, c = 1, m = 0):
    #Dice rolling: (random integer in range from 1 -> t (dice type)
    #Default input, with s defined, yields roll = 1(d6)+0
    #d_roll with parameters set yield a roll = c(dt)+m
    #s is the seed for the RNG, use at LEAST 8 bytes of random data
    roll = 0
    random.seed(s)
    
    if c > 0:
        for x in range(c):
            roll += random.randint(1, t)
    elif c == 0:
        return(m)
    else:
        c = abs(c)
        for x in range(c):
            roll -= random.randint(1, t)
    
    return(roll + m)

def d_err():
    print('Error: flag \'-d\' parameter %r is incorrect.  Only integer pairs of the form' % x)
    print('       T,N having constraints of T > 1 and N != 0 are supported. Please read')
    print('       the dice_cup help by running \'dice_cup -h\'.')
    return

def h_main():
    print('Introduction to dice_cup', version)
    print('  Hello, dice_cup is a CLI program written in Python 3 to simulate')
    print('  the outcome of various types of dice rolls.  Die types can be set')
    print('  arbitrarily greater than 1, making for fun dice types like an eleven-')
    print('  sided die, or \"1(d11)\".  The nomenclature for die rolls herein is as')
    print('  follows: \"set { group [ number ( die type ) +\\- modifier ] }\"')
    print('\nSYNTAX\n  python3 dice_cup.py [-h] [-v] [-q] [-d] [-m] [-g] [-s] [-t] [-l] [-u]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.\n')
    print('  -v Displays the version of dice_cup.\n')
    print('  -q Quiet Mode: only displays the Dice Group roll outcomes delimited by a \',\'')
    print('     comma. Sets are separated by a new line, only one Set is printed per line.\n')
    print('  -d Specify the die type and number to roll.  Single or multiple')
    print('     parameter pairs may be entered to combine various die types.  The')
    print('     input pairs must be integers T,N separated by a \',\'.  An example')
    print('     of the format for these parameters is listed below:\n')
    print('     INPUT FORMAT \'-d T1,N1 [T2,N2 ... Tn,Nn]\'')
    print('       Single die types: \'-d T,N\', where type (T) > 1 and number (N) != 0,')
    print('         yields \'N\' numbers of \'T\'-sided dice rolled together.  The')
    print('         input \'-d 6,1\' will roll a single six-sided die, or \"1(d6)\".  While')
    print('         the input \'-d 10,2\' will roll two ten-sided dice, or \"2(d10)\".\n')
    print('       Multiple die types: \'-d T1,N1 T2,N2 ... Tn,Nn\' yields multiple dice')
    print('         rolled together in form \"N1(dT1) + N2(dT2) + ... + Nn(dTn)\", where')
    print('         the first number of each parameter pair must be greater than 1,')
    print('         while the second number of each pair must not be equal to 0.  The')
    print('         input \'-d 6,1 4,-2 3,4\' will roll \"1(d6) - 2(d4) + 4(d3)\".\n')
    print('  -m Add or subtract a modifier to a roll; addition is the default action.')
    print('     <defaults to m = 0>')
    print('     *Note: for NEGATIVE modifiers, some OSs may require the \'-\' to be escaped.')
    print('         i.e. for a (-4) modifier, the appropriate non-escaped flag would be')
    print('              \'-m -4\'')
    print('              for a (-4) modifier, the appropriate escaped flag values may be')
    print('              \'-m \-4\' or possibly \'-m \'-4\'\'')
    print('              for a (+7) modifier, the appropriate flag is \'-m 7\'\n')
    print('  -g Define the number of \"Dice Groups\" you wish to roll in a single Set.')
    print('     Such as rolling a group of three Dice Groups of two six-sided dice,')
    print('     or \"3[2(d6)]\".  <defaults to g = 1>\n')
    print('  -s Define how many \"Sets\" of Dice Groups you wish to roll.  Such as,')
    print('     two Sets each containing three Dice Groups of two six-sided dice,')
    print('     or \"2{3[2(d6)]}\".  <defaults to s = 1>\n')
    print('  -t Print the total sum of the Group rolls in a Set; listed as \"Group Total\".')
    print('\nOUTPUT FORMAT\n  Note that dice_cup has two modes of output:\n')
    print('   1. Standard Mode: will print the Set number, a single line for each dice')
    print('      roll in the Group, the \"Ideal Average\" (probabilistic), and the \"Group')
    print('      Average" (actual roll outcome).  NOTE: if the \'-t\' flag is set, then the')
    print('      Group Total will be printed the line after the Group Average.\n')
    print('      The dice_cup output format for two Sets with multiple rolls in a Group:')
    print('        ---\n        Set 1\n        ---')
    print('        \'Group 1\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        \'Group 2\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('            .     | \'              .              \' : \'   .   \'')
    print('            .     | \'              .              \' : \'   .   \'')
    print('            .     | \'              .              \' : \'   .   \'')
    print('        \'Group n\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        ---\n        Ideal Average: \'X1\'\n        Group Average: \'Y1\'')
    print('        ---')
    print('         .')
    print('         .')
    print('         .')
    print('        ---\n        Set n\n        ---')
    print('        \'Group 1\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        \'Group 2\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('            .     | \'              .              \' : \'   .   \'')
    print('            .     | \'              .              \' : \'   .   \'')
    print('            .     | \'              .              \' : \'   .   \'')
    print('        \'Group n\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        ---\n        Ideal Average: \'X2\'\n        Group Average: \'Y2\'')
    print('\n   2. Quiet Mode: will only output a single Set of Group rolls per line,')
    print('                    results will be printed as a comma separated list.')
    print('\nEXAMPLES\n  python3 dice_cup.py -d 6,1 -g 3')
    print('    Prints the Standard Mode output for \"3[1(d6)]\" rolls.')
    print('\n  python3 dice_cup.py -d 8,3 -m -5 -g 2')
    print('    Prints the Standard Mode output for \"2[3(d8)-5]\" rolls.')
    print('\n  python3 dice_cup.py -d 10,1 6,2 -g 4 -m 10 -s 5')
    print('    Prints the Standard Mode output for \"5{4[1(d10)+2(d6)+10]}\" rolls.')
    print('\n  python3 dice_cup.py -q -d 6,3 4,-2 32,1 -m -20 -g 30 -s 2')
    print('    Prints the Quiet Mode output for \"2{30[3(d6)-2(d4)+1(d32)-20]}\" rolls.')
    return

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome, dice_cup is a CLI-based die roll simulation engine. It utilizes a cryptographic PRNG to accurately simulate various dice rolls.')
parser.add_argument("-h", action='store_true', help="Display the help page")
parser.add_argument("-v", action='store_true', help="Display version information")
parser.add_argument("-q", action='store_true', help="Only display rolled numbers; called \'Quite Mode\'")
parser.add_argument("-d", nargs='+', type=str, help="Define the types of dice to roll; called a \'Dice Group\'", metavar='#,#')
parser.add_argument("-m", nargs='?', const=0, default=0, type=int, help="Add, or subtract, an integer roll modifier", metavar='#')
parser.add_argument("-l", nargs='?', type=str, help="Define a lower bound for all die rolls", metavar='#')
parser.add_argument("-u", nargs='?', type=str, help="Define an upper bound for all die rolls", metavar='#')
parser.add_argument("-g", nargs='?', const=1, default=1, type=pos_int, help="How many \'Dice Groups\' to roll <Defaults to 1>", metavar='#')
parser.add_argument("-s", nargs='?', const=1, default=1, type=pos_int, help="How many \'Sets of Dice Groups\' to roll <Defaults to 1>", metavar='#')
parser.add_argument("-t", action='store_true', help="Display the sum total of a \'Dice Group\' roll")
args = parser.parse_args()

if args.v:
    print('dice_cup version:', version)
    sys.exit()

if args.h:
    h_main()
    sys.exit()

#if args.l > args.u:
#    print('Input Error: flags \'-l\' and \'-u\' are set, but l =', args.l, 'is greater than u =', args.u, '.')
#    print('             Please read the dice_cup help by invoking the \'-l\' and \'-u\' flags.')
#    sys.exit(1)

if args.d:
    p_list = []
    m_str = str(args.m)
    g_len = len(str(args.g))
    for x in args.d:
        d_pair = x.split(',')
        #Check the -d parameter list for input errors...
        if len(d_pair) != 2:
            d_err()
            sys.exit(1)
        try:
            if (int(d_pair[1]) == 0) or (int(d_pair[0]) < 2):
                d_err()
                sys.exit(1)
        except ValueError:
            d_err()
            sys.exit(1)
        p_list.append(d_pair) #Store the sane -d parameter list
    a_ideal = 0;
    #Scan through the -d parameters to calulate the Ideal Average
    for z in p_list: #Faster to calculate here, just in case there are multiple groups
        zt_int = int(z[0])
        zg_int = int(z[1])
        a_ideal += (zg_int * ((zt_int + 1) / 2))
    a_ideal += args.m
    for y in range(args.s):
        t_group = 0
        if not args.q:
            print('---\nSet', (y+1))
            print('---')
        for x in range(args.g):
            r = 0
            if not args.q:
                print('Group',repr(x+1).rjust(g_len), '|', end = ' ')
            for z in p_list: #Generate the dice roll outcomes of the -d parameters
                zt_int = int(z[0])
                zg_int = int(z[1])
                r += d_roll(os.urandom(16), zt_int, zg_int)
                if not args.q:
                    print(z[1]+'(d'+z[0]+') +', end = ' ')
            r += args.m
            if not args.q:
                print('('+m_str+') :', r)
            else:
                if (x+1) < args.g:
                    print(r, end=',')
                else:
                    print(r)
            t_group += r
        a_group = t_group / args.g #Calculate the Group roll average
        if not args.q:
            print('---\nIdeal Average:', a_ideal)
            print('Group Average:', a_group)
        if args.t and not args.q:
            print('Group Total:', t_group)
    sys.exit()

parser.print_help()
