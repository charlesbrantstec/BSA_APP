import decimal
from decimal import Decimal
import pandas as pd
import re
import sys
import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
df = pd.DataFrame

def subs_df():
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

    df = pd.DataFrame(columns=['Subcontractor', '2022 Total'])
    # df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)

    for key,value in subs.items():
        df = df.append({'Subcontractor': key, '2022 Total' : value}, ignore_index=True)

    # df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)
    # df = df.append({'Subcontractor':'TOTAL', '2022 Total':total}, ignore_index=True)
    return df

# pc
# df.to_csv('C:/Users/12158/Desktop/BSA_APP/'+name+' - Subcontractors Payments.csv', index=False)

# mac
# df.to_csv('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/'+name+' - Subcontractors Totals.csv', index=False)

# print(df)

##################################################
# GET INFO FOR SUBS                              #
##################################################

with open('Subs.json','r') as f:
    data = json.loads(f.read())

json_df = pd.json_normalize(data, record_path = ['subcontractors'])

print(json_df)
# print(jsonDf)

def subs_info_df():
    for subcontractor in subs_df()['Subcontractor']:
        fuzz_dict = {}
        for sub in json_df['name']:
            fuzz_dict.update({sub:fuzz.partial_ratio(subcontractor.upper(),sub.upper())})
            max = 0
            for key,value in fuzz_dict.items():
                if value > max:
                    max = value
            val_list = list(fuzz_dict.values())
            key_list = list(fuzz_dict.keys())
            position = val_list.index(max)
            true_sub = key_list[position]
            for row in json_df.iterrows():
                if row['name'] == true_sub:
                    print(''+row['name']+'\n'+row['address']+'\n'+row['ein'])
                for row in subs_df().iterrows():
                    if row['Subcontractor'] == subcontractor:
                        print('Total: ' + row['2022 Total'])




            # print(sub + ':' +str(fuzz.partial_ratio(subcontractor.upper(),sub.upper())))
            

# print(subs_df())
subs_info_df()