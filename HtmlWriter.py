from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import re 
import CompanyReader

def populate_html(company, df):
    with open('test.html', 'r', encoding="utf8") as f:
        html_string = f.read()

    name = df.loc[df['Customer'] == company, 'Customer'].item()
    street = df.loc[df['Customer'] == company, 'Street'].item()
    city = df.loc[df['Customer'] == company, 'City'].item()
    state = df.loc[df['Customer'] == company, 'State'].item()
    zip = df.loc[df['Customer'] == company, 'Zip'].item()
    ein = df.loc[df['Customer'] == company, 'E.I.N.'].item()

    # Copy1
    html_string = html_string.replace('id="Copy1CustomerContact">TEST<','id="Copy1CustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<')
    html_string = html_string.replace('id="Copy1CustomerEIN">*<','id="Copy1CustomerEIN">'+ein+'<')

    html_string = html_string.replace('id="CopyBCustomerContact">*<','id="CopyBCustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<')
    html_string = html_string.replace('id="CopyBCustomerEIN">*<','id="CopyBCustomerEIN">'+ein+'<')

    html_string = html_string.replace('id="Copy2CustomerContact">*<','id="Copy2CustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<') 
    html_string = html_string.replace('id="Copy2CustomerEIN">*<','id="Copy2CustomerEIN">'+ein+'<')

    html_string = html_string.replace('id="CopyCCustomerContact">*<','id="CopyCCustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<') 
    html_string = html_string.replace('id="CopyCCustomerEIN">*<','id="CopyCCustomerEIN">'+ein+'<')

    
    # html_string = html_string.replace('id="Copy1CustomerEIN">*<')
    # id="Copy1CustomerEIN"
    # id="Copy1SubEIN"
    # id="Copy1SubName"
    # id="Copy1SubStreetAddr"
    # id="Copy1SubCityStZip"
    # id="Copy1SubComp"
    # 

    # print(re.search('id="Copy1CustomerContact">TEST<',html_string))

    with open("populated.html", "w", encoding="utf8") as file:
        file.write(html_string)

    print('HTML successfully populated!')

df = CompanyReader.setup_df()

# populate_html('WG CONSTRUCTION INC', df)