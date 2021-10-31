list_of_names = ['Jon', 'Joe', 'Jotaro', 'Josuke', 'Giorno','Jolyne','Johnny', 'Jonno', 'Jonathan', 'Nathan']


print('Printing lengths of all names:')
for name in list_of_names:
    print(f'{name} - {len(name)} characters long')
print('--------')

print('Printing all names longer than 5 letters')
for name in list_of_names:
    if len(name) > 5:
        print(name)
print('--------')

print('Printing all names longer than 5 letters that contain the letter "n" or "N"')
for name in list_of_names:
    if len(name) > 5 and ('n' in name or 'N' in name):
        print(name)
print('--------')

print('Emptying list of all names')
while len(list_of_names) >= 1:
    print(f'Popping value: {list_of_names.pop()}')

print('--------')
print('Done.')