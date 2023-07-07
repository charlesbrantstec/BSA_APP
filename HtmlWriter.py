from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import re 
import CompanyReader

def populate_html(company):
    df = CompanyReader.setup_df()
#    with open('test.html', 'r', encoding="utf8") as f:
#        html_string = f.read()
    with open('1096 template.html', 'r', encoding='utf8') as f:
        html_string = f.read()

    name = df.loc[df['Customer'] == company, 'Customer'].item()
    street = df.loc[df['Customer'] == company, 'Street'].item()
    city = df.loc[df['Customer'] == company, 'City'].item()
    state = df.loc[df['Customer'] == company, 'State'].item()
    zip = df.loc[df['Customer'] == company, 'Zip'].item()
    ein = df.loc[df['Customer'] == company, 'E.I.N.'].item()
    contact = df.loc[df['Customer'] == company, 'Primary Contact'].item()

    # Set the needed info on 1096 page 1
    html_string = html_string.replace('id="p1Filer">*</div>', 'id="p1Filer">' + name + '</div>') 
    html_string = html_string.replace('id="p1StreetAddr">*</div>', 'id="p1StreetAddr">' + street + '</div>')
    html_string = html_string.replace('id="p1CityStateZip">*<span class="_ _46"></span>*<span class="_ _47"> </span>*</div>', 'id="p1CityStateZip">' + city + '<span class="_ _46"></span>' + state + '<span class="_ _47"> </span>' + zip + '</div>')

    # Copy1
    # html_string = html_string.replace('id="Copy1CustomerContact">TEST<','id="Copy1CustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<')
    # html_string = html_string.replace('id="Copy1CustomerEIN">*<','id="Copy1CustomerEIN">'+ein+'<')

    # html_string = html_string.replace('id="CopyBCustomerContact">*<','id="CopyBCustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<')
    # html_string = html_string.replace('id="CopyBCustomerEIN">*<','id="CopyBCustomerEIN">'+ein+'<')

    # html_string = html_string.replace('id="Copy2CustomerContact">*<','id="Copy2CustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<') 
    # html_string = html_string.replace('id="Copy2CustomerEIN">*<','id="Copy2CustomerEIN">'+ein+'<')

    # html_string = html_string.replace('id="CopyCCustomerContact">*<','id="CopyCCustomerContact">'+name+'<br>'+street.upper()+'<br>'+city.upper()+', '+state+' '+zip+'<') 
    # html_string = html_string.replace('id="CopyCCustomerEIN">*<','id="CopyCCustomerEIN">'+ein+'<')

    
    # html_string = html_string.replace('id="Copy1CustomerEIN">*<')
    # id="Copy1CustomerEIN"
    # id="Copy1SubEIN"
    # id="Copy1SubName"
    # id="Copy1SubStreetAddr"
    # id="Copy1SubCityStZip"
    # id="Copy1SubComp"
    # 

    # print(re.search('id="Copy1CustomerContact">TEST<',html_string))

    file_name = company.replace(" ", "_") + '_1096.html'
    with open(file_name, "w", encoding="utf8") as file:
        file.write(html_string)

    print('HTML successfully populated!')

# df = CompanyReader.setup_df()

# print(df)

# populate_html('AE CARPENTERS INC', df)