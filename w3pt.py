"""
    Christina Trotter
    ENGR 692
    12/8/18
    Python 3.7.1

    This is the main file
    Run from terminal by using the command python3 w3pt.py
"""

from explr_mod import *
global prompts

def latest_blocks():
    global prompts
    print('\n---- LATEST BLOCKS ----')
    while True:
        try:
            depth = int(input(prompts['blocks']))
            break
        except:                
            print(prompts['invalid'])
    get_latest_blocks(depth)

def latest_transactions():
    global prompts
    print('\n---- LATEST TRANSACTIONS ----')
    while True:
        try:
            depth = int(input(prompts['transactions']))
            break
        except:                
            print(prompts['invalid'])
    get_latest_transactions(depth)

def miner_query():
    global prompts
    print('\n---- MINER QUERY ----')
    miner = input(prompts['miner'])
    start = get_start()
    depth = get_depth()
    get_miner_query(miner,depth,start)

def get_depth():
    global prompts
    while True:
        try:
            depth = int(input(prompts['depth']))
            return depth
        except:                
            print(prompts['invalid'])

def get_start():
    global prompts
        
    LAST, OTHR = '1','2'
    
    choice = input(prompts['start'])
    
    while choice not in [LAST,OTHR]:
        choice = input(prompts['invalid'])
    
    if choice == OTHR:
        while True:
            try:
                start = int(input(prompts['block']))
                return start
            except:                
                print(prompts['invalid'])

    return False
           
        
def sub_menu():
    global prompts
    
    TO, FRM, TO_FRM, MAIN, SUB = '1','2','3','4','\n---- TRANSACTION QUERY ----\n\n[1]\tto\n[2]\tfrom\n[3]\tto-from\n[4]\tmain menu\n\nchoice: '
   
    choices = [TO, FRM, TO_FRM, MAIN]
    
    choice = None

    while choice != MAIN:
        choice = input(SUB)
        while choice not in choices:
            choice = input(prompts['invalid'])
        if choice == TO:
            print('\n-- TO QUERY --')
            to = input(prompts['to'])
            start = get_start()
            depth = get_depth()
            get_transaction_query(depth=depth,to=to,start=start)
        elif choice == FRM:
            print('\n-- FROM QUERY --')
            fr = input(prompts['from'])
            start = get_start()
            depth = get_depth()
            get_transaction_query(depth=depth,fr=fr,start=start)
        elif choice == TO_FRM:
            print('\n-- TO-FROM QUERY --')
            to = input(prompts['to'])
            fr = input(prompts['from'])
            start = get_start()
            depth = get_depth()
            get_transaction_query(depth,to,fr,start)
            
    
L_BLK, L_TX, MNR_QRY, TX_QRY, QUIT, MENU = '1','2','3','4','5', '\n-------- MAIN MENU --------\n\n[1]\tlatest blocks\n[2]\tlatest transactions\n[3]\tminer query\n[4]\ttransaction query\n[5]\tquit\n\n--------------------------\n\nchoice: '

choices = [L_BLK, L_TX, MNR_QRY, TX_QRY, QUIT]

prompts = {
    'block':'\nenter an integer value for the start block: ',
    'blocks':'\nenter an integer value for the number of blocks to show: ',
    'depth':'\nhow far back do you want to search?\nenter an integer value for the number of blocks: ',
    'from':'\nenter the FROM address to search for: ',
    'invalid':'\ninvalid input\nplease try again: ',
    'miner':'\nenter the miner address to search for: ',
    'start':'\nwhere do you want to start?\n\n[1]\tlatest block\n[2]\tother\n\nchoice: ',
    'to':'\nenter the TO address to search for: ',
    'transactions':'\nenter an integer value for the number of transactions to show: '
    }

if __name__ == '__main__':

    choice = None

    while choice != QUIT:
        choice = input(MENU)
        while choice not in choices:
            choice = input(prompts['invalid'])
        if choice == L_BLK:
            latest_blocks()
        elif choice == L_TX:
            latest_transactions()
        elif choice == MNR_QRY:
            miner_query()
        elif choice == TX_QRY:
            sub_menu()
    
    print('\ngoodbye!\n')
            

        
    

