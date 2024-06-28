import json

file = "egypt_netnames.json"

with open(file, 'r') as f:
    cp = json.load(f)
    dict_1 = {}
    for item in cp:
        if item[1] not in dict_1:
            dict_1[item[1]] = [item[0]]
        else:
           dict_1[item[1]].append(item[0])

    print(dict_1)
    
    with open("formated json.json", 'w') as fg:
        json.dump(dict_1, fg)