import random
import datetime

# 1) Import random function, generate both a random number 
# between 0 and 1 as well as a random number between 1 and 10.
rn_1 = random.random()
rn_2 = random.randint(1, 10)
print(rn_1, rn_2)

# 2) Use the datetime library together with the random number to generate a random, unique value
right_now = datetime.datetime.now().isoformat()
print(right_now)
unique_value = f'{right_now}-{rn_1}-{rn_2}'
print(unique_value)