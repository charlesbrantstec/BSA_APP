from quiffen import Qif
import decimal
from decimal import Decimal
import pandas as pd
import re
import sys

# textfile = open(sys.argv[1], 'r')
# name = sys.argv[1].split('\\')[-1].split('.QIF')[0]
textfile = open('REIFAST CONSTRUCTION.QIF', 'r')
name = 'REIFAST CONSTRUCTION'
filetext = textfile.read()
textfile.close()

##################################################
# GET TOTALS FOR SUBS                            #
##################################################
start = '!Clear:AutoSwitch\n!Option:AutoSwitch'
raw = (filetext.split(start)[1]).split('^')
subs = set()
subs = {}

# get list of subs
for item in raw:
    item1 = item.split('\n')
    # if raw[1] contains '22 then we count the expense
    if bool(re.search('\'22', item1[1])):
        # 'U-' indicates an expense
        if bool(re.search('U-', item1[2])):
            if 'LSubcontractors' in item1:
                for str in item1:
                    if str.startswith('P'):
                        sub = str[1:]
                        if sub not in subs:
                            subs.update({sub:Decimal('0')})
                            value = Decimal((item1[2][2:]).replace(',',''))
                            subs[sub] += value

total = Decimal('0')
for key, value in subs.items():
    total += value

# format Decimals to strings
# for key,value in subs.items():
#     subs[key] = "{:.2f}".format(value)

# print(subs)

df = pd.DataFrame(columns=['Subcontractor', '2022 Total'])
df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)

for key,value in subs.items():
    df = df.append({'Subcontractor': key, '2022 Total' : value}, ignore_index=True)

df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)
df = df.append({'Subcontractor':'TOTAL', '2022 Total':total}, ignore_index=True)

df.to_csv('C:/Users/12158/Desktop/BSA_APP/'+name+' - Subcontractors Payments.csv', index=False)

print(df)

