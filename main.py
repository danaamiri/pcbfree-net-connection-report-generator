import csv
import os
import re
import report as r

file_path = 'pcb-file.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

parts = []
nets = []
vcc = []
gnd = []
partIndicatorFound = False
netIndicatorFound = False


for index, line in enumerate(lines):
    if line.startswith("*PART*"):
        partIndicatorFound = True
        continue
    if line.startswith("*NET*"):
        netIndicatorFound = True
        continue
    if line.startswith("*END*"):
        break
    if line == "\n":
        partIndicatorFound = False
        netIndicatorFound = False
    if netIndicatorFound: 
        if "VCC" in line:
            addingLine = lines[index + 1].split(" ")
            addingLine.pop()
            vcc = addingLine
        elif "GND" in line:
            addingLine = lines[index + 1].split(" ")
            addingLine.pop()
            gnd = addingLine
        if(line.startswith("*")):
            addingLine = lines[index + 1].split(" ")
            addingLine.pop()
            nets.append(addingLine)
    if partIndicatorFound:
        parts.append(line.split(" ")[0])
        
short_circuite = set(vcc).intersection(gnd)

if short_circuite:
    print(f"Common items: {short_circuite}")
    exit()

part_connection = {k: {} for k in parts}
for part in parts:
    for net in nets:
        for pin in net:
            if part in pin:
                pin_dict = part_connection[part]
                key = int(pin.split(".")[1])
                pin_dict[key] = []
                
    part_connection[part] = dict(sorted(part_connection[part].items()))
    
for part in parts:
    pin_dict = part_connection[part]
    for net in nets:
        for pin in net:
            key = int(pin.split(".")[1])
            keyPin = part + "." + str(key)
            if(pin == keyPin):
                pinList = []
                pinList.extend(net)
                if keyPin in pinList:
                    pinList.remove(keyPin)
                pin_dict[key].extend(pinList)

for part in parts:
    for net in nets:
        pin_dict = part_connection[part]
        for pin in net:
            key = int(pin.split(".")[1])
            keyPin = part + "." + str(key)
            if keyPin in vcc:
                pin_dict[key] = ["VCC"]
            if keyPin in gnd:
                pin_dict[key] = ["GND"]
            

output_directory = 'output_csv_files'

prefixes = sorted(list(set([item.rstrip('0123456789') for item in part_connection.keys()])))

os.makedirs(output_directory, exist_ok=True)

connections = {key: {} for key in prefixes}
for prefix in prefixes:
    for component in part_connection:
        stc = component.rstrip('0123456789')
        if stc == prefix:
            pfDict = connections[prefix]
            pfDict[component] = part_connection[component]

for prefix, component in connections.items():
    filename = os.path.join(output_directory, f'{prefix}_pins.csv')
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        firstIt = True
        colSize = max(part_connection[max(component)].keys())
        for k, pins in component.items():
            stc = k.rstrip('0123456789')
            if stc == prefix:
                if firstIt:
                    csvwriter.writerow(['PartNo/Pin'] + list(range(1, colSize + 1)))
                firstIt = False
                row_data = [k]
                for pin_num in range(1, max(pins.keys()) + 1):
                    row_data.append('\n'.join(pins.get(pin_num, [''])))
                csvwriter.writerow(row_data)
            