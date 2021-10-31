import json
import pickle

# 1) Python script which queries the user for input (infinite loop with exit possibility) and writes input to file
# 2) Add option to user interface - user should be able to output data in terminal
# 3) Store user input to a list and write that list to file with both pickle and json
# 4) Adjust logic to load content to work with pickled/json data

waiting_for_input = True


savestate = []


def get_user_choice():
    """Returns the input of the user to choose an option in the user interface."""
    user_input = input('Input your choice: ')
    return user_input


def save_data():
    user_input = str(input('Input the data to save: '))
    global savestate
    savestate.append(user_input)
    with open('assignment_savedata.p', mode='wb') as f:
        # f.write(json.dumps(input_list))
        f.write(pickle.dumps(savestate))


def load_data():
    with open('assignment_savedata.p', mode='rb') as f:
        global savestate
        savestate = pickle.loads(f.read())


def output_data():
    with open('assignment_savedata.p', mode='rb') as f:
        file_content = pickle.loads(f.read())
        print(file_content)


while waiting_for_input:
    print('Please choose:')
    print('1: Write data to file')
    print('2: Output file data to terminal')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        save_data()
    elif user_choice == '2':
        output_data()
    elif user_choice == 'q':
        print('Quitting...')
        waiting_for_input = False
    else:
        print('Input was invalid, please pick an option from the list.')
