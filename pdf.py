from bs4 import BeautifulSoup as bs
import os
import re
import App
import CompanyReader

contacts_df = CompanyReader.contacts_df
# 
# company = ''

def info(company):
    print(contacts_df.loc[contacts_df['Customer'] == company])

with open('f1099nec fields copy.html', 'r', encoding="utf8") as f:
    html_string = f.read()


# html_string = html_string.replace('id="Copy1CustomerContact">*<','id="Copy1CustomerContact">TEST<')
# print(re.search('id="Copy1CustomerContact">TEST<',html_string))



# with open("test.html", "w", encoding="utf8") as file:
#     file.write(html_string)
