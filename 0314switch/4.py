dict = {"agree": 0, "disagree": 0}
while True:
    a = input()
    if a == "1":
        dict["agree"] += 1
    elif a == "0":
        dict["disagree"] += 1
    elif a == "-1":
        break
if dict["agree"] >= dict["disagree"]:
    print("Yes")
elif dict["agree"] < dict["disagree"]:
    print("No")