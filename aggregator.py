import os
import init_js
import referee
import tests
import python_3
import js_node
import task_description


# Directory path
if not os.path.exists((dir_name := "C:\\Users\\ТЕХНОРАЙ\\Documents\\GitHub")):
    dir_name = "C:\\Users\\o.zozula\\Documents\\GitHub"
# Mission name
mission_name = "checkio-task-sums-in-a-triangle"
# js modifier
js_complex = False
# py modifier
py_iterable = False

# commenting allows to migrate separate files
files_to_convert = (
    init_js,
    python_3,
    js_node,
    task_description,
    referee,
    # tests,
)

for file in files_to_convert:
    if file is js_node:
        file.next_api(dir_name, mission_name, js_complex)
    elif file in (python_3, referee):
        file.next_api(dir_name, mission_name, py_iterable)
    else:
        file.next_api(dir_name, mission_name)

# old init files deleting
for file in ("js_node", "python_3", "python_27"):
    try:
        os.remove(f"{dir_name}\\{mission_name}\\editor\\initial_code\\" + file)
    except:
        pass

if not os.path.exists(f"{dir_name}\\{mission_name}\\.gitignore"):

    with open(f"{dir_name}\\{mission_name}\\.gitignore", 'w') as gitignore:
        gitignore.write(
            '''.vscode

*.py[cod]

# C extensions
*.so

# Packages
*.egg
*.egg-info
dist
build
eggs
parts
bin
var
sdist
develop-eggs
.installed.cfg
lib
lib64

# Installer logs
pip-log.txt

# Unit test / coverage reports
.coverage
.tox
nosetests.xml

# Translations
*.mo

# Mr Developer
.mr.developer.cfg
.project
.pydevproject
.idea

.DS_Store
__VERSION__.py

__pycache__
'''
        )
