def extract_func_names(directory_name, mission_name):

    referee_py = open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'r')
    for line in referee_py.readlines():
        if line.lstrip().startswith("\"python"):
            func_name = line.split(":")[1].strip()[1:-2]
        elif line.lstrip().startswith("\"js"):
            js_func_name = line.split(":")[1].strip()[1:-1]
            break
    referee_py.close()

    return func_name, js_func_name

def next_api(directory_name, mission_name, py_iterable):

    func_name, js_func_name = extract_func_names(directory_name, mission_name)

    try:
        referee_py = open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'w')
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
    except:
        print("\\verification\\referee.py - PROBLEM!")
    else:
        print("\\verification\\referee.py - OK")
    finally:
        referee_py.close()