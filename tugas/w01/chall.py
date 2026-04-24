#!/usr/bin/env python3

inventory = []

while True:
    if inventory:
        print('You currently have:')
        for item in inventory:
            print(f'- {item}')
    else:
        print('Your inventory is empty!')
    
    print('Add items to your inventory using Python list syntax, like [\'sword\', \'potion\']')
    try:
        new_items = eval(input(">> "))
        if type(new_items) == list:
            inventory.extend(new_items)
        else:
            print('That wasn\'t a list!')
    except:
        print('Let\'s not try anything weird here...')
    print()