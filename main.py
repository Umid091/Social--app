import random
import string

d= string.ascii_letters
b = string.digits
m= d+b
print(m)
code = ''
for i in range(4):
    belgi=random.choice(m)
    code= code +belgi
    print(i)
print(code)







