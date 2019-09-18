from checkbook_functions import timestamp_from_date, pick_one


def update_sql_table(time, amount, category, description, username):
    '''
    receives time (as a timestamp), transaction amount, transaction category and description, and the user's username
    uses username to reference user's unique transaction table from sql checkbook.db
    inserts new information row into user's tranaction column
    '''
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    
    c = conn.cursor()

    transaction = (time, amount, category, description,)
    execute_line = "INSERT INTO " + username + " VALUES (?,?,?,?)"
    c.execute(execute_line, transaction)

    conn.commit()

    conn.close()

def add_new_user_table(user, password):
    '''
    receives new user name and initializes blank transaction table for new user and appends username table to contain new username
    this one is out of date from the used one, lacks commit statement and user password argument
    '''
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()
    
    c.execute("CREATE TABLE " + user + " (date text, amount real, Category text, description text)")
    user_info = [user, password]
    execute_cmd = f"INSERT INTO users VALUES ('{user}', '{password}')"
    c.execute(execute_cmd)

    conn.commit()

    conn.close()

def select_usernames():
    '''
    uses sql SELECT statement to build a list of all usernames
    returns list of existing users
    '''
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()
    users = []
    for user in c.execute('SELECT username FROM users'):
        users.append(user[0])
    return users

def check_password(username, password):
    '''
    takes in input of username and password attempt
    returns false if provided password does not match username in users table
    '''
    #select password
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()
    for value in c.execute('SELECT password FROM users WHERE username = ?', [username]):
        pswd = value[0]
    t_f = (password == pswd)
    return t_f

def search_by_date(user):
    '''
    Refines transaction table select to dates within 12:00:00am on startdate and 11:59:59pm on end date
    '''
    start_date = input("Enter Start Date (MM/DD/YYYY) ")
    end_date = input("Enter End Date (MM/DD/YYYY) ")
    date_range = (timestamp_from_date(start_date), timestamp_from_date(end_date) + 86400)
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()

    table = []
    for row in c.execute("SELECT * FROM "+ user +" WHERE date BETWEEN ? and ?", date_range):
        table.append(row)
    conn.close()
    return table

def search_by_category(user):
    '''
    filters select statement to return either all withdrawals or all deposits
    '''
    choose_category = input("Type 'D' to see Deposits and 'W' to see Withdrawals")
    while True:
        if choose_category.lower() in ['w', 0]:
            category = 'Withdrawal'
            break
        elif choose_category.lower() in ['d', 1]:
            category = 'Deposit'
            break
        else:
            category, choose_category = pick_one(['Deposit', 'Withdrawal'])
            break
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()

    table = []
    for row in c.execute("SELECT * FROM " + user + " WHERE Category = ?",  [category]):
        table.append(row)
    conn.close()
    return table

def search_by_keyword(user):
    '''
    refines select statement by keyword found in description
    '''
    keyword = input('Enter Keyword ')
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()

    table = []
    for row in c.execute("SELECT * FROM dom WHERE description LIKE '%" +keyword+"%'"):
        table.append(row)
    conn.close()
    return table

    keyword = input('Enter Keyword ')
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()

    table = []
    for row in c.execute("SELECT * FROM "+ user +" WHERE description LIKE '%" +keyword+"%'"):
        table.append(row)
    conn.close()
    return table

def select_all(user):
    import sqlite3
    conn = sqlite3.connect('checkbook.db')
    c = conn.cursor()

    table = []
    for row in c.execute("SELECT * FROM " + user):
        table.append(row)
    conn.close()
    return table