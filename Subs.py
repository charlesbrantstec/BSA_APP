import decimal
from decimal import Decimal
import pandas as pd
import re
import sys


textfile = open(sys.argv[1], 'r')
#pc
# name = sys.argv[1].split('\\')[-1].split('.QIF')[0]
#mac
name = sys.argv[1].split('/')[-1].split('.QIF')[0]
# textfile = open('REIFAST CONSTRUCTION.QIF', 'r')
# name = 'reifast'
filetext = textfile.read()
textfile.close()

##################################################
# GET YEARLY TOTALS BY SUB                       #
##################################################


