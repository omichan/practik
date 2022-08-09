import json
from datetime import datetime
from operator import itemgetter
import re


# open JSON file
with open("operations.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file)

# sort executed operations by date
data_sorted = sorted([x for x in data if 'from' in x and x["state"]=="EXECUTED"], key=lambda k:k['date'], reverse=True)

def hide_card(operation):
    # hide card number
    # argument: str -- operation text with card number

    # get only card number
    card_number = re.findall(r'(\d+)', operation)[0]

    # transform str to list
    hide_card_list = list(card_number)

    # hide some digits by '*'
    hide_card_list[6:12] = list('*'*6)

    # group by 4 symbols
    hide_card_tab = ["".join(hide_card_list[i:i+4]) for i in range(0, len(hide_card_list), 4)]

    # hide card str
    hide_card = " ".join(hide_card_tab)
    # replace open CN by hided CN
    return operation.replace(card_number, hide_card)

def hide_account(operation):
    # hide account number
    # argument: str -- operation text with acc number

    # get only account number
    account_number = re.findall(r'(\d+)', operation)[0]

    # hide account by '*'
    account_hide = "**" + account_number[-4:]

    # replace open AN by hided AN
    return operation.replace(account_number, account_hide)

# last 5 operations loop
for operation in data_sorted[:5]:
    # str to date format
    full_date = datetime.strptime(operation["date"], "%Y-%m-%dT%H:%M:%S.%f")

    # print operation date
    print(full_date.date().strftime("%Y.%m.%d"), operation["description"])

    # card or account detector for "from"
    if "Счет" in operation["from"]:
        trans_from = hide_account(operation["from"])  
    else:
        trans_from = hide_card(operation["from"])

    # card or account detector for "to"
    if "Счет" in operation["to"]:
        trans_to = hide_account(operation["to"])  
    else:
        trans_to = hide_card(operation["to"])
        
    # print direction of transaction 
    print(trans_from, "->", trans_to)

    #print transaction amount
    print(operation["operationAmount"]["amount"], operation["operationAmount"]["currency"]["name"])

    # operation separator
    print()

print(data[0].values())
print(data[0].keys())
print('EXECUTED' in data[0].values())
print('state' in data[0].keys())

