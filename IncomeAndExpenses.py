from quiffen import Qif
import decimal
from decimal import Decimal
import pandas as pd
import re
import sys


textfile = open(sys.argv[1], 'r')
name = sys.argv[1].split('\\')[-1].split('.QIF')[0]
# textfile = open('REIFAST CONSTRUCTION.QIF', 'r')
# name = 'ae carpenters'
filetext = textfile.read()
textfile.close()

##################################################
# GET ACCOUNT NAMES                              #
##################################################

start = "!Option:AutoSwitch\n!Account"
end = "!Clear:AutoSwitch"

#1 splits on start, selects second substring
#2 splits on end, selects first substring
rawaccs = (filetext.split(start))[1].split(end)[0]

rawaccs1 = rawaccs.split('^')
accounts = []
for acc in rawaccs1:
    acct = (acc.split('\n')[1].split('\n')[0])
    accounts.append(acct)
accounts.pop()   

#create dataframe for each account

# print(accounts)

##################################################
# GET TRANSACTIONS FOR ACCT YEAR                 #
##################################################

# start = '!Option:AutoSwitch\n!Account\nNBoA Chk 3340\nTBank\n^\nNChecking 2815\nTBank\n^\nNChecking 9122\nTBank\n^\n!Clear:AutoSwitch\n!Option:AutoSwitch\n'
# start = '!Option:AutoSwitch'
# print((filetext.split(start)[1]).split('^')[0])

#v get all expenses & income for 2022
# start = '!Option:AutoSwitch\n!Account\nNBoA Chk 3340\nTBank\n^\nNChecking 2815\nTBank\n^\nNChecking 9122\nTBank\n^\n!Clear:AutoSwitch\n!Option:AutoSwitch\n'
start = '!Clear:AutoSwitch\n!Option:AutoSwitch'
raw = (filetext.split(start)[1]).split('^')
expenses = Decimal('0')
incomes = Decimal('0')

for item in raw:
    item1 = item.split('\n')
    # if raw[1] contains '22 then we count the expense/income
    if bool(re.search('\'22', item1[1])):
        # 'U-' indicates an expense
        if bool(re.search('U-', item1[2])):
            expense = Decimal((item1[2].split('U-')[1]).replace(',',''))
            expenses += expense
        # check if - in 'U-' is a number
        if bool(re.search(r'[0-9]', item1[2][:2])):
            income = Decimal((item1[2].split('U')[1]).replace(',',''))
            incomes += income
# print(expenses)
# print(incomes)

#find all expense and income categories
expenseCategories = []
incomeCategories = []
# last item in raw list is '\n' which is causing an erro at end of loop
raw.pop()
for item in raw[3:]:
    item1 = item.split('\n')
    # is this an expense?
    if bool(re.search('\'22', item1[1])):
        if bool(re.search('U-', item1[2])) and '!Account' not in item1[1]:
            for str in item1:
                if str.startswith('L'):
                    expenseCategories.append(str[1:])
    if bool(re.search(r'[0-9]', item1[2][:2])):
            for str in item1:
                if str.startswith('L'):
                    incomeCategories.append(str[1:])
            
# convert list to set to remove duplicates then back to list
expenseCategoryList = []
incomeCategoryList = []
for category in expenseCategories:
    expenseCategoryList.append(category.split(':')[0])

for category in incomeCategories:
    incomeCategoryList.append(category.split(':')[0])   

expenseCategories = list(set(expenseCategoryList))
incomeCategories = list(set(incomeCategoryList))
# print(expenseCategories)
# print(incomeCategories)

expensesDict = {}
for cat in expenseCategories:
    expensesDict.update({cat: Decimal('0')})

incomeDict = {}
for cat in incomeCategories:
    incomeDict.update({cat: Decimal('0')})

print(expensesDict)

# total all expenses and income per category
for item in raw[3:]:
    item1 = item.split('\n')
    # is this an expense?
    if bool(re.search('\'22', item1[1])):
        if bool(re.search('U-', item1[2])) and '!Account' not in item1[1]:
            for str in item1:
                if str.startswith('L'):
                    category = str[1:].split(':')[0]
                    expense = Decimal((item1[2].split('U-')[1]).replace(',',''))
                    expensesDict[category] += expense
        if bool(re.search(r'[0-9]', item1[2][:2])) and '!Account' not in item1[1]:
            for str in item1:
                if str.startswith('L'):
                    category = str[1:].split(':')[0]
                    income = Decimal((item1[2].split('U')[1]).replace(',',''))
                    incomeDict[category] += income

# convert Decimal(value) to string value
for key,value in expensesDict.items():
    expensesDict[key] = "{:.2f}".format(value)

for key,value in incomeDict.items():
    incomeDict[key] = "{:.2f}".format(value)


df = pd.DataFrame(columns=['Category','2022 Total'])
df = df.append({'Category' : 'INCOME', '2022 Total' : '******'}, ignore_index=True)
for key,value in incomeDict.items():
    df = df.append({'Category': key, '2022 Total' : value}, ignore_index=True)

df = df.append({'Category' : 'TOTAL INCOME', '2022 Total' : incomes}, ignore_index=True)

df = df.append({'Category' : 'EXPENSES', '2022 Total' : '******'}, ignore_index=True)
for key,value in expensesDict.items():
    df = df.append({'Category': key, '2022 Total' : value}, ignore_index=True)

df = df.append({'Category' : 'TOTAL EXPENSES', '2022 Total' : expenses}, ignore_index=True)
df = df.append({'Category' : 'OVERALL TOTAL', '2022 Total' : incomes - expenses}, ignore_index=True)

df.to_csv('C:/Users/12158/Desktop/BSA_APP/'+name+' - Income&Expense by Category.csv', index=False)

##################################################
# GET EXPENSES BY SUB CONTRACTOR                 #
##################################################










