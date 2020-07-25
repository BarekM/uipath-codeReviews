import re


p = '[a-z]+'

x = re.match(p, "123")
if not(x):
    print(x)