# 1) Write a normal with def keyword function that accepts another function as an argument.
#    Output the result of that other function in normal function.
def diymap(function_arg, function_input):
    return function_arg(function_input)


def successor(number):
    return number + 1


print(diymap(successor, 13))

# 2) Call normal function by calling a lambda function - which performs any operation - as an argument
print(diymap(lambda number: number * 2, 5))


# 3) Tweak normal function by enabling infinite number of arguments on which lambda function will be executed
def diymaptwo(function_arg, *function_inputs):
    for el in function_inputs:
        print(function_arg(el))


diymaptwo(lambda number: number * 2, 10, 13, 7, 3)


# 4) Format output of normal function so that numbers look nice and are centred within 20 character column.
def diymapthree(function_arg, *function_inputs):
    for el in function_inputs:
        print('Output of DIY Map 3: {:-^20}'.format(function_arg(el)))


diymapthree(lambda number: number * 2, 2.4, 5, 6, 173)
