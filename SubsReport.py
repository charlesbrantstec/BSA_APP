import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re


# df = pd.read_excel(r'C:\Users\12158\Desktop\BSA_APP\ReifastSubs.xlsx')
# subs_df = pd.read_excel(r'C:\Users\12158\Desktop\BSA_APP\SUBS 2022.xlsx')
# # df = pd.read_excel(r'/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/ReifastSubs.xlsx')
# # subs_df = pd.read_excel(r'/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/SUBS 2022.xlsx')
# subs_df = subs_df.drop(subs_df.index[0])

def has_letters(inputString):
    return bool(re.search('[a-zA-Z]', inputString))

def sub_totals(report):

    sub_totals = {}
    # pc
    # df = pd.read_excel(report[3:][:-1])
    # mac
    df = pd.read_excel(report.replace('\'',''))

    for index, row in df.iterrows():
        name = str(row['Unnamed: 1'])
        amount = row['Unnamed: 10']
        if has_letters(name) and name != 'Date' and  name != 'nan':
            amount = '{:,.2f}'.format(float(amount))[1:]
            sub_totals.update({name.upper() : amount})

    return sub_totals

def merge_duplicates(sub_totals):

    new_dict = {}

    for key, value in sub_totals.items():

        for sub, tot in sub_totals.items():

            if key != sub:

                fuzz_ratio = fuzz.partial_ratio(key.upper(), sub.upper())

                if fuzz_ratio > 95:

                    new_dict.update({key.upper() : sub.upper()})
                    # print(key.upper() +', '+sub.upper() +':' + str(fuzz_ratio))
    
    copy = new_dict.copy()
    val = ''
    for key, value in new_dict.items():
        
        if key != val:
            print('Are '+ key + ' and ' + value + ' the same company?')
            y = input()

            val += value
            
            if y.upper() == 'Y' or y.upper() == 'YES':

                print('Enter the correct name for this company: ')
                z = input().upper()

                total = '{:,.2f}'.format(float(sub_totals[key].replace(',','')) + float(sub_totals[value].replace(',','')))
                del sub_totals[key]
                del sub_totals[value]

                del copy[key]
                del copy[value]

                sub_totals.update({z : total})
    # print(sub_totals)
    return sub_totals

# def populate_subs(sub_totals):

#     df = pd.read_excel('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/SUBS 2022.xlsx')

#     fuzz_df = pd.DataFrame(columns=['Input','Master','PartialRatio','Ratio'])

#     sub_list = df['SUB CONTRACTORS NAME'].tolist()

#     matches_dict = {}

#     for key, value in sub_totals.items():

#         match = process.extractOne(key, sub_list)

#         if match[1] >= 80:

#             matches_dict[key] = (match[0], match[1])

#         else:

#             matches_dict[key] = ('NEW', 0)

#     for key, value in matches_dict.items():
#         print(key + ": " + str(value))
#     return matches_dict

def populate_subs(sub_totals):

    # df = pd.read_excel('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/SUBS 2022.xlsx')
    # updated master subs 
    df = pd.read_excel('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/SUBS 2022 V1.xlsx')
    df = df.drop(0, axis=0)

    fuzz_df = pd.DataFrame(columns=['Input','Master','PartialRatio','Ratio'])

    for key, value in sub_totals.items():

        for index, row in df.iterrows():

                master_sub = row['SUB CONTRACTORS NAME']

                token_ratio = fuzz.token_set_ratio(key.upper(), master_sub.upper())

                fuzz_ratio = fuzz.partial_ratio(key.upper(), master_sub.upper())

                ratio = fuzz.ratio(key.upper(), master_sub.upper())

                new_row = {'Input' : key, 'Master' : master_sub, 'PartialRatio' : fuzz_ratio, 'Ratio' : ratio}

                fuzz_df = fuzz_df.append(new_row, ignore_index=True)

                if ratio >= 80 and fuzz_ratio >= 85:

                    # partial_ratio = fuzz.ratio(key.upper(), master_sub.upper())

                    # fuzz_ratio = fuzz.token_set_ratio(key.upper(), master_sub.upper())

                    print(key + ', ' + master_sub + ' : ' + 'ratio: ' +  str(ratio) + ', fuzz: ' + str(fuzz_ratio), ', token: ' + str(token_ratio))

                    # if fuzz_ratio > 80:

                    #     fuzz_ratio = fuzz.token_set_ratio(key.upper(), master_sub.upper())


                    #     print(key + ', ' + master_sub + ' : ' + str(fuzz_ratio))
        # print(fuzz_df.to_string())


#  Rule 1: Fill master row  on 1 match w/ partial  >90 and ratio >80

# PARTIAL
# ALL BEST CONTRACTORS, ALL BEST CONTRACTOR CORP : 95
# CG CONTRACTOR, BCG CONTRACTOR CORP : 100
# CG CONTRACTOR, PERFECT CONTRACTOR CORP : 92
# CG CONTRACTOR, CG CONTRACTOR LLC : 100
# GEE COTRACTOR LLC, CG CONTRACTOR LLC : 91
# GREEN MASTER CONTRACTOR CORP, GREEN MASTER CONTRACTOR CORP : 100
# GS GENERAL CONSTRUCTION, DIMENSION GENERAL CONSTRUCTION LLC : 91
# MAIN LINE CONTRACTOR CORP, MAIN LINE CONTRACTOR CORP : 100

# RATIO
# ALL BEST CONTRACTORS, ALL BEST CONTRACTOR CORP : 86
# CG CONTRACTOR, BCG CONTRACTOR CORP : 81
# CG CONTRACTOR, PERFECT CONTRACTOR CORP : 67
# CG CONTRACTOR, CG CONTRACTOR LLC : 87
# GEE COTRACTOR LLC, CG CONTRACTOR LLC : 88
# GREEN MASTER CONTRACTOR CORP, GREEN MASTER CONTRACTOR CORP : 100
# GS GENERAL CONSTRUCTION, DIMENSION GENERAL CONSTRUCTION LLC : 77
# MAIN LINE CONTRACTOR CORP, MAIN LINE CONTRACTOR CORP : 100


# df = pd.read_excel('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/SUBS 2022.xlsx')
# print(df)

# populate_subs()

# print(merge_duplicates(sub_totals()))

# print('MFB CONSTRUCTION' != 'MFB CONSTRUCTION LLC')
# print(sub_totals()['MFB CONSTRUCTION LLC'])

# print(sub_totals())
# print(has_letters(1/4/2022))

# company_subs(report)

# path = Path('C:\Users\12158\Desktop\BSA_APP\SUBS 2022.xlsx')
# path = path.replace('\\','\\\\')
# df = pd.read_excel(path)
# print(df)

# def merge_duplicate_subcontractors():
#     sub_totals = subs_totals()
#     new_dict = {}
#     for subcontractor, total in sub_totals.items():
#         for sub, tot in sub_totals.items():
#             if subcontractor != sub:
#                 fuzz_ratio = fuzz.partial_ratio(subcontractor.upper(),sub.upper())
#                 if fuzz_ratio > 97 :
#                     if len(subcontractor) > len(sub):
#                         sub_totals[subcontractor] = float(sub_totals[subcontractor].replace(',','')) + float(sub_totals[sub].replace(',',''))
#                         sub_totals[subcontractor] = '{:,.2f}'.format(sub_totals[subcontractor])
#                         new_dict = sub_totals.copy()
#                         del new_dict[sub]
#                     elif len(sub) < len(subcontractor):
#                         sub_totals[sub] = float(sub_totals[subcontractor].replace(',','')) + float(sub_totals[sub].replace(',',''))
#                         sub_totals[sub] = '{:,.2f}'.format(sub_totals[sub])
#                         new_dict = sub_totals.copy()                      
#                         del new_dict[subcontractor]
#     return new_dict

# # print(merge_duplicate_subcontractors())

# # print(subs_df)

# def populate_subs():

#     subs_dict = merge_duplicate_subcontractors()

#     for key, value in subs_dict.items(): # iterate over subcontractors in subs dict

#         match = 0

#         match_index = 0
   
#         for index, row in subs_df.iterrows(): # match that subcontractor against each subcontractor in subs_df
          
#             sub_name = row['SUB CONTRACTORS NAME']
        
#             fuzz_ratio = fuzz.partial_ratio(key.upper(),sub_name.upper()) # compare input subcontractor to subcontract in subs_df

#             print(key + ', ' + sub_name + ' : ' + str(fuzz_ratio))
     
#             if fuzz_ratio > 93 and fuzz_ratio >= match:  

#                 match = fuzz_ratio

#                 match_index = index

#         if match > 0:

#             subs_df.at[match_index, 'AMOUNT PAID'] = value

#         else:

#             new_row = [key.upper(), None, None, None, None, None, value]

#             subs_df.loc[len(subs_df) + 1] = new_row

#     return subs_df

# print(populate_subs())
