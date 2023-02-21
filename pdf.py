from bs4 import BeautifulSoup as bs
import os
import re
 

# Give location where text is
# stored which you wish to alter
# old_text = soup.find('div', {"id": "info"})

# base = os.path.dirname(os.path.abspath(__file__))
# html = open(os.path.join(base, 'f1099nec.html'), encoding="utf8")
# soup = bs(html, 'html.parser')

# old_text = soup.find('div', {"id": "test"})
# new_text = old_text.replace_with('test')

with open('f1099nec fields copy.html', 'r', encoding="utf8") as f:
    html_string = f.read()

# print(html_string)
# print(re.search('Copy1CustomerContact',html_string))
# re.sub('id="Copy1CustomerContact"><','id="Copy1CustomerContact">TEST<',html_string)
html_string = html_string.replace('id="Copy1CustomerContact">*<','id="Copy1CustomerContact">TEST<')
print(re.search('id="Copy1CustomerContact">TEST<',html_string))

with open("test.html", "w", encoding="utf8") as file:
    file.write(html_string)
