import re

a = "DataBaseUser"

print((re.sub(r"(?<!^)(?=[A-Z])", r"_", a).lower()))
