#!/usr/bin/env python3
#----------------
#Name: dice_cup
#Version: 0.0.2
#Date: 2015-04-22
#----------------

import os
import sys
import argparse
import random

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome to dice_cup, a CLI-based dice rolling program.')
parser.add_argument("-h", action='store_true', help="Display the help page.")
parser.add_argument("-v", action='store_true', help="Display version information.")
parser.add_argument("-q", action='store_true', help="Enable quiet mode; only display rolled numbers.")
parser.add_argument("-c", nargs='?', type=int, help="Set dice combinations to roll.", metavar='combo #')
parser.add_argument("-d", nargs='?', type=int, help="-REQUIRED- Define the dice type to roll.", metavar='die #')
parser.add_argument("-m", nargs='?', type=int, help="Add or subtract a roll modifier.", metavar='+/- #')
parser.add_argument("-n", nargs='?', type=int, help="Set the number of rolls to make.", metavar='roll #')
args = parser.parse_args()

version = "0.0.2"

if args.v:
    print('dice_cup version:', version)
    sys.exit()

if args.h:
    print('Introduction to dice_cup', version)
    print('  Hello, dice_cup is a CLI program written in Python 3.x to simulate')
    print('  the outcome of various types of dice rolls.')
    print('\nSYNTAX\n  python3 dice_cup.py [-h] [-v] [-q] [-c] [-d] [-n]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.\n')
    print('  -v Displays the version of dice_cup.\n')
    print('  -q Quiet Mode: Only display the roll followed by a return character.\n')
    print('  -c Choose a combination of the specified dice to roll, such as 3(d6).\n')
    print('  -d Specify the dice type, such as \'-d 6\' for a 6-sided die (d6) or')
    print('     \'-d 100\' for percentile dice (d100).\n')
    print('  -m Add or subtract a modifier to a roll; addition is the default action.')
    print('     **Note: to enter a NEGATIVE number, the \'-\' must be escaped.')
    print('             i.e. for a (-4) modifier, the appropriate flag is \'-m \-4\'.')
    print('                  for a (+7) modifier, the appropriate flag is \'-m 7\'.\n')
    print('  -n Set the number rolls you wish to make, such as rolling 2(d6) 3 times.\n')
    print('\nOUTPUT FORMAT\n  Note that dice_cup has two \"Modes\" of output:')
    print('    \"Standard Mode\" will print a single line for each dice roll.')
    print('    The format of which looks like:\n      \'roll #\' | \'specified roll\' : \'outcome\'')
    print('      -----\n      Ideal Average: \'X\'\n      Roll  Average: \'Y\'')
    print('\n    \"Quiet Mode\" will just simply render a roll outcome per line.')
    print('\nEXAMPLES\n  python3 dice_cup.py -d 6 -n 3')
    print('    Prints the \"Standard Mode\" output for a single (d6) roll 3 times.')
    print('\n  python3 dice_cup.py -c 3 -d 8 -m 10 -n 2')
    print('    Prints the \"Standard Mode\" output for 3(d8)+10 roll 2 times.')
    print('\n  python3 dice_cup.py -q -d 100 -m \-20 -n 30')
    print('    Prints the \"Quiet Mode\" output for a 1(d100)-20 roll 30 times.')
    sys.exit()

n = 1 #Set the default number of dice to roll.
c = 1 #Set the default dice combination.
m = 0 #Set the initial modifier value

def d_roll (s, t = 6, c = 1, m = 0):
    #Dice rolling: (random integer in range from 1 -> t (dice type)
    #Default input, with s defined, yields roll = 1(d6)+0
    #d_roll with parameters set yield a roll = c(dt)+m
    #s is the seed for the RNG, use at LEAST 8 bytes of random data.
    roll = 0
    random.seed(s)
    for x in range(c):
        roll += random.randint (1, t)
    return (roll + m)

if args.n and args.n > 0:
    n = args.n

if args.c and args.c > 0:
    c = args.c

if args.m:
    m = args.m

if args.d and args.d > 0:
    a = 0 #Initialize the average counter to 0
    c_str = str(c)
    d_str = str(args.d)
    m_str = str(m)
    n_len = len(str(n))
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
    if a:
        a = a / n #Calculate roll average.
        r = (c * ((args.d + 1) / 2)) + m #Calculate the ideal average. 
        print('-----\nIdeal Average:', r)
        print('Roll  Average:', a) 
    sys.exit()

parser.print_help()
