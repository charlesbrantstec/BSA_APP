import pandas as pd
import warnings
import re
import math

warnings.simplefilter(action='ignore', category=FutureWarning)


# contacts = pd.read_csv('C:\\Users\\12158\\Desktop\\BSA_APP\\CUSTOMER CONTACTS.csv')
# print(contacts)

# contacts_df = pd.DataFrame(columns=['Customer','Main Phone','Street','City','State','Zip','E.I.N.'])

contacts_dict = {}

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def is_nan_empty_or_null(value):
    if value is None:
        return True
    elif isinstance(value, str) and not value:
        return True
    elif math.isnan(value):
        return True
    else:
        return False

def setup_df():
    contacts = pd.read_csv('C:\\Users\\12158\\Desktop\\BSA_APP\\CUSTOMER CONTACTS.csv')
    # contacts = pd.read_csv('/Users/charlesbrant-stec/Desktop/BSA_APP/BSA_APP/CUSTOMER CONTACS.csv')

    contacts_df = pd.DataFrame(columns=['Customer','Main Phone','Street','City','State','Zip','Primary Contact','E.I.N.'])

    for index,row in contacts.iterrows():
        company = row['Customer']
        phone = row['Main Phone']
        city = row['City']
        state = row['State']
        zip = row['Zip']
        ein = row['E.I.N.']
        # primary_contact = row['Primary Contact']

        new_row = {}
        if company[0] == '*':
            street = ''
            primary_contact = ''
            # if is_nan_empty_or_null(row['Street2']) and not is_nan_empty_or_null(row['Street1']):
            #     street += row['Street1']
            #     primary_contact += ''
            # elif not is_nan_empty_or_null(row['Street1']) and not is_nan_empty_or_null(row['Street2']):
            #     street += row['Street2']
            #     primary_contact += row['Street1']
            if has_numbers(row['Street1']):
                street += row['Street1']
                primary_contact += ''
            else:
                street += row['Street2']
                primary_contact += row['Street1']
            new_row = {'Customer' : company[1:], 'Main Phone' : phone, 'Street' : street , 'City' : city , 'State' : state, 'Zip' : zip ,'Primary Contact' : primary_contact, 'E.I.N.' : ein}
            contacts_df = contacts_df.append(new_row, ignore_index=True)
    # contacts_df.to_csv('contacts.csv',index=False)
    return contacts_df

setup_df().to_csv('CONTACTS.CSV',index=False)
# df = setup_df()
# print(df.to_string())
# print(setup_df().loc[setup_df()['Customer'] == '5TAR PAINTING LLC'])
# contacts_df = contacts_df.append({'Customer' : '123'}, ignore_index=True)
# print(contacts_df)

# print(has_numbers('123abc'))
