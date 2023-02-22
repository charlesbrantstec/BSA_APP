import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pathlib import Path
import re


# df = pd.read_excel(r'C:\Users\12158\Desktop\BSA_APP\ReifastSubs.xlsx')
# subs_df = pd.read_excel(r'C:\Users\12158\Desktop\BSA_APP\SUBS 2022.xlsx')
# # df = pd.read_excel(r'/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/ReifastSubs.xlsx')
# # subs_df = pd.read_excel(r'/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/SUBS 2022.xlsx')
# subs_df = subs_df.drop(subs_df.index[0])

# def subs_totals():
#     arr = df['Unnamed: 4'].unique() # get all unique subs from df
#     cleaned_arr = [item for item in arr if isinstance(item, str) and item != 'Description'] # clean the subs array
#     sub_totals = {}
#     for subcontractor in cleaned_arr:
#         sum = df.loc[df['Unnamed: 4'] == subcontractor, 'Unnamed: 8'].sum() # get sum by subcontractor
#         formatted_sum = '{:,.2f}'.format(abs(sum)) # format sum
#         sub_totals.update({subcontractor:formatted_sum})
#     return sub_totals
            
# print(subs_totals())
# {'All Best Contractors': '321,331.00', 'CG Contractor': '6,500.00',
#  'Da Silva And Associate LLC': '10,000.00', 'GEE Cotractor LLC': '665.00',
#  'Green Master Contractor Corp': '563,155.84', 'GS General Construction': '7,824.00',
#  'Main Line Contractor Corp': '47,468.64', 'Maximum Contrators': '37,985.00', 'MFB Construction LLC': '72,720.00',
#  'New Team Contractor': '182,843.57', 'Vip Construction Llc': '4,244.68'}
# report = input()
def has_letters(inputString):
    return bool(re.search('[a-zA-Z]', inputString))

def sub_totals(report):
# def sub_totals():

    # df = pd.read_excel(r'C:\Users\12158\Desktop\BSA_APP\REIFAST SUBS.xlsx')

    sub_totals = {}
    df = pd.read_excel(report[3:][:-1])
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

    return sub_totals

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
