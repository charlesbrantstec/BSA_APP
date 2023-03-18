import CompanyReader
import SubsReport
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import HtmlWriter

df = CompanyReader.setup_df()

print('Welcome to Charlie\'s 1096 & 1099 generator!')
company = ''

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
    # return inputted_company
    print('Drag and drop the subcontractor report for your company here:')
    z = input()
    sub_totals = SubsReport.sub_totals(z)
    # print(sub_totals)
    SubsReport.merge_duplicates(sub_totals)
    SubsReport.populate_subs(sub_totals)
    # print(SubsReport.merge_duplicates(sub_totals))
    
# get_company()
HtmlWriter.populate_html(get_company(),df)



# print(df.loc[df['Customer'] == get_company(), 'Customer'].item())
