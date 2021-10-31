import copy

# 1) Create a list of person dictionaries with a name, age, and list of hobbies for each person.
persons = [
    {
        'name': 'Julian',
        'age': 20,
        'hobbies': ['piano', 'gaming', 'chess']
    },
    {
        'name': 'Rick',
        'age': 73,
        'hobbies': ['science', 'adventure']
    },
    {
        'name': 'Jonathan',
        'age': 50,
        'hobbies': ['archery', 'chess']
    },
    {
        'name': 'Barry',
        'age': 17,
        'hobbies': ['gaming', 'science']
    }
]

# 2) Use a list comprehension to convert this list into a list of 
#    names of the persons
names = [person['name'] for person in persons]
print('Printing names...')
print(names)
print('')

# 3) Use a list comprehension to check whether all persons are older
#    than 20
print('Checking age...')
if all([person['age'] > 20 for person in persons]):
    print('All persons older than 20.')
else:
    print('Not all persons older than 20.')
print('')

# 4) Copy the person list so I can safely edit the name of the first 
#    person (without changing original list)
copied_persons = copy.deepcopy(persons)
copied_persons[0]['name'] = 'King Jules'
print('Printing new list...')
print(copied_persons)
print('')
print('Printing old list...')
print(persons)
print('')

# 5) Unpack the persons of the original list into different variables
#    and output these variables.
a, b, c, d = persons
print('Printing persons...')
print(a)
print(b)
print(c)
print(d)