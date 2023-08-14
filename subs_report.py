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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

warnings.filterwarnings("ignore", category=DeprecationWarning)


# textfile = open(sys.argv[1], 'r')
# name = sys.argv[1].split('\\')[-1].split('.QIF')[0]

def match_subs(subs_df):
    subs_v1 = pd.read_excel(r'C:\Users\12158\Desktop\BSA_APP\SUBS 2022 V1.xlsx')
    matched_subs = {}
    unmatched_subs = {}

    for item, row in subs_df.iterrows():
        cmp_name = row['Subcontractor']
        cmp_total = row['2022 Total']
        yr_total = subs_df.loc[subs_df['Subcontractor'] == 'TOTAL', '2022 Total'].item()

        if cmp_name != '******' and cmp_name != 'TOTAL':
            is_matched = False

            for item, row in subs_v1.iterrows():
                v1_name = row['SUB CONTRACTORS NAME']

                partial_ratio = fuzz.partial_ratio(cmp_name.upper(), v1_name)
                ratio = fuzz.ratio(cmp_name.upper(), v1_name)

                if partial_ratio > 90 and ratio > 85:
                    matched_subs.update({v1_name : str(cmp_total)})
                    is_matched = True
                    break

                    # print('PARTIAL RATIO - ' + cmp_name + ', ' + v1_name + ' : ' + str(partial_ratio))
                    # print('RATIO - ' + cmp_name + ', ' + v1_name + ' : ' + str(ratio))
            if not is_matched:    
                unmatched_subs.update({cmp_name : str(cmp_total)})

    for key, value in matched_subs.items():
        subs_v1.loc[subs_v1['SUB CONTRACTORS NAME'] == key, 'AMOUNT PAID'] = value

    for key, value in unmatched_subs.items():
        # Create a new row to add
        new_row = {'SUB CONTRACTORS NAME': key, 'AMOUNT PAID': value}

        # Add the new row to the DataFrame
        subs_v1.loc[len(subs_v1)] = new_row

    new_row = {'SUB CONTRACTORS NAME': 'TOTAL', 'AMOUNT PAID': yr_total}
    subs_v1.loc[len(subs_v1)] = new_row
    # print(matched_subs)
    # print(unmatched_subs)
    # # print(yr_total)
    # print(subs_v1.to_string())

    return subs_v1


def subs_df(qif_path):
    textfile = open(qif_path, 'r')
    # textfile = open(r'C:\Users\12158\Desktop\BSA_APP\QIF\REIFAST CONSTRUCTION INC.QIF', 'r')
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
        df = df.append({'Subcontractor': key.upper(), '2022 Total': value}, ignore_index=True)

    df = df.append({'Subcontractor':'******', '2022 Total':'******'}, ignore_index=True)
    df = df.append({'Subcontractor':'TOTAL', '2022 Total':total}, ignore_index=True)
    # print(df)
    return match_subs(df)
    # print(match_subs(df))
    # return df    

