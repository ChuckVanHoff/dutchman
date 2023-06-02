''' This is supposed to be a file that takes data from a receipt and
writes a file containing the json-formatted user inputs.

When running this script the user is prompted for data. 
  -date: should be entered mm-dd-yyyy
  -name: should be entered as it appears on the reciept
  -amount: the dollar amount without the "$" symbol
  -type: either "cash" or "check" or the last four digits of the card
'''


import json
import time
import signal


class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Input timeout")

def store_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)
    return

def get_user_input(storedata=False):
    data = {}
    # Set the timeout to 5 minutes
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(300)
    try:
        data['datetime'] = str(time.time())
        data['date'] = input('Enter the receipt date: ')
        data['name'] = input('Enter the receiver name: ')
        data['amount'] = float(input('Enter the amount: '))
        data['type'] = input('Enter the type: ')
    except TimeoutError:
        print("Input timeout. Returning None.")
        return None
    finally:
        # Disable the alarm
        signal.alarm(0)
    if storedata:
        filename = str(data['name'] + data['date'])
        store_data(data, filename)
    return data

def store_data_from_user_input():
    data = get_user_input()
    # Create a filename from the data and store the data in the file.
    filename = str(data['name'] + data['date'])
    store_data(data, filename)
    return

def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data
        
data = get_user_input(storedata=True)
print(data)
