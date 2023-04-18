import sys

input_str = sys.stdin.read()
replaceOne = input_str.replace("\n", "\\n")
replaceTwo = input_str.replace("\t", "\\t")

print(replaceTwo)
