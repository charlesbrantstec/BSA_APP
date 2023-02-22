import pandas as pd
import warnings
import re

warnings.simplefilter(action='ignore', category=FutureWarning)


# contacts = pd.read_csv('C:\\Users\\12158\\Desktop\\BSA_APP\\CUSTOMER CONTACTS.csv')
# print(contacts)

# contacts_df = pd.DataFrame(columns=['Customer','Main Phone','Street','City','State','Zip','E.I.N.'])

contacts_dict = {}

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def setup_df():
    contacts = pd.read_csv('C:\\Users\\12158\\Desktop\\BSA_APP\\CUSTOMER CONTACTS.csv')
    contacts_df = pd.DataFrame(columns=['Customer','Main Phone','Street','City','State','Zip','E.I.N.'])

    for index,row in contacts.iterrows():
        company = row['Customer']
        phone = row['Main Phone']
        city = row['City']
        state = row['State']
        zip = row['Zip']
        ein = row['E.I.N.']

        new_row = {}
        if company[0] == '*':
            street = ''
            if has_numbers(row['Street1']):
                street += row['Street1']
            else:
                street += row['Street2']
            new_row = {'Customer' : company[1:], 'Main Phone' : phone, 'Street' : street , 'City' : city , 'State' : state, 'Zip' : zip ,'E.I.N.' : ein}
            contacts_df = contacts_df.append(new_row, ignore_index=True)
    return contacts_df

# print(setup_df())
# print(setup_df().loc[setup_df()['Customer'] == '5TAR PAINTING LLC'])
# contacts_df = contacts_df.append({'Customer' : '123'}, ignore_index=True)
# print(contacts_df)

# print(has_numbers('123abc'))