#!/usr/bin/env python3
#----------------
#Name: dice_cup
#Version: 1.1.13
#Date: 2016-10-09
#----------------

import os
import sys
import argparse
import random

version = "1.1.13"

def pos_int(p): #a function for argparse 'type' to call for checking input values
    int_p = int(p)
    if int_p <= 0:
        msg = "%r is not a positive integer." % p
        raise argparse.ArgumentTypeError(msg)
    return int_p

def d_roll(s, t = 6, c = 1, m = 0, l = False, h = False):
    #Dice rolling: (random integer in range from 1 -> t (dice type)
    #Default input, with s defined, yields roll = 1(d6)+0
    #d_roll with parameters set yield a roll = c(dt)+m
    #s is the seed for the RNG, use at LEAST 8 bytes of random data
    #l is the drop the lowest roll flag
    #h is the drop the highest roll flag
    #NOTE: either l, or h, may be set, not both; l takes precedence
    roll = 0
    random.seed(s)
    roll_sample = 0
    first_run = True
    roll_low = 0
    roll_high = 0
    
    if c > 0:
        for x in range(c):
            roll_sample = random.randint(1, t)
            if first_run:
                roll_low = roll_sample
                roll_high = roll_sample
                first_run = False
            elif roll_sample < roll_low:
                roll_low = roll_sample
            elif roll_sample > roll_high:
                roll_high = roll_sample
            roll += roll_sample
    elif c == 0:
        return(m)
    else:
        c = abs(c)
        for x in range(c):
            roll_sample = random.randint(1, t)
            if first_run:
                roll_low = roll_sample
                roll_high = roll_sample
                first_run = False
            elif roll_sample < roll_low:
                roll_low = roll_sample
            elif roll_sample > roll_high:
                roll_high = roll_sample
            roll -= roll_sample
    
    if l:
        roll -= roll_low
    elif h:
        roll -= roll_high
    
    return(roll + m)

def d_err():
    print('Error: the flag \'-d\' parameter %r is incorrect.  Only integer pairs of the' % x)
    print('       form \'T,N\' having constraints of T > 1 and N != 0 are supported.')
    print('       Please read the dice_cup help by running \'dice_cup -h\'.')
    return

def h_main():
    print('Introduction to dice_cup', version)
    print('  Hello, dice_cup is a CLI program written in Python 3 to simulate')
    print('  the outcome of various types of dice rolls.  Die types can be set')
    print('  arbitrarily greater than 1, making for fun die types such as an eleven-')
    print('  sided die, or \"1(d11)\".\n')
    print('  The nomenclature for die rolls herein is as follows:')
    print('    \"set {dice group [(number (die type) + ... +\\- modifier) +\\- percentage]}\"')
    print('\nSYNTAX\n  dice_cup.py [-h] [-v] [-q] [-d] [-m] [-p] [-g] [-s] [-i]')
    print('              [-l] [-u] [-L] [-H]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.\n')
    print('  -v Displays the version of dice_cup.\n')
    print('  -q Quiet Mode: only outputs Dice Group roll(s) results delimited by a \',\'')
    print('     comma. Only one Set is displayed per line.\n')
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
    print('  -L Drop the lowest roll of the first dice number within each Dice Group.')
    print('     \"Drop Lowest\" will appear before each die number to be modified.')
    print('     i.e. to roll 3[4(d6)+1(d4)], dropping the lowest d6 roll, the following')
    print('     syntax would be appropriate: \'dice_cup -d 6,4 4,1 -g 3 -L\'\n')
    print('  -H Drop the highest roll of the first dice number within each Dice Group.')
    print('     \"Drop Highest\" will appear before each die number to be modified.')
    print('     i.e. to roll 5[3(d8)+2(d6)], dropping the highest d8 roll, the following')
    print('     syntax would be appropriate: \'dice_cup -d 8,3 6,2 -g 5 -H\'\n')
    print('  -l Set an integer value as the Lower Bound for all Dice Groups.  Results that')
    print('     are trimmed will be displayed as \'LB\' in the Dice Group outcome.')
    print('     If all results in a Set of Dice Group(s) are trimmed, both Set Average and')
    print('     Set Total will output a value of \'DNE\' representing \"Does Not Exist\".\n')
    print('  -u Set an integer value as the Upper Bound for all Dice Groups.  Results that')
    print('     are trimmed will be displayed as \'UB\' in the Dice Group outcome.')
    print('     If all results in a Set of Dice Group(s) are trimmed, both Set Average and')
    print('     Set Total will output a value of \'DNE\' representing \"Does Not Exist\".\n')
    print('  -m Add or subtract a an integer value, a \"modifier\", from all Dice Groups.')
    print('     i.e. add a +5 modifier with \'-m 5\' or subtract a -3 modifier with \'-m -3\'.')
    print('     Note: for NEGATIVE modifiers, some OSs may require the \'-\' to be escaped.')
    print('           e.g. for a -4 modifier, the appropriate escaped flag values may be')
    print('                \'-m \-4\' or possibly \'-m \'-4\'\'.\n')
    print('  -p Apply an integer value as a \"percentage modifier\" to all Dice Groups.')
    print('     i.e. add 23% to each Dice Group with \'-p 23\' or subtract 50% with \'-p -50\'.')
    print('     Note: for NEGATIVE percentages, some OSs may require the \'-\' to be escaped.')
    print('           e.g. for a -60% modifier, the appropriate escaped flag values may be')
    print('                \'-p \-60\' or possibly \'-p \'-60\'\'.\n')
    print('  -g Define the number of \"Dice Groups\" you wish to roll in a single Set.')
    print('     Such as rolling a group of three Dice Groups of two six-sided dice,')
    print('     or \"3[2(d6)]\".\n')
    print('  -s Define how many \"Sets\" of Dice Groups you wish to roll.  Such as,')
    print('     two Sets each containing three Dice Groups of two six-sided dice,')
    print('     or \"2{3[2(d6)]}\".\n')
    print('  -i Prints statistical information about the Dice Group rolls of a Set:')
    print('       a) \"Ideal Average\": the probabilistic average of a Set')
    print('       b) \"Set Average\": the actual rolled average of a Set')
    print('       c) \"Set Total\": the sum total of rolls in a Set')
    print('       d) \"Set High\": the highest roll of a Set')
    print('       e) \"Set Low\": the lowest roll of a Set')
    print('       f) \"Set Deviation\": the deviation of a Set from the Ideal Average')
    print('     If \'-i\' is used in Quiet Mode, a new line with the Ideal Average, Set')
    print('     Average, Set Total, Set High, Set Low, and Set Deviation will be')
    print('     printed below each Set\'s results list as a 6-tuple in the')
    print('     aforementioned order.')
    print('\nOUTPUT FORMAT\n  Note that dice_cup has two modes of output:\n')
    print('    1) Standard Mode: will print the Set number and a single line for each')
    print('       Dice Group rolled.  If the \'-i\' flag is set, the \"Ideal Average\",')
    print('       \"Set Average\", and \"Set Total\" will be displayed after the Dice')
    print('       Group rolls; below a \'---\' delimiter.\n')
    print('       The dice_cup Standard Mode output format is as follows:\n')
    print('         =====\n         Set 1\n         =====')
    print('         Lower Bound = \'lower bound value\'')
    print('         Upper Bound = \'upper bound value\'\n         ---')
    print('         \'Group 1\' | \'roll combination +\\- modifier\' +\\- % : \'outcome\'')
    print('         \'Group 2\' | \'roll combination +\\- modifier\' +\\- % : \'outcome\'')
    print('             .     |                .                :     .')
    print('             .     |                .                :     .')
    print('             .     |                .                :     .')
    print('         \'Group n\' | \'roll combination +\\- modifier\' +\\- % : \'outcome\'')
    print('          .')
    print('          .')
    print('          .')
    print('         =====\n         Set n\n         =====')
    print('         Lower Bound = \'lower bound value\'')
    print('         Upper Bound = \'upper bound value\'\n         ---')
    print('         \'Group 1\' | \'roll combination +\\- modifier\' +\\- % : \'outcome\'')
    print('         \'Group 2\' | \'roll combination +\\- modifier\' +\\- % : \'outcome\'')
    print('             .     |                .                :     .')
    print('             .     |                .                :     .')
    print('             .     |                .                :     .')
    print('         \'Group n\' | \'roll combination +\\- modifier\' +\\- % : \'outcome\'')
    print('\n    2) Quiet Mode: only outputs the final result(s) of Dice Group(s), listing')
    print('       one Set per line.  Results will be printed as a comma separated list.')
    print('\nEXAMPLES\n  dice_cup.py -d 6,3')
    print('    Prints the Standard Mode output for a single \"3(d6)\" roll.')
    print('\n  dice_cup.py -d 8,4 -m -5 -g 2')
    print('    Prints the Standard Mode output for \"2[4(d8)-5]\" rolls.')
    print('\n  dice_cup.py -d 23,1 4,-2 -l -2 -u 18 -g 2 -i')
    print('    Prints the Standard Mode output for \"2[1(d23)-2(d4)]\" rolls with a Lower')
    print('    Bound of -2, an Upper Bound of 18, and statistical information displayed.')
    print('\n  dice_cup.py -d 10,1 6,2 -g 4 -p 10 -s 5')
    print('    Prints the Standard Mode output for \"5{4[(1(d10)+2(d6))+10%]}\" rolls.')
    print('\n  dice_cup.py -q -d 6,3 4,-2 32,1 -m -20 -g 30 -s 2')
    print('    Prints the Quiet Mode output for \"2{30[3(d6)-2(d4)+1(d32)-20]}\" rolls.')
    return

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome, dice_cup is a CLI-based die roll simulation engine. It utilizes a cryptographic PRNG to accurately simulate various dice rolls.')
parser.add_argument("-h", action='store_true', help="Display the help page")
parser.add_argument("-v", action='store_true', help="Display version information")
parser.add_argument("-q", action='store_true', help="Only display rolled numbers; called \'Quiet Mode\'")
parser.add_argument("-d", nargs='+', type=str, help="Define the types of dice to roll; called a \'Dice Group\'", metavar='#,#')
parser.add_argument("-m", nargs='?', const=0, default=0, type=int, help="Add, or subtract, an integer modifier to each Dice Group", metavar='#')
parser.add_argument("-p", nargs='?', const=0, default=0, type=int, help="Apply an integer percentage modifier to each Dice Group", metavar='%')
parser.add_argument("-l", nargs='?', type=int, help="Define a lower bound for all Dice Groups", metavar='#')
parser.add_argument("-u", nargs='?', type=int, help="Define an upper bound for all Dice Groups", metavar='#')
parser.add_argument("-L", action='store_true', help="Drop the lowest initial roll in all Dice Groups")
parser.add_argument("-H", action='store_true', help="Drop the highest initial roll in all Dice Groups")
parser.add_argument("-g", nargs='?', const=1, default=1, type=pos_int, help="Define how many \'Dice Groups\' to roll in a Set", metavar='#')
parser.add_argument("-s", nargs='?', const=1, default=1, type=pos_int, help="Define how many \'Sets of Dice Groups\' to roll", metavar='#')
parser.add_argument("-i", action='store_true', help="Displays statistical information of each Set rolled")
args = parser.parse_args()

l_check = isinstance(args.l, int)
u_check = isinstance(args.u, int)

if args.v:
    print('dice_cup version:', version)
    sys.exit()

if args.h:
    h_main()
    sys.exit()

if (l_check and u_check):#See if both -l and -u are set and check for errors
    if args.l >= args.u:
        print('Error: the flags \'-l\' and \'-u\' are set, but -l =', args.l, 'and -u =', args.u)
        print('       i.e. the lower bound is either greater than, or equal, to the')
        print('       upper bound.  Please enter new boundary values so that \'-l\' < \'-u\'.')
        sys.exit(1)

if args.L and args.H:#See if both -L and -H are set
    print('Error: the flags \'-L\' and \'-H\' are set, yet only one is allowed.')
    print('       Please select either the \'-L\' or the \'-H\' flag.')
    sys.exit(1)

if args.d:
    d_list = []
    m_str = str(args.m)
    p_str = str(args.p)
    g_len = len(str(args.g))
    s_len = len(str(args.s))
    p_val = (args.p / 100)
    for x in args.d:
        if x.find('+') != -1: #Scan for extra whitespace
            y = x.replace(' ', '')
            y_list = y.split('+')
            d_pair = y_list[0].split(',')
            for z in y_list[1:]:
                args.d.append(z)
        else:
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
        d_list.append(d_pair) #Store the sane -d parameter list
    a_ideal = 0
    a_low = 0
    a_high = 0
    a_roll = 0
    a_drop = 0
    #Scan through the -d parameters to calculate the Ideal Average
    first_run = True
    for z in d_list: #Faster to calculate here, just in case there are multiple groups
        zt_int = int(z[0])
        zg_int = int(z[1])
        a_ideal += (zg_int * ((zt_int + 1) / 2))
        if args.L and first_run:#Calculate the ways to roll the lowest die to drop
            for r in range(1,(zt_int + 1)):
                a_low += (((((zt_int + 1) - r) ** zg_int) - ((zt_int - r) ** zg_int)) * r)
            a_roll += zt_int ** zg_int
        elif args.H and first_run:#Calculate the ways to roll the highest die to drop
            for r in range(1,(zt_int + 1)):
                a_high += (((r ** zg_int) - ((r - 1) ** zg_int)) * r)
            a_roll += zt_int ** zg_int
        first_run = False
    a_ideal += args.m
    if args.p:
        a_ideal += (a_ideal * p_val)
        a_low += (a_low * p_val)
        a_high += (a_high * p_val)
    if args.L:
        a_drop = ((a_ideal * a_roll) - a_low) / a_roll
        a_ideal = a_drop
    elif args.H:
        a_drop = ((a_ideal * a_roll) - a_high) / a_roll
        a_ideal = a_drop
    for y in range(args.s):
        t_set = 0
        c_trim = 0
        g_div = 0
        g_var = 0
        a_set = "DNE"
        s_dev = 0
        r_high = False
        r_low = False
        if not args.q:
            print('=' * (s_len + 4))
            print('Set', repr(y + 1).rjust(s_len))
            print('=' * (s_len + 4))
            if l_check:
                print('Lower Bound =', args.l,)
            if u_check:
                print('Upper Bound =', args.u)
            if (u_check or l_check):
                print('---')
        for x in range(args.g):
            r = 0
            b = 0
            trim = False
            if args.L and (not args.q):
                print('Group',repr(x + 1).rjust(g_len), '| Drop Lowest', end = ' ')
            elif args.H and (not args.q):
                print('Group',repr(x + 1).rjust(g_len), '| Drop Highest', end = ' ')
            elif not args.q:
                print('Group',repr(x + 1).rjust(g_len), '|', end = ' ')
            first_run = True
            for z in d_list: #Generate the dice roll outcomes of the -d parameters
                zt_int = int(z[0])
                zg_int = int(z[1])
                if (l_check or u_check): #See if either -l or -u are set
                    if args.L and first_run:#Check for first dice run of group and L flag
                        b += d_roll(os.urandom(16), zt_int, zg_int, 0, True)
                    elif args.H and first_run:#Check for first dice run of group and H flag
                        b += d_roll(os.urandom(16), zt_int, zg_int, 0, False, True)
                    else:
                        b += d_roll(os.urandom(16), zt_int, zg_int)
                else:
                    if args.L and first_run:#Check for first dice run of group and L flag
                        r += d_roll(os.urandom(16), zt_int, zg_int, 0, True)
                    elif args.H and first_run:#Check for first dice run of group and H flag
                        r += d_roll(os.urandom(16), zt_int, zg_int, 0, False, True)
                    else:
                        r += d_roll(os.urandom(16), zt_int, zg_int)
                first_run = False
                if not args.q:
                    print(z[1]+'(d'+z[0]+') +', end = ' ')
            b += args.m
            if (l_check and u_check): #See if both -l and -u are set
                if ((b >= args.l) and (b <= args.u)):
                    r += b
                    if args.p:
                        r += round((r * p_val))
                    g_var += ((r - a_ideal) ** 2)
                elif b < args.l:
                    trim = "LB["+str(b)+"]"
                    c_trim += 1
                else:
                    trim = "UB["+str(b)+"]"
                    c_trim += 1
            elif l_check:
                if b >= args.l:
                    r += b
                    if args.p:
                        r += round((r * p_val))
                    g_var += ((r - a_ideal) ** 2)
                else:
                    trim = "LB["+str(b)+"]"
                    c_trim += 1
            elif u_check:
                if b <= args.u:
                    r += b
                    if args.p:
                        r += round((r * p_val))
                    g_var += ((r - a_ideal) ** 2)
                else:
                    trim = "UB["+str(b)+"]"
                    c_trim += 1
            else:
                r += args.m
                if args.p:
                    r += round((r * p_val))
                g_var += ((r - a_ideal) ** 2)
            #Calculate the high and low rolls
            if not r_high:
                r_high = r
            elif not trim:
                if r > r_high:
                    r_high = r
            if not r_low:
                r_low = r
            elif not trim:
                if r < r_low:
                    r_low = r
            if not args.q:
                if trim:
                    if args.p and args.m:
                        print('('+m_str+') + ('+p_str+'%) :', trim)
                    elif args.m:
                        print('('+m_str+') :', trim)
                    else:
                        print('\b\b:', trim)
                else:
                    if args.p and args.m:
                        print('('+m_str+') + ('+p_str+'%) :', r)
                    elif args.m:
                        print('('+m_str+') :', r)
                    else:
                        print('\b\b:', r)
            else:
                if (x+1) < args.g:
                    if trim:
                        print(trim, end=',')
                    else:
                        print(r, end=',') 
                else:
                    if trim:
                        print(trim)
                    else:
                        print(r)
            if not trim:
                t_set += r
        g_div = args.g - c_trim 
        if g_div != 0:
            a_set = t_set / g_div #Calculate the Group roll average
            s_dev = ((g_var / g_div) ** (0.5))
        if args.i and not args.q:
            print('---\nIdeal Average:', a_ideal)
            print('Set Average:', a_set)
            if g_div == 0:
                print('Set Total: DNE')
                print('Set High: DNE')
                print('Set Low: DNE')
                print('Set Deviation: DNE')
            else:
                print('Set Total:', t_set)
                print('Set High:', r_high)
                print('Set Low:', r_low)
                print('Set Deviation:', s_dev)
        elif args.i:
            if g_div == 0:
                print(a_ideal, a_set, 'DNE', 'DNE', 'DNE', 'DNE', sep=',')
            else:
                print(a_ideal, a_set, t_set, r_high, r_low, s_dev, sep=',')
    sys.exit()

parser.print_help()
