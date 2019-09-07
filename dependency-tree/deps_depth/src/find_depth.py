import sys
import json
import subprocess
import ast

def find_depth(path):
    with open("get_name.sh", 'w') as file:
        file.write('#!/bin/bash\n')
        file.write('cut -d "=" -f 2 <<< $(npm run env | grep "npm_package_name")')

    temp = subprocess.check_output(['chmod','+x', 'get_name.sh'])
    name = subprocess.check_output(['./get_name.sh'])
    #print(name)
    '''
    temp = subprocess.check_output(["npm", "install"])
    try:
        dict = subprocess.check_output(["npm","ls","-j"])
    except:
        temp = subprocess.check_output(["npm-install-missing"])
        dict = subprocess.check_output(["npm","ls","-j"])
    dict = dict.decode('utf-8')
    dict = ast.literal_eval(dict)
    '''
    pkg = name.decode('utf-8')
    tree = subprocess.check_output(["npm-remote-ls", pkg])
    file = tree.decode('utf-8')
    #print(file)
    file = file.split('\n')
    max_depth = 0
    for line in file:
        char_count = 0
        for letter in line:
            if letter.isalpha():
                break
            char_count = char_count + 1
        if(char_count > max_depth):
            max_depth = char_count

    max_depth = (max_depth/3) - 1
    #print(max_depth)
    #print("Finding depth in file {}".format(path))
    result = {}
    result["check_id"] = pkg
    result["path"] = path
    result["extra"] = {}
    result["extra"]["depth"] = max_depth
    return result

all_results = []
for path in sys.argv[1:]:
    all_results.append(find_depth(path))

with open("/analysis/output/output.json", "w") as output:
    output.write(json.dumps({"results": all_results}, sort_keys=True, indent=4))
