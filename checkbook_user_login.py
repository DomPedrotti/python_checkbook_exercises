from pick import pick
from cb_sql_functions import select_usernames, check_password, add_new_user_table



def log_on():
    '''
    on startup of checkbook app, log_on() asks user their status as a new or existing user

    if user provides correct credentials and successfully signs on, log_on returns username to python_checkbook.py to be used to reference user's unique transaction tables

    if existing user, log_on redirects user to sign in

    if user is new, log_on() redirects them to create account function so they can initialize their account before sending them on to sign in

    finally if user opts not to sign in, function return nothing and program closes
    '''
    existing_user = new_or_existing_user()
    if existing_user == None:
        return
    elif existing_user:
        return enter_user_and_password()
    elif not existing_user:
        create_account()
        return enter_user_and_password()
    


def new_or_existing_user():
    '''
    verifies user is either new or existing, also provides user a chance to exit program
    '''
    prompt = "Are You a New or Exising User? (Use Arrow Keys to Make Selection)"
    choices = ['Current User', 'New User', 'Exit']
    identify, index = pick(choices, prompt, indicator = '->')
    
    if index == 2:
        return None
    elif index == 0:
        return True
    else:
        return False


def enter_user_and_password():
    '''
    allows user to access their unique transaction account

    prompts user to reenter username if it does not exist

    cross checks password with coresponding password in users table

    provides another opportunity for user to quit
    '''
    print("Please Enter Login Information: ")
    all_usernames = select_usernames()
    username = input('Username: ')
    while username not in all_usernames:
        error = 'Invalid Username, Try Again?'
        choices = ['Yes', 'No']
        choice, index = pick(choices, error)
        if index == 1:
            return
        else:
            username = input('Username: ')
    password = input('Password: ')
    while not check_password(username, password):
        error = 'Invalid Password, Try Again?'
        choices = ['Yes', 'No']
        choice, index = pick(choices, error)
        if index == 1:
            return
        else:
            password = input('Password: ')
    return username

def create_account():
    '''
    allows user to input username and password to initialize new user transaction table

    checks new username to be unique and prompts user to enter something different if new username is the same as an existing one

    does not log user in
    '''
    existing_users = select_usernames()
    print(existing_users)

    username = input('New Username: ')
    while username in existing_users:
        username = input("ERROR: user profile already exists please enter new username\n to quit, please enter 'quit'\nNew Username: ")
        if username.lower().strip() == 'quit':
            return
    password = input('Password: ')
    add_new_user_table(username, password)
    print("\n Congratulations, you're all set!\n")



