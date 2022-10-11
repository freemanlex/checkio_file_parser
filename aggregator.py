import os
import init_js, referee, tests, python_3, js_node, task_description


# Directory path
directory_name = "C:\\Users\\ТЕХНОРАЙ\\Documents\\GitHub"
if not os.path.exists(directory_name):
    directory_name = "C:\\Users\\o.zozula\\Documents\\GitHub"
# Mission name
mission_name = "checkio-mission-remove-all-after"
# js modifier
js_complex = True
# py modifier
py_iterable = True

files_to_convert = (
    init_js,
    python_3,
    js_node, 
    task_description, 
    referee, 
    tests, 
)

for file in files_to_convert:
    if file is js_node:
        file.next_api(directory_name, mission_name, js_complex)
    elif file in (python_3, referee):
        file.next_api(directory_name, mission_name, py_iterable)
    else:
        file.next_api(directory_name, mission_name)

# old init files deleting
for file in ("js_node", "python_3", "python_27"):
    try:
        os.remove(f"{directory_name}\\{mission_name}\\editor\\initial_code\\" + file)
    except:
        pass
