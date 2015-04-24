#!/usr/bin/env python3
#----------------
#Name: dice_cup
#Version: 1.0.2
#Date: 2015-04-24
#----------------

import os
import sys
import argparse
import random

def pos_int(p): #a funtion for argparse 'type' to call for checking input values
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
parser.add_argument("-c", nargs='?', default=1, type=pos_int, help="Set combination of dice to roll.", metavar='# (dice)')
parser.add_argument("-d", nargs='?', type=int, help="*REQUIRED* Set the dice type to roll.", metavar='# (type)')
parser.add_argument("-m", nargs='?', default=0, type=int, help="Add or subtract a roll modifier.", metavar='# or \-#')
parser.add_argument("-n", nargs='?', default=1, type=pos_int, help="Set the number of rolls in a group.", metavar='# (rolls)')
parser.add_argument("-s", nargs='?', default=1, type=pos_int, help="Define how many \'sets of groups\' to roll.", metavar='# (sets)')
args = parser.parse_args()

version = "1.0.2"

if args.v:
    print('dice_cup version:', version)
    sys.exit()

if args.h:
    print('Introduction to dice_cup', version)
    print('  Hello, dice_cup is a CLI program written in Python 3.x to simulate')
    print('  the outcome of various types of dice rolls. Die types can be set')
    print('  arbitrarily greater than 1, making for fun dice types like (d11).')
    print('\nSYNTAX\n  python3 dice_cup.py [-h] [-v] [-q] [-c] [-d] [-m] [-n] [-s]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.\n')
    print('  -v Displays the version of dice_cup.\n')
    print('  -q Quiet Mode: Only displays a set marker and roll outcomes followed')
    print('     by a new line.\n')
    print('  -c Choose a combination of the specified dice to roll, such as three six-')
    print('     sided dice, or 3(d6).')
    print('     <defaults to c = 1>\n')
    print('  -d Specify the dice type, such as \'-d 6\' for a six-sided die, or a (d6),')
    print('     and \'-d 100\' for a percentile die, or a (d100).\n')
    print('  -m Add or subtract a modifier to a roll; addition is the default action.')
    print('     <defaults to m = 0>')
    print('     **Note: to enter a NEGATIVE number, the \'-\' must be escaped.')
    print('             i.e. for a (-4) modifier, the appropriate flag is \'-m \-4\'.')
    print('                  for a (+7) modifier, the appropriate flag is \'-m 7\'.\n')
    print('  -n Define the number of dice combos you wish to roll in a group at once.')
    print('     Such as, rolling a group of three combos of two six-sided dice,')
    print('     or 3[2(d6)+0].')
    print('     <defaults to n = 1>\n')
    print('  -s Define how many sets of groups you wish to roll. Such as, two sets of')
    print('     groups containing three combos of two six-sided dice, or 2{3[2(d6)+0]}.')
    print('     <defaults to s = 1>')
    print('\nOUTPUT FORMAT\n  Note that dice_cup has two modes of output:\n')
    print('   1. Standard Mode: will print the set number, a single line for each dice')
    print('      roll in the group, the Ideal (probabilistic) average, and the Group')
    print('      (actually rolled) average.\n')
    print('      The dice_cup output for a single set with multiple rolls in a group:')
    print('        -----\n        Set 1\n        -----')
    print('        \'1\' | \'roll combination\' : \'outcome\'')
    print('        \'2\' | \'roll combination\' : \'outcome\'')
    print('        \'.\' | \'        .       \' : \'   .   \'')
    print('        \'.\' | \'        .       \' : \'   .   \'')
    print('        \'.\' | \'        .       \' : \'   .   \'')
    print('        \'N\' | \'roll combination\' : \'outcome\'')
    print('        -----\n        Ideal Average: \'X\'\n        Group Average: \'Y\'')
    print('\n   2. Quiet Mode: will just simply output a set marker (\'-----\') and')
    print('      a single roll outcome, per line, of the group.')
    print('\nEXAMPLES\n  python3 dice_cup.py -d 6 -n 3')
    print('    Prints the Standard Mode output for 3[1(d6)] rolls.')
    print('\n  python3 dice_cup.py -c 3 -d 8 -m 10 -n 2')
    print('    Prints the Standard Mode output for 2[3(d8)+10] rolls.')
    print('\n  python3 dice_cup.py -c 4 -d 10 -n 3 -s 5')
    print('    Prints the Standard Mode output for 5{4[3(d8)+10]} rolls.')
    print('\n  python3 dice_cup.py -q -d 100 -m \-20 -n 30 -s 2')
    print('    Prints the Quiet Mode output for 2{30[1(d100)-20]} rolls.')
    sys.exit()

if args.d and args.d > 1:
    c_str = str(args.c)
    d_str = str(args.d)
    m_str = str(args.m)
    n_len = len(str(args.n))
    for y in range(args.s):
        a = 0 #Initialize the average counter to 0
        if not args.q:
            print('-----\nSet', (y+1))
        print('-----')
        for x in range(args.n):
            r = d_roll(os.urandom(16), args.d, args.c, args.m) #Pass d_roll 16 bytes of OS entropy
            if args.q: #Quiet Mode
                print(r)
            else:
                if args.m < 0: #If the roll modifier is negative, adjust printed output for "-" instead of "+"
                    print(repr(x+1).rjust(n_len), '|', c_str+'(d'+d_str+')'+m_str+' :', r)
                else:
                    print(repr(x+1).rjust(n_len), '|', c_str+'(d'+d_str+')+'+m_str+' :', r)
                a += r
        if not args.q:
            a = a / args.n #Calculate roll average.
            r = (args.c * ((args.d + 1) / 2)) + args.m #Calculate the ideal average. 
            print('-----\nIdeal Average:', r)
            print('Group Average:', a) 
    sys.exit()

parser.print_help()
