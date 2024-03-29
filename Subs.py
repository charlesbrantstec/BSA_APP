import decimal
from decimal import Decimal
import pandas as pd
import re
import sys
import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


# textfile = open(sys.argv[1], 'r')
# name = sys.argv[1].split('\\')[-1].split('.QIF')[0]
textfile = open(r'C:\Users\12158\Desktop\BSA_APP\QIF\REIFAST CONSTRUCTION INC.QIF', 'r')
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
                                subs.update({sub: Decimal('0')})
                                value = Decimal((item1[2][2:]).replace(',', ''))
                                subs[sub] += value

    total = Decimal('0')
    for key, value in subs.items():
        total += value

    df = pd.DataFrame(columns=['Subcontractor', '2022 Total'])
    # df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)

    for key, value in subs.items():
        df = df.append({'Subcontractor': key, '2022 Total': value}, ignore_index=True)

    # df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)
    # df = df.append({'Subcontractor':'TOTAL', '2022 Total':total}, ignore_index=True)
    print(df)
    return df    



# pc
# df.to_csv('C:/Users/12158/Desktop/BSA_APP/'+name+' - Subcontractors Payments.csv', index=False)

# mac
# df.to_csv('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/'+name+' - Subcontractors Totals.csv', index=False)

# print(df)

##################################################
# GET INFO FOR SUBS                              #
##################################################
# NEEED TO REFACTOR TO USE BSA_DB NOT JSON #######

with open('Subs.json', 'r') as f:
    data = json.loads(f.read())

json_df = pd.json_normalize(data, record_path=['subcontractors'])

# print(json_df)
# print(jsonDf)

def subs_info_df():
    tdf = pd.DataFrame(columns=['Name','Address','EIN','Total'])
    sub_df = subs_df()  
    for subcontractor in sub_df['Subcontractor']:
        fuzz_dict = {}
        total = sub_df[sub_df['Subcontractor'] == subcontractor]['2022 Total'].to_string(index=False)
        address = ''
        for index, row in json_df.iterrows():
            sub = row['name']
            address = row['address']
            ein = row['ein']
            fuzz_dict.update({sub: fuzz.partial_ratio(subcontractor.upper(), sub.upper())})
            max = 0
            match = ''
            for key, value in fuzz_dict.items():
                if value > max:
                    max = value
                    match = key
                if max < 98:
                    match = subcontractor
            if match == subcontractor:
                address = 'N\A'
                ein = 'N\A'
            else:
                address = json_df[json_df['name'] == match]['address'].to_string(index=False)
                ein = json_df[json_df['name'] == match]['ein'].to_string(index=False)
            if len(address) == 0:
                address = 'N/A'
            if len(ein) == 0:
                ein = 'N/A'
        new_row = pd.DataFrame({'Name' : [match], 'Address': [address], 'EIN' : [ein], 'Total' : [total]})
        ndf = pd.concat([tdf, new_row])
        tdf = ndf
        # print(match + '\n' + address + '\n' + ein)
        # print('Total:' + total + '\n')
    # print(ndf)
    return ndf
                                   
# print(subs_info_df())

subs_df()

