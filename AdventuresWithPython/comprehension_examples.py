"""
    A couple of list comprehensions and the equivalent for loops.
"""

# A list of the doubles of the values 0 through 9
# list comprehension
doubles = [i*2 for i in range(10)]

# equivalent for loop
doubles = []
for i in range(10):
    doubles.append(i*2)

    
# a list of the doubles of the even values in 0 through 9
# list comprehension
doubles = [i*2 for i in range(10) if i%2==0]

# equivalent for loop
doubles = []
for i in range(10):
    if i%2 == 0:
        doubles.append(i*2)
