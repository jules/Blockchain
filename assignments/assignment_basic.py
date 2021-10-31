# Basic assignment provided by Academind

def get_name():
    """Returns the user input (their name) as a string. """
    return str(input('What is your name?: '))


def get_age():
    """Returns the user input (their age) as a float. """
    return float(input('What is your age?: '))


def return_two_arguments(argument_1="test 1", argument_2="test 2"):
    """Returns the two user arguments as a single string."""
    return f'{argument_1} {argument_2}'


def return_decades(age_input):
    """Returns the number of decades in the user's input (their age)."""
    return int((age_input - age_input % 10)/10)


print(return_two_arguments(get_name(), get_age()))
print(return_decades(get_age()))
