import re

a = input()

print((re.sub(r"(?<!^)(?=[A-Z])", r"_", a).lower()))
