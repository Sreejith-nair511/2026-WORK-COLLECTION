# Bad ML-style code (conceptually wrong + poor practice)

data = [1, 2, 3, 4, 5]
result = []

for i in data:
    if i > 3:
        result.append("Pass")
    else:
        result.append("Fail")

print(result)

# Issues:
# 1. Using a loop with conditional statements instead of functional programming constructs.

# 2. Appending to a list in a loop is less efficient and less readable.

#No training concept

#No separation of data, model, prediction

#Not reusable or extensible

#This is just IF-ELSE, not ML thinking