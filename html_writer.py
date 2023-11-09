import pandas as pd
import os
import re 
import company_reader
import copy_a
import math

def no_nan(str):
    if str == 'nan':
        return ''
    else:
        return str

def populate_html(company, excel):

    subs_df = pd.read_excel(excel) # Dataframe containing Subcontractor Information
    df = company_reader.setup_df() # Dataframe containing Client information

    # Convert our HTML template to a string for ease manipulating the data
    with open('Templates/1096 template.html', 'r', encoding='utf8') as f:
        html_string = f.read()

    # Get the client information 
    name = df.loc[df['Customer'] == company, 'Customer'].item()
    street = df.loc[df['Customer'] == company, 'Street'].item()
    city = df.loc[df['Customer'] == company, 'City'].item()
    state = df.loc[df['Customer'] == company, 'State'].item()
    zip = df.loc[df['Customer'] == company, 'Zip'].item().zfill(5)
    ein = df.loc[df['Customer'] == company, 'E.I.N.'].item()
    contact = df.loc[df['Customer'] == company, 'Primary Contact'].item()
    phone = df.loc[df['Customer'] == company, 'Main Phone'].item()

    subs_total = subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == 'TOTAL', 'AMOUNT PAID'].item() 

    # Set the needed info on 1096 page 1
    html_string = html_string.replace('id="p1Filer">*</div>', 'id="p1Filer">' + name + '</div>') 
    html_string = html_string.replace('id="p1StreetAddr">*</div>', 'id="p1StreetAddr">' + street + '</div>')
    html_string = html_string.replace('id="p1CityStateZip">*<span class="_ _46"></span>*<span class="_ _47"> </span>*</div>',
                                     'id="p1CityStateZip">' + city + '<span class="_ _46"></span>' + state + ' ' + zip + '<span class="_ _47"> </span></div>')
    html_string = html_string.replace('id="p1Contact">*</div>', 'id="p1Contact">' + contact + '</div>')
    html_string = html_string.replace('id="p1Phone">*</div>','id="p1Phone">' + phone + '</div>')
    html_string = html_string.replace('id="p1EINextra">*<span class="_ _48"> </span>*<span class="_ _49"> </span><span class="ff9">0.00<span class="_ _2"> </span></span>*</div>',
                                      'id="p1EINextra">' + ein + '<span class="_ _48"> </span><span class="_ _49"> </span><span class="ff9">' + str(subs_total) + '<span class="_ _2"> </span></span></div>')

    # Assuming the DataFrame is named subs_v1_df
    subs_df['AMOUNT PAID'] = pd.to_numeric(subs_df['AMOUNT PAID'], errors='coerce')
    subs_df = subs_df.dropna(subset=['AMOUNT PAID'])
    # Drop rows where 'SUB CONTRACTORS NAME' is 'TOTAL'
    subs_df = subs_df[subs_df['SUB CONTRACTORS NAME'] != 'TOTAL']

    threes = []           # List to store sets of three column values
    threethrees = []      # Temporary list to accumulate values

    for index, row in subs_df.iterrows():
        threethrees.append(row['SUB CONTRACTORS NAME'])
        if len(threethrees) == 3:
            threes.append(threethrees)
            threethrees = []
    
    remaining = len(threethrees)
    if remaining > 0:
        threes.append(threethrees + [''] * (3 - remaining))

    print(threes)

    with open('Templates/p4.txt', 'r', encoding='utf-8') as file:        
        p4 = file.read()  # Read the contents of the file into a string variable
    
    with open('Templates/p5.txt', 'r', encoding='utf-8') as file:        
        p5 = file.read()  # Read the contents of the file into a string variable

    with open('Templates/p6.txt', 'r', encoding='utf-8') as file:        
        p6 = file.read()  # Read the contents of the file into a string variable

    with open('Templates/p7.txt', 'r', encoding='utf-8') as file:        
        p7 = file.read()  # Read the contents of the file into a string variable

    final_pg4 = ''

    for list in threes:
        pg4 = p4
        for index, sub in enumerate(list):   
                if sub:
                    street_sub = no_nan(str(subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == sub, 'ADDRESS'].item()))
                    city_sub = no_nan(str(subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == sub, 'CITY'].item()))
                    state_sub = no_nan(str(subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == sub, 'STATE '].item()))
                    zip_sub = no_nan(str(subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == sub, 'ZIP'].item()))
                    ein_sub = no_nan(str(subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == sub, 'EIN'].item()))
                    total = no_nan(str(subs_df.loc[subs_df['SUB CONTRACTORS NAME'] == sub, 'AMOUNT PAID'].item()))
                else:
                    street_sub = ''
                    city_sub = ''
                    state_sub = ''
                    zip_sub = ''
                    ein_sub = ''
                    total = ''
                    name = ''
                    street = ''
                    city = ''
                    state = ''
                    zip = ''
                    ein = ''
                    
                if index == 0:
                    pg4 = pg4.replace('id="A1Name">*</div>', 'id="A1Name">' + name + '</div>')
                    pg4 = pg4.replace('id="A1Street">*</div>', 'id="A1Street">' + str(street) + '</div>')                                  
                    pg4 = pg4.replace('id="A1CityStateZip">*<span class="_ _73"> </span><span class="ws1">** </span>*****</div>', 
                                    'id="A1CityStateZip">' + str(city).ljust(24) + '<span class="ws1">' + str(state) + ' </span>' + str(zip) + '</div>')
                    pg4 = pg4.replace('id="A1EIN">*<span class="_ _74"> </span>*</div>', 'id="A1EIN">' + str(ein) + '<span class="_ _74"> </span>' + str(ein_sub) + '</div>')
                    pg4 = pg4.replace('id="A1SubName">*</div>', 'id="A1SubName">' + sub + '</div>')
                    pg4 = pg4.replace('id="A1SubStreet">*</div>', 'id="A1SubStreet">' + str(street_sub) + '</div>')
                    pg4 = pg4.replace('id="A1SubCityStateZip">*<span class="_ _75"> </span><span class="ws2">** </span>*****</div>',
                                    'id="A1SubCityStateZip">' + str(city_sub).ljust(24) + str(state_sub) + ' ' + str(zip_sub).replace('.' ,'') + '<span class="_ _75"> </span><span class="ws2"></span></div>')
                    pg4 = pg4.replace('id="A1Total">*</div>', 'id="A1Total">' + str(total) + '</div>')
                elif index == 1:
                    pg4 = pg4.replace('id="A2Name">*</div>', 'id="A2Name">' + name + '</div>')
                    pg4 = pg4.replace('id="A2Street">*</div>', 'id="A2Street">' + str(street) + '</div>')
                    pg4 = pg4.replace('id="A2CityStateZip">*<span class="_ _73"> </span><span class="ws1">**<span class="ff11"> </span></span>*****</div>', 
                                    'id="A2CityStateZip">' + str(city).ljust(24) + state + ' ' + zip +'<span class="_ _73"> </span><span class="ws1"><span class="ff11"> </span></span></div>')
                    pg4 = pg4.replace('id="A2EIN">*<span class="_ _74"> </span>*</div>', 'id="A2EIN">' + str(ein) + '<span class="_ _74"> </span>' + str(ein_sub) + '</div>')
                    pg4 = pg4.replace('id="A2SubName">*</div>', 'id="A2SubName">' + sub + '</div>')
                    pg4 = pg4.replace('id="A2SubStreet">*</div>', 'id="A2SubStreet">' + str(street_sub) + '</div>')
                    pg4 = pg4.replace('id="A2SubCityStateZip">*<span class="_ _75"> </span><span class="ws2">**<span class="ff11"> </span></span>*****</div>',
                                    'id="A2SubCityStateZip">' + str(city_sub).ljust(24) + str(state_sub) + ' ' + str(zip_sub).replace('.' ,'') + '<span class="_ _75"> </span><span class="ws2"><span class="ff11"> </span></span></div>')
                    pg4 = pg4.replace('id="A2Total">*</div>', 'id="A2Total">' + str(total) + '</div>')                     
                elif index == 2:
                    pg4 = pg4.replace('id="A3Name">*</div>', 'id="A3Name">' + name + '</div>')
                    pg4 = pg4.replace('id="A3Street">*</div>', 'id="A3Street">' + str(street) + '</div>')
                    pg4 = pg4.replace('id="A3CityStateZip">*<span class="_ _73"> </span><span class="ws1">**<span class="ff11"> </span></span>*****</div>', 
                                    'id="A3CityStateZip">' + str(city).ljust(24) + state + ' ' + zip +'<span class="_ _73"> </span><span class="ws1"><span class="ff11"> </span></span></div>')
                    pg4 = pg4.replace('id="A3EIN">*<span class="_ _74"> </span>*</div>', 'id="A3EIN">' + str(ein) + '<span class="_ _74"> </span>' + str(ein_sub) + '</div>')
                    pg4 = pg4.replace('id="A3SubName">*</div>', 'id="A3SubName">' + sub + '</div>')
                    pg4 = pg4.replace('id="A3SubStreet">*</div>', 'id="A3SubStreet">' + str(street_sub) + '</div>')
                    pg4 = pg4.replace('id="A3SubCityStateZip">*<span class="_ _75"> </span><span class="ws2">**<span class="ff11"> </span></span>*****</div>',
                                    'id="A3SubCityStateZip">' + str(city_sub).ljust(24) + str(state_sub) + ' ' + str(zip_sub).replace('.' ,'') + '<span class="_ _75"> </span><span class="ws2"><span class="ff11"> </span></span></div>')
                    pg4 = pg4.replace('id="A3Total">*</div>', 'id="A3Total">' + str(total) + '</div>')
        final_pg4 += pg4
   
    html_string = html_string.replace('<div class="loading-indicator">', final_pg4 + '<div class="loading-indicator">') # Add Copy A for all subcontractors to the 1096

    # Get the client information 
    name = df.loc[df['Customer'] == company, 'Customer'].item()
    street = df.loc[df['Customer'] == company, 'Street'].item()
    city = df.loc[df['Customer'] == company, 'City'].item()
    state = df.loc[df['Customer'] == company, 'State'].item()
    zip = df.loc[df['Customer'] == company, 'Zip'].item().zfill(5)
    ein = df.loc[df['Customer'] == company, 'E.I.N.'].item()
    contact = df.loc[df['Customer'] == company, 'Primary Contact'].item()

    b1c = ''

    # Create Copy B, Copy 1 and Copy C for each subcontracotr and append it the the html string
    for index, row in subs_df.iterrows():  
        pg5 = p5
        pg6 = p6
        pg7 = p7

        sub_name = row['SUB CONTRACTORS NAME']
        street_sub = no_nan(str(row['ADDRESS']))
        city_sub = no_nan(str(row['CITY']))
        state_sub = no_nan(str(row['STATE ']))
        zip_sub = no_nan(str(row['ZIP']))
        ein_sub = no_nan(str(row['EIN']))
        total = no_nan(str(row['AMOUNT PAID']))
        print(sub_name + ': ' + total)

        # Create Copy B
        pg5 = pg5.replace('id="copyBName">*</div>', 'id="copyBName">' + name + '</div>')
        pg5 = pg5.replace('id="copyBTotal">*</div>', 'id="copyBTotal">' + total + '</div>')
        pg5 = pg5.replace('id="copyBStateZip">**<span class="ff11"> </span><span class="ws0">*****</span>',
                          'id="copyBStateZip">' + state + '<span class="ff11"> </span><span class="ws0">' + zip + '</span>')
        # pg5 = pg5.replace('id="copyBOwner">OWNER</div>', 'id="copyBOwner">' + contact + '</div>') # Need to see if we want to add the owner here
        pg5 = pg5.replace('id="copyBOwner">OWNER</div>', 'id="copyBOwner"></div>')
        pg5 = pg5.replace('id="copyBStreet">*</div>', 'id="copyBStreet">' + street + '</div>')
        pg5 = pg5.replace('id="copyBCity">*</div>', 'id="copyBCity">' + city + '</div>')
        # pg5 = pg5.replace('id="copyBTelephone">*</div>', 'id="copyBTelephone">' + ) # need to add customer telephone to contacts
        pg5 = pg5.replace('id="copyBEin">*<span class="_ _74"> </span>*</div>', 'id="copyBEin">' + ein + '<span class="_ _74"> </span>' + ein_sub + '</div>')
        pg5 = pg5.replace('id="copyBSubName">*</div>', 'id="copyBSubName">' + sub_name + '</div>')
        pg5 = pg5.replace('id="copyBSubStreet">*</div>', 'id="copyBSubStreet">' + street_sub + '</div>')
        pg5 = pg5.replace('id="copyBSubCityStateZip">*<span class="_ _75"> </span>*</div>',
                          'id="copyBSubCityStateZip">' + city_sub.ljust(24) + state_sub + ' ' + zip_sub.replace('.' ,'') + '<span class="_ _75"> </span></div>')
        b1c += pg5

        # Create Copy 1
        pg6 = pg6.replace('id="copy1Name">*</div>', 'id="copy1Name">' + name + '</div>')
        pg6 = pg6.replace('id="copy1Total">*</div>', 'id="copy1Total">' + total + '</div>')
        pg6 = pg6.replace('id="copy1Street">*</div>', 'id="copy1Street">' + street + '</div>')
        pg6 = pg6.replace('id="copy1CityStateZip">*<span class="_ _73"> </span><span class="ws1">**<span class="ff11"> </span></span>*****</div>',
                          'id="copy1CityStateZip">' + city_sub.ljust(24) + state_sub + ' ' + zip_sub.replace('.' ,'') + '<span class="_ _73"> </span><span class="ws1"><span class="ff11"> </span></span></div>')
        pg6 = pg6.replace('id="copy1Ein">*<span class="_ _74"> </span>*</div>', 'id="copy1Ein">' + ein + '<span class="_ _74"> </span>' + ein_sub + '</div>')
        pg6 = pg6.replace('id="copy1SubName">*</div>', 'id="copy1SubName">' + sub_name + '</div>') 
        pg6 = pg6.replace('id="copy1SubStreet">*</div>', 'id="copy1SubStreet">' + street_sub + '</div>')
        pg6 = pg6.replace('id="copy1SubcityStatezip">*<span class="_ _75"> </span><span class="ws2">**<span class="ff11"> </span></span>*****</div>',
                          'id="copy1SubcityStatezip">' + city_sub.ljust(24) + state_sub + ' ' + zip_sub.replace('.' ,'') + '<span class="_ _75"> </span><span class="ws2"><span class="ff11"> </span></span></div>')
        b1c += pg6

        # Create Copy C
        pg7 = pg7.replace('id="copyCName">*</div>', 'id="copyCName">' + name + '</div>')
        pg7 = pg7.replace('id="copyCTotal">*</div>', 'id="copyCTotal">' + total + '</div>')
        pg7 = pg7.replace('id="copyCStreet">*</div>', 'id="copyCStreet">' + street + '</div>')
        pg7 = pg7.replace('id="copyCCityStateZip">*<span class="_ _73"> </span><span class="ws1">**<span class="ff11"> </span></span>*****</div>',
                          'id="copyCCityStateZip">' + city.ljust(24) + state + ' ' + zip.replace('.' ,'') + '<span class="_ _73"> </span><span class="ws1"><span class="ff11"> </span></span></div>')
        pg7 = pg7.replace('id="copyCEin">*<span class="_ _74"> </span>*</div>',
                          'id="copyCEin">' + ein + '<span class="_ _74"> </span>' + ein_sub + "</div>")
        pg7 = pg7.replace('id="copyCSubName">*</div>', 'id="copyCSubName">' + sub_name + '</div>')
        pg7 = pg7.replace('id="copyCSubStreet">*</div>', 'id="copyCSubStreet">' + street_sub + '</div>')
        pg7 = pg7.replace('id="copyCSubcityStateZip">*<span class="_ _75"> </span><span class="ws2">** </span>*****</div>',
                          'id="copyCSubcityStateZip">' + city_sub.ljust(24) + state_sub + ' ' + zip_sub.replace('.' ,'') + '<span class="_ _75"> </span><span class="ws2"></span></div>')
        b1c += pg7
    html_string = html_string.replace('<div class="loading-indicator">', b1c + '<div class="loading-indicator">')


    file_name = 'C:\\Users\\12158\\Desktop\\Reports\\' + company + ' 2022\\' + company.replace(" ", "_") + '_1096.html'

    with open(file_name, "w", encoding="utf8") as file:
        file.write(html_string)

    print('HTML successfully populated!')

    os.startfile(file_name) # Open the HTML 1096 report

