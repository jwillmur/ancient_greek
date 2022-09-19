import re

text = input("Enter text: ")
lines = input("Enter lines xx-xx: ")

start = re.search('\d+-', lines)
end = re.search('-\d+', lines)

print(text, start, end)
