#!/usr/bin/env python3
#----------------
#Name: dice_cup
#Version: 1.1.3
#Date: 2015-05-01
#----------------

import os
import sys
import argparse
import random

def pos_int(p): #a function for argparse 'type' to call for checking input values
    int_p = int(p)
    if int_p <= 0:
        msg = "%r is not a positive integer." % p
        raise argparse.ArgumentTypeError(msg)
    return int_p

def d_roll (s, t = 6, c = 1, m = 0):
    #Dice rolling: (random integer in range from 1 -> t (dice type)
    #Default input, with s defined, yields roll = 1(d6)+0
    #d_roll with parameters set yield a roll = c(dt)+m
    #s is the seed for the RNG, use at LEAST 8 bytes of random data
    roll = 0
    random.seed(s)
    for x in range(c):
        roll += random.randint (1, t)
    return (roll + m)

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome to dice_cup, a CLI-based dice rolling program.')
parser.add_argument("-h", action='store_true', help="Display the help page.")
parser.add_argument("-v", action='store_true', help="Display version information.")
parser.add_argument("-q", action='store_true', help="Quiet Mode: only display rolled numbers.")
parser.add_argument("-d", nargs='+', type=str, help="*REQUIRED* Set the combo and die type(s) to roll.", metavar='#,#')
parser.add_argument("-m", nargs='?', const=0, default=0, type=int, help="Add or subtract a roll modifier.", metavar='# or \-#')
parser.add_argument("-g", nargs='?', const=1, default=1, type=pos_int, help="Define the number of rolls in a Group.", metavar='#')
parser.add_argument("-s", nargs='?', const=1, default=1, type=pos_int, help="Define how many \'Sets of Groups\' to roll.", metavar='#')
parser.add_argument("-t", action='store_true', help="Display the total / sum of a Group roll.")
args = parser.parse_args()

version = "1.1.3"

if args.v:
    print('dice_cup version:', version)
    sys.exit()

if args.h:
    print('Introduction to dice_cup', version)
    print('  Hello, dice_cup is a CLI program written in Python 3.x to simulate')
    print('  the outcome of various types of dice rolls.  Die types can be set')
    print('  arbitrarily greater than 1, making for fun dice types like an eleven-')
    print('  sided die, or \"1(d11)\".  The nomenclature for die rolls herein is as')
    print('  follows: \"set { group [ combination ( die type ) +\\- modifier ] }\"')
    print('\nSYNTAX\n  python3 dice_cup.py [-h] [-v] [-q] [-d] [-m] [-g] [-s] [-t]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.\n')
    print('  -v Displays the version of dice_cup.\n')
    print('  -q Quiet Mode: only displays the Group roll outcomes delimited by a comma.')
    print('     Sets are separated by a new line; one Set is printed per line.\n')
    print('  -d Specify the combination and die type(s) to roll.  Single or multiple')
    print('     parameter pairs may be entered to combine various die types.  The')
    print('     input pairs must be POSITIVE INTEGERS separated by a \',\'.  An example')
    print('     of the format for these parameters is listed below:\n')
    print('     INPUT FORMAT {\'-d\' input / parameter pairs}')
    print('       Single die types: \'-d A,B\', where A > 0 and B > 1, yields a')
    print('         die roll of \'A\' combinations of \'B\'-sided dice.  The input')
    print('         \'-d 1,6\' will roll a single six-sided die, or \"1(d6)\".  While')
    print('         the input \'-d 2,10\' will roll two ten-sided dice, or \"2(d10)\".\n')
    print('       Multiple die types: \'-d A,B C,D ... Y,Z\' yields multiple dice')
    print('         rolled together in form \"A(dB) + C(dD) + ... + Y(dZ)\", where the')
    print('         first number of each parameter pair must be greater than 0, while')
    print('         the second number of each pair must be greater than 1.  The input')
    print('         \'-d 1,6 2,4 4,3\' will roll \"1(d6) + 2(d4) + 4(d3)\".\n')
    print('  -m Add or subtract a modifier to a roll; addition is the default action.')
    print('     <defaults to m = 0>')
    print('     *Note: for NEGATIVE modifiers, some OSs may require the \'-\' to be escaped.')
    print('         i.e. for a (-4) modifier, the appropriate (escaped) flag would be')
    print('               \'-m \-4\' or \'-m \'-4\'\'.')
    print('              for a (+7) modifier, the appropriate flag is \'-m 7\'.\n')
    print('  -g Define the number of dice combos you wish to roll in a \"Group\" at once.')
    print('     Such as rolling a Group of three combos of two six-sided dice,')
    print('     or \"3[2(d6)]\".  <defaults to g = 1>\n')
    print('  -s Define how many \"Sets\" (multiple Groups) you wish to roll.  Such as,')
    print('     two Sets of Groups containing three combos of two six-sided dice,')
    print('     or \"2{3[2(d6)]}\".  <defaults to s = 1>\n')
    print('  -t Print the total sum of the Group rolls in a Set; listed as \"Group Total\".')
    print('\nOUTPUT FORMAT\n  Note that dice_cup has two modes of output:\n')
    print('   1. Standard Mode: will print the Set number, a single line for each dice')
    print('      roll in the Group, the \"Ideal Average\" (probabilistic), and the \"Group')
    print('      Average" (actually rolled).  NOTE: if the \'-t\' flag is set, then the')
    print('      Group Total will be printed the line after the Group Average.\n')
    print('      The dice_cup output format for two Sets with multiple rolls in a Group:')
    print('        --\n        Set 1\n        --')
    print('        \'1\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        \'2\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        \'.\' | \'              .              \' : \'   .   \'')
    print('        \'.\' | \'              .              \' : \'   .   \'')
    print('        \'.\' | \'              .              \' : \'   .   \'')
    print('        \'N\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        --\n        Ideal Average: \'X1\'\n        Group Average: \'Y1\'')
    print('        --\n        Set 2\n        --')
    print('        \'1\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        \'2\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        \'.\' | \'              .              \' : \'   .   \'')
    print('        \'.\' | \'              .              \' : \'   .   \'')
    print('        \'.\' | \'              .              \' : \'   .   \'')
    print('        \'N\' | \'roll combination +\\- modifier\' : \'outcome\'')
    print('        --\n        Ideal Average: \'X2\'\n        Group Average: \'Y2\'')
    print('\n   2. Quiet Mode: will only output a single Set of Group rolls per line, roll')
    print('        outcomes will be separated by a \',\' (comma).')
    print('\nEXAMPLES\n  python3 dice_cup.py -d 1,6 -g 3')
    print('    Prints the Standard Mode output for \"3[1(d6)]\" rolls.')
    print('\n  python3 dice_cup.py -d 3,8 -m 5 -g 2')
    print('    Prints the Standard Mode output for \"2[3(d8)+5]\" rolls.')
    print('\n  python3 dice_cup.py -d 1,10 2,6 -g 4 -m 10 -s 5')
    print('    Prints the Standard Mode output for \"5{4[1(d10)+2(d6)+10]}\" rolls.')
    print('\n  python3 dice_cup.py -q -d 3,6 2,4 1,32 -m \-20 -g 30 -s 2')
    print('    Prints the Quiet Mode output for \"2{30[3(d6)+2(d4)+1(d32)-20]}\" rolls.')
    sys.exit()

if args.d:
    p_list = []
    m_str = str(args.m)
    g_len = len(str(args.g))
    for x in args.d:
        d_pair = x.split(',')
        #Check the -d parameter list for input errors...
        if len(d_pair) != 2:
            print('Input Error: flag \'-d\' parameter %r must be a pair of positive integers \'A,B\'.' % x)
            print('             Please read the dice_cup help by invoking the \'-h\' flag.')
            sys.exit(1)
        try:
            if (int(d_pair[0]) < 1) or (int(d_pair[1]) < 2):
                print('Input Error: flag \'-d\' parameter %r is out of range; \'A,B\' must have the' % x)
                print('             MINIMUM VALUES of A = 1 & B = 2; please read the dice_cup help.')
                sys.exit(1)
        except ValueError:
            print('Input Error: flag \'-d\' parameter %r must contain POSITIVE INTEGERS only.' % x)
            print('             Please read the dice_cup help by invoking the \'-h\' flag.')
            sys.exit(1)
        p_list.append(d_pair)#Store the sane -d parameter list
    a_ideal = 0;
    for z in p_list:
        z0_int = int(z[0])
        z1_int = int(z[1])
        a_ideal += (z0_int * ((z1_int + 1) / 2)) #Calculate the Ideal average
    a_ideal += args.m
    for y in range(args.s):
        t_group = 0
        if not args.q:
            print('--\nSet', (y+1))
            print('--')
        for x in range(args.g):
            r = 0
            if not args.q:
                print(repr(x+1).rjust(g_len), '|', end = ' ')
            for z in p_list:
                z0_int = int(z[0])
                z1_int = int(z[1])
                r += d_roll(os.urandom(16), z1_int, z0_int)
                if not args.q:
                    print(z[0]+'(d'+z[1]+') +', end = ' ')
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
            print('--\nIdeal Average:', a_ideal)
            print('Group Average:', a_group)
        if args.t and not args.q:
            print('Group Total:', t_group)
    sys.exit()

parser.print_help()
