#!/usr/bin/env python3
#----------------
#Name: dice_cup
#Version: 1.0.0
#Date: 2015-04-23
#----------------

import os
import sys
import argparse
import random

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome to dice_cup, a CLI-based dice rolling program.')
parser.add_argument("-h", action='store_true', help="Display the help page.")
parser.add_argument("-v", action='store_true', help="Display version information.")
parser.add_argument("-q", action='store_true', help="Quiet Mode: only display rolled numbers.")
parser.add_argument("-c", nargs='?', type=int, help="Set combination of dice to roll.", metavar='# dice')
parser.add_argument("-d", nargs='?', type=int, help="(REQUIRED) Define the dice type to roll.", metavar='# type')
parser.add_argument("-m", nargs='?', type=int, help="Add or subtract a roll modifier.", metavar='# or \-#')
parser.add_argument("-n", nargs='?', type=int, help="Define the number of rolls in a group.", metavar='# rolls')
parser.add_argument("-s", nargs='?', type=int, help="Define the number of sets to roll.", metavar='# sets')
args = parser.parse_args()

version = "1.0.0"

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

n = 1 #Set the default number of dice to roll.
c = 1 #Set the default dice combination.
m = 0 #Set the default modifier value
s = 1 #Set the default set value

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

if args.n and args.n > 0:
    n = args.n

if args.c and args.c > 0:
    c = args.c

if args.s and args.s > 0:
    s = args.s

if args.m:
    m = args.m

if args.d and args.d > 1:
    c_str = str(c)
    d_str = str(args.d)
    m_str = str(m)
    n_len = len(str(n))
    for y in range(s):
        a = 0 #Initialize the average counter to 0
        if not args.q:
            print('-----\nSet', (y+1))
        print('-----')
        for x in range(n):
            r = d_roll(os.urandom(16), args.d, c, m) #Pass d_roll 16 bytes of OS entropy
            if args.q: #Quiet Mode
                print(r)
            else:
                if m < 0: #If the roll modifier is negative, adjust printed output for "-" instead of "+"
                    print(repr(x+1).rjust(n_len), '|', c_str+'(d'+d_str+')'+m_str+' :', r)
                else:
                    print(repr(x+1).rjust(n_len), '|', c_str+'(d'+d_str+')+'+m_str+' :', r)
                a += r
        if not args.q:
            a = a / n #Calculate roll average.
            r = (c * ((args.d + 1) / 2)) + m #Calculate the ideal average. 
            print('-----\nIdeal Average:', r)
            print('Group Average:', a) 
    sys.exit()

parser.print_help()
