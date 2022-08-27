import re, json


def next_api(directory_name, mission_name):

    # extracting dictionary with tests
    test_py = open(f"{directory_name}\\{mission_name}\\verification\\tests.py", 'r')
    test_py_readlines = test_py.readlines()
    for ind, line in enumerate(test_py_readlines):
        if line.startswith("TESTS ="):
            tests_dict = eval(''.join(test_py_readlines[ind: ])[8: ])
            break
    test_py.close()

    for category in tests_dict.values():
        for dictionary in category:
            inp = dictionary['input']
            if type(inp) != list:
                dictionary['input'] = [inp]

    tests_dict = json.dumps(tests_dict, indent=4)
    tests_dict = re.sub('\"input\": [\n[ ]{18}', '\"input\": [', tests_dict)
    tests_dict = re.sub('\n[ ]{12}]', ']', tests_dict)
    tests_dict = tests_dict.replace('true', 'True').replace('false', 'False')

    test_py = open(f"{directory_name}\\{mission_name}\\verification\\tests.py", 'w')
    test_py.write(
'''\"\"\"
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
\"\"\"

TESTS = ''' + tests_dict)
    test_py.close()