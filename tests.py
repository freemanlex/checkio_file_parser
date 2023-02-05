import os
from pathlib import Path

# parsing function arguments


def args_parse(directory_name: str, mission_name: str) -> dict:

    file_path = f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3.tmpl"
    # if not os.path.exists(file_path):
    #     file_path = f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3"

    with open(file_path, 'r') as python_3:
        python_3_readLines = python_3.readlines()

    for line in python_3_readLines:
        if line.startswith('def'):
            init_string = line[line.index('(') + 1: line.index(')')]
            break

    # replacing commas inside typehints with '.', commas between args with '*'
    cache = ''
    for char in init_string:
        if char == '[':
            cache += char
        elif char == ']':
            cache = cache[:-1]
        elif char == ',':
            init_string = init_string.replace(',', ('.', '*')[not cache], 1)
    # replacing '.' inside typehints back to ','
    init_string = init_string.replace('.', ',')
    # creating dict with name of args and if present - typehint and default value
    final_dict = {}
    for arg in map(str.strip, init_string.split('*')):
        val = typehint = None
        if '=' in arg:
            arg, val = map(str.strip, arg.split('='))
        if ':' in arg:
            arg, typehint = map(str.strip, arg.split(':'))
            if (ind := typehint.find("[")) != -1:
                typehint = typehint[:ind], typehint[ind + 1: -1]
        final_dict[arg] = typehint, val

    return final_dict


def next_api(directory_name: str, mission_name: str) -> None:

    # print(args_parse(directory_name, mission_name))
    changed = False
    # changing output to list
    with open(f"{directory_name}\\{mission_name}\\verification\\tests.py", 'r') as test_py:
        test_py_readlines = test_py.readlines()

    for ind, line in enumerate(test_py_readlines):
        # print(line)
        if (l := line.lstrip()).startswith('"input":'):
            start = ind
            # print(start)
        elif l.startswith('"answer":'):
            end = ind
            # print(end)
            test = "".join(test_py_readlines[start: end]).strip()
            title, out = test.split(":", 1)
            # print(out.strip(", \n"))
            if type(eval(out.strip(", \n"))) != list:
                changed = True
                out = '[' + out.strip(", \n") + '],\n'
                test_py_readlines[start: end] = ' ' * 12 + ": ".join([title, out])
        # elif line.startswith(' '*8 + '}'):
        #     if not test_py_readlines[ind-1].endswith(",\n"):
        #         test_py_readlines[ind-1] += ","
        #     if not line.endswith(","):
        #         test_py_readlines[ind] += ","

    Path(f"{directory_name}\\{mission_name}\\verification\\tests.py").write_text("".join(test_py_readlines))
    if changed:
        print("\\verification\\tests.py - OK")
