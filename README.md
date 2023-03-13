# dice_cup
----
Hi, dice_cup is a CLI dice roll simulator written for Python 3.  It
has support for arbitrary die types, combinations, modifiers, and
groupings, just to name a few features.  It is designed to be a dice
rolling engine for use with other programs or a GUI, but it works well
on its own.

The help screen is below, enjoy...

Introduction to dice_cup 1.1.8
  Hello, dice_cup is a CLI program written in Python 3 to simulate
  the outcome of various types of dice rolls.  Die types can be set
  arbitrarily greater than 1, making for fun die types such as an eleven-
  sided die, or "1(d11)".  The nomenclature for die rolls herein is as
  follows: 
  "set { dice group [ number ( die type ) +\- modifier ] }"

SYNTAX

  dice_cup.py [-h] [-v] [-q] [-d] [-m] [-g] [-s] [-i] [-l] [-u]

ARGUMENTS

  -h Displays this help page.

  -v Displays the version of dice_cup.

  -q Quiet Mode: only outputs Dice Group roll(s) results delimited by a ','
     comma. Only one Set is displayed per line.

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

  -l Set an integer value as the Lower Bound for all Dice Groups.  Results that
     are trimmed will be displayed as 'LB' in the Dice Group outcome.
     If all results in a Set of Dice Group(s) are trimmed, both Set Average and
     Set Total will output a value of 'DNE' representing "Does Not Exist".

  -u Set an integer value as the Upper Bound for all Dice Groups.  Results that
     are trimmed will be displayed as 'UB' in the Dice Group outcome.
     If all results in a Set of Dice Group(s) are trimmed, both Set Average and
     Set Total will output a value of 'DNE' representing "Does Not Exist".

  -m Add or subtract a an integer value, a "modifier", from a Dice Group.
     i.e. add a +5 modifier with '-m 5' or subtract a -3 modifier with '-m -3'.
     Note: for NEGATIVE modifiers, some OSs may require the '-' to be escaped.
           e.g. for a -4 modifier, the appropriate escaped flag values may be
                '-m \-4' or possibly '-m '-4''.

  -g Define the number of "Dice Groups" you wish to roll in a single Set.
     Such as rolling a group of three Dice Groups of two six-sided dice,
     or "3[2(d6)]".

  -s Define how many "Sets" of Dice Groups you wish to roll.  Such as,
     two Sets each containing three Dice Groups of two six-sided dice,
     or "2{3[2(d6)]}".

  -i Prints statistical information about the Dice Group rolls of a Set:
       a) the "Ideal Average", or theoretic probabilistic average, of a Set
       b) the "Set Average", or actual rolled average, of a Set
       c) the "Set Total", or the sum total of rolls, of a Set
       d) the "Set High", or the highest roll of a Set
       e) the "Set Low", or the lowest roll of a Set
     If '-i' is used in Quiet Mode, a new line with the Ideal Average, Set
     Average, Set Total, Set High, and Set Low will be printed below each
     Set's result list as a 5-tuple in the aforementioned order.

OUTPUT FORMAT
  Note that dice_cup has two modes of output:

    1) Standard Mode: will print the Set number and a single line for each
       Dice Group rolled.  If the '-i' flag is set, the "Ideal Average",
       "Set Average", and "Set Total" will be displayed after the Dice
       Group rolls; below a '---' delimiter.

       The dice_cup Standard Mode output format is as follows:

         =====
         Set 1
         =====
         Lower Bound = 'lower bound value'
         Upper Bound = 'upper bound value'
         ---
         'Group 1' | 'roll combination +\- modifier' : 'outcome'
         'Group 2' | 'roll combination +\- modifier' : 'outcome'
             .     |                .                :     .
             .     |                .                :     .
             .     |                .                :     .
         'Group n' | 'roll combination +\- modifier' : 'outcome'
          .
          .
          .
         =====
         Set n
         =====
         Lower Bound = 'lower bound value'
         Upper Bound = 'upper bound value'
         ---
         'Group 1' | 'roll combination +\- modifier' : 'outcome'
         'Group 2' | 'roll combination +\- modifier' : 'outcome'
             .     |                .                :     .
             .     |                .                :     .
             .     |                .                :     .
         'Group n' | 'roll combination +\- modifier' : 'outcome'

    2) Quiet Mode: only outputs the final result(s) of Dice Group(s), listing
       one Set per line.  Results will be printed as a comma separated list.

EXAMPLES
  dice_cup.py -d 6,3
    Prints the Standard Mode output for a single "3(d6)" roll.

  dice_cup.py -d 8,4 -m -5 -g 2
    Prints the Standard Mode output for "2[4(d8)-5]" rolls.

  dice_cup.py -d 23,1 4,-2 -l -2 -u 18 -g 2 -i
    Prints the Standard Mode output for "2[1(d23)-2(d4)]" rolls with a Lower
    Bound of -2, an Upper Bound of 18, and statistical information displayed.

  dice_cup.py -d 10,1 6,2 -g 4 -m 10 -s 5
    Prints the Standard Mode output for "5{4[1(d10)+2(d6)+10]}" rolls.

  dice_cup.py -q -d 6,3 4,-2 32,1 -m -20 -g 30 -s 2
    Prints the Quiet Mode output for "2{30[3(d6)-2(d4)+1(d32)-20]}" rolls.
