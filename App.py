import CompanyReader
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

df = CompanyReader.contacts_df
print('Welcome to Charlie\'s 1096 & 1099 generator!')

def get_company():
    print('Enter a company name: ')
    x = input()
    matches = []
    inputted_company =''
    for index, row in df.iterrows():
        company = row['Customer']
        ratio = fuzz.partial_ratio(x.upper(), row['Customer'].upper())
        result = ''
        if ratio > 95:
            matches.append(company)
    if len(matches) == 0:
        print('Invalid company')
        get_company()   
    if len(matches) > 0:
        for match in matches:
            print('Did you mean ' + match + '?')  
            y = input()
            if y.upper() == 'Y' or y.upper() == 'YES':
                inputted_company += match
                break
    return inputted_company
    
# get_company()

print(df.loc[df['Customer'] == get_company()])