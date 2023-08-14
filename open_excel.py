import pandas as pd
import pyautogui
from openpyxl import load_workbook
import os

def create_excel(cmp_name, df):
    excel_file = os.path.join('C:\\Users\\12158\\Desktop\\Reports\\' + cmp_name + ' 2022\\', cmp_name + ' 2022 SUBS REPORT.xlsx')
    # excel_file = cmp_name + ' 2022 SUBS REPORT.xlsx' # Name the file with the passed in company name
    df.to_excel(excel_file, index=False)

    # os.startfile(excel_file) # Open the saved excel file

    return excel_file


