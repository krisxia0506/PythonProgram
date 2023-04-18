words = input()
words = words.split()
words = [x.lower() for x in words]
c = len(words)
j = ''
target = []
for i in range(0, c):
    if words[i - 1].endswith('.'):
        j = words[i].capitalize()
        target.append(j)
    elif words[i] == 'i' and words[i - 1].endswith(','):
        j = 'I'
        target.append(j)

    else:
        j = words[i]
        target.append(j)

for x in target:
    print(x, end=' ')
