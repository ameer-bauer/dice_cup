# dice_cup
----
Hi, dice_cup is a CLI dice roll simulator written for Python 3.x; it
has support for arbitrary die types, combinations, modifiers, and
groupings, just to name a few features.  It is designed to be a dice
rolling engine for use with other programs or a GUI, but it works well
on its own. 
~The help screen is below, enjoy.~

Introduction to dice_cup 1.1.4
  Hello, dice_cup is a CLI program written in Python 3 to simulate
  the outcome of various types of dice rolls.  Die types can be set
  arbitrarily greater than 1, making for fun dice types like an eleven-
  sided die, or "1(d11)".  The nomenclature for die rolls herein is as
  follows: "set { group [ number ( die type ) +\- modifier ] }"

SYNTAX
  python3 dice_cup.py [-h] [-v] [-q] [-d] [-m] [-g] [-s] [-t] [-l] [-u]

ARGUMENTS
  -h Displays this help page.

  -v Displays the version of dice_cup.

  -q Quiet Mode: only displays the Dice Group roll outcomes delimited by a ','
     comma. Sets are separated by a new line, only one Set is printed per line.

  -d Specify the die type and number to roll.  Single or multiple
     parameter pairs may be entered to combine various die types.  The
     input pairs must be integers T,N separated by a ','.  An example
     of the format for these parameters is listed below:

     INPUT FORMAT '-d T1,N1 [T2,N2 ... Tn,Nn]'
       Single die types: '-d T,N', where type (T) > 1 and number (N) != 0,
         yields 'N' numbers of 'T'-sided dice rolled together.  The
         input '-d 6,1' will roll a single six-sided die, or "1(d6)".  While
         the input '-d 10,2' will roll two ten-sided dice, or "2(d10)".

       Multiple die types: '-d T1,N1 T2,N2 ... Tn,Nn' yields multiple dice
         rolled together in form "N1(dT1) + N2(dT2) + ... + Nn(dTn)", where
         the first number of each parameter pair must be greater than 1,
         while the second number of each pair must not be equal to 0.  The
         input '-d 6,1 4,-2 3,4' will roll "1(d6) - 2(d4) + 4(d3)".

  -m Add or subtract a modifier to a roll; addition is the default action.
     <defaults to m = 0>
     *Note: for NEGATIVE modifiers, some OSs may require the '-' to be escaped.
         i.e. for a (-4) modifier, the appropriate non-escaped flag would be
              '-m -4'
              for a (-4) modifier, the appropriate escaped flag values may be
              '-m \-4' or possibly '-m '-4''
              for a (+7) modifier, the appropriate flag is '-m 7'

  -g Define the number of "Dice Groups" you wish to roll in a single Set.
     Such as rolling a group of three Dice Groups of two six-sided dice,
     or "3[2(d6)]".  <defaults to g = 1>

  -s Define how many "Sets" of Dice Groups you wish to roll.  Such as,
     two Sets each containing three Dice Groups of two six-sided dice,
     or "2{3[2(d6)]}".  <defaults to s = 1>

  -t Print the total sum of the Group rolls in a Set; listed as "Group Total".

OUTPUT FORMAT
  Note that dice_cup has two modes of output:

   1. Standard Mode: will print the Set number, a single line for each dice
      roll in the Group, the "Ideal Average" (probabilistic), and the "Group
      Average" (actual roll outcome).  NOTE: if the '-t' flag is set, then the
      Group Total will be printed the line after the Group Average.

      The dice_cup output format for two Sets with multiple rolls in a Group:
        ---
        Set 1
        ---
        'Group 1' | 'roll combination +\- modifier' : 'outcome'
        'Group 2' | 'roll combination +\- modifier' : 'outcome'
            .     | '              .              ' : '   .   '
            .     | '              .              ' : '   .   '
            .     | '              .              ' : '   .   '
        'Group n' | 'roll combination +\- modifier' : 'outcome'
        ---
        Ideal Average: 'X1'
        Group Average: 'Y1'
        ---
         .
         .
         .
        ---
        Set n
        ---
        'Group 1' | 'roll combination +\- modifier' : 'outcome'
        'Group 2' | 'roll combination +\- modifier' : 'outcome'
            .     | '              .              ' : '   .   '
            .     | '              .              ' : '   .   '
            .     | '              .              ' : '   .   '
        'Group n' | 'roll combination +\- modifier' : 'outcome'
        ---
        Ideal Average: 'X2'
        Group Average: 'Y2'

   2. Quiet Mode: will only output a single Set of Group rolls per line,
                    results will be printed as a comma separated list.

EXAMPLES
  python3 dice_cup.py -d 6,1 -g 3
    Prints the Standard Mode output for "3[1(d6)]" rolls.

  python3 dice_cup.py -d 8,3 -m -5 -g 2
    Prints the Standard Mode output for "2[3(d8)-5]" rolls.

  python3 dice_cup.py -d 10,1 6,2 -g 4 -m 10 -s 5
    Prints the Standard Mode output for "5{4[1(d10)+2(d6)+10]}" rolls.

  python3 dice_cup.py -q -d 6,3 4,-2 32,1 -m -20 -g 30 -s 2
    Prints the Quiet Mode output for "2{30[3(d6)-2(d4)+1(d32)-20]}" rolls.
