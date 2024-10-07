import copernicusmarine as cm

help(cm.subset)

string = """{zero} hola {one} {one}, {zero}"""

numbers_dict = {"one": "1", "two": "2", "zero": "3"}

print(numbers_dict)
print(string.format(**numbers_dict))
