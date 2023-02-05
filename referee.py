from pathlib import Path


def extract_func_names(directory_name: str, mission_name: str) -> tuple[str, str]:

    func_name = js_func_name = ""
    with open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'r') as referee_py:
        referee_lines = referee_py.readlines()

    for line in referee_lines:
        l = line.lstrip()
        if l.startswith(("\"python", "\'python")):
            func_name = line.split(":")[1].strip("\", \', \n")
        elif l.startswith(("\"js", "\'js")):
            js_func_name = line.split(":")[1].strip("\", \', \n")
            break

    if not func_name:
        for line in referee_lines:
            if line.lstrip().startswith("function_name"):
                func_name = line.split("=")[1].strip("\", \n")
                break
    if not js_func_name:
        s = func_name.split("_")
        js_func_name = s[0] + "".join(map(str.capitalize, s[1:]))

    return func_name, js_func_name


def next_api(directory_name: str, mission_name: str, py_iterable: bool) -> None:

    func_name, js_func_name = extract_func_names(directory_name, mission_name)

    Path(f"{directory_name}\\{mission_name}\\verification\\referee.py").write_text(
        '''from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.io_template import CheckiOReferee
''' + '# ' * (not py_iterable) + '''from checkio.referees.checkers import to_list

from tests import TESTS

api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        ''' + '# ' * (not py_iterable) + '''checker=to_list,
        function_name={
            "python": "''' + func_name + '''",
            "js": "''' + js_func_name + '''"
        },
        cover_code={
            "python-3": {},
            "js-node": {
                # "dateForZeros": True,
            }
        }
    ).on_ready)\n''')

    print("\\verification\\referee.py - OK")
