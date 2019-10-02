from checkbook_user_login import log_on
from cb_sql_functions import update_sql_table, select_all, search_by_date, search_by_category, search_by_keyword
from checkbook_functions import check_balance, add_description, print_table, check_value, pick_one
from time import time
from pick import pick 
print("\n\n ~~~~ Welcome to your Terminal Checkbook! ~~~~\n")
#prompt username and open associated table

username = log_on()
#username = 'dude'

#Print welcome message and show options for input selection
while True:
    #if log_on returne no username, quit program
    if username == None:
        print ("Goodbye!")
        break 

    #prompt user to choose action, 1 returns total of transaction columns, 2 and 3 make transactions, 4 filters the data and 5 quits program
    options = ('1) Check Balance', '2) Make a Deposit', '3) Make a Withdrawal', '4) Search History', '5) Exit')
    print(f"\nWhat would you like to do? \n\n{options[0]} \n{options[1]} \n{options[2]} \n{options[3]} \n{options[4]}")
    action = input("\nYour Choice? ")
    #if user choses incorect input, make them select option manually
    if action not in ['1', '2', '3', '4', '5']:
        choice, action = pick_one(options)

    #displays current balance and doesn't move on till user presses the enter button
    if action == '1':
        print(f"\nYour balance is ${check_balance(username)}")
        input("press <ENTER> to continue")

    #makes transaction using sql insert into uers's transaction table
    elif action == '2' or action == '3':
        if action == '2':    
            amount = input("\nHow Much Would You Like to Deposit? ")
            amount = check_value(amount)
            category = "Deposit"
        else:
            #follows same process as making a deposit but with a negative amount
            amount = input("\nHow Much Would You Like to Withdrawal? ")
            amount = check_value(amount)
            amount = float(amount) * -1
            category = 'Withdrawal'
        description = add_description()
        timestamp = time()
        update_sql_table(timestamp, float(amount), category, description, username)

    #Provides user option to see all historical transactions or choose to filter results
    elif action == '4':
        view_history = input('Would you like to...\n\n1) See All Transactions\n2) Filter Search\n')
        
        if view_history not in ('1', '2'):
            choice, view_history = pick_one(['1) See All Transactions', '2) Filter Search'])

        if view_history.strip() == '1':
            table = select_all(username)
            print_table(table)
        else: 
            #provides user option to filter by: date, category, or keyword
            search_by = input("Would You Like to... \n1) Search by Date \n2) Search by Category \n3) Search by Key Word?\n")
            
            if search_by not in ['1', '2', '3']:
                choice, search_by = pick_one(['1) Search by Date' ,'2) Search by Category', '3) Search by Key Word?'])
            
            if search_by == '1':
                table = search_by_date(username)
                print_table(table)
            elif search_by == '2':
                table = search_by_category(username)
                print_table(table)
            elif search_by == '3':
                table = search_by_keyword(username)
                print_table(table)
    # close application
    elif action == '5':
        print("\nThanks and have a great day!\n")
        break
    

