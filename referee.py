def extract_func_names(directory_name: str, mission_name: str) -> tuple[str, str]:

    with open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'r') as referee_py:
        for line in referee_py.readlines():
            if line.lstrip().startswith("\"python"):
                func_name = line.split(":")[1].strip("\", \n")
            elif line.lstrip().startswith("\"js"):
                js_func_name = line.split(":")[1].strip("\", \n")
                break

    return func_name, js_func_name

def next_api(directory_name: str, mission_name: str, py_iterable: bool) -> None:

    func_name, js_func_name = extract_func_names(directory_name, mission_name)

    with open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'w') as referee_py:

        referee_py.write(
'''from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.io_template import CheckiOReferee
''' + '# '*(not py_iterable) + '''from checkio.referees.checkers import to_list

from tests import TESTS

api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        ''' + '# '*(not py_iterable) + '''checker=to_list,
        function_name={
            "python": "''' + func_name + '''",
            "js": "''' + js_func_name + '''"
        },
        cover_code={
            'python-3': {},
            'js-node': {
                # "dateForZeros": True,
            }
        }
    ).on_ready)\n''')

    print("\\verification\\referee.py - OK")