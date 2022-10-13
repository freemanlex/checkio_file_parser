import os


# Функция для изменения строчек теста в такс-дискрипте на новую строку next-API
def task_desc_change(path: str) -> None:

    with open(f'{path}', mode='r', encoding='utf-8') as task_description:
        lines = task_description.readlines()

    ex = start = 0
    for ind, line in enumerate(lines):
        if "Example:" in line:
            lines[ind] = line.replace('Example: ', 'Example:').\
                              replace('Example:', 'Examples:')
            ex = ind
        elif all([ex, ind > ex,'{% if interpreter.slug' in line]):
            start = ind
        elif all([start, ind > start, '{% endif' in line]):
            lines[start: ind + 1] = '<pre class="brush: {% if is_js %}javascript{% else %}python{% endif %}">{{init_code_tmpl}}</pre>\n'
        else:
            lines[ind] = line.replace('interpreter.slug == "js-node"', 'is_js').\
                              replace("Input: ", "Input:").\
                              replace("Output: ", "Output:")    
        
    with open(rf'{path}', mode='w', encoding='utf-8') as task_description: 
        task_description.write(''.join(lines))

    if (index:=path.find("\\translations")) == -1:
        index = path.find("\\info")
    print(f'{path[index:]} - OK')

def next_api(dir_name: str, mission_name: str) -> None:
    
    # Парсинг файла task_description.html
    for parent, _, files in os.walk(f'{dir_name}\\{mission_name}'):
        if 'task_description.html' in files:
            task_desc_change(parent + '\\' + 'task_description.html')

    # create uk
    if not os.path.exists((path_uk:=f"{dir_name}\\{mission_name}\\translations\\uk\\info")):
        os.makedirs(path_uk)

    # if not os.path.exists(path_uk + "\\task_description.html"):

    #     with open(f"{dir_name}\\{mission_name}\\info\\task_description.html", 'r') as descr,\
    #          open(path_uk + "\\task_description.html", 'w') as descr_uk:
    #         descr_uk.write(descr.read())

    if not os.path.exists(path_uk + "\\task_short_description.html"):

        with open(f"{dir_name}\\{mission_name}\\info\\task_short_description.html", 'r') as descr,\
             open(path_uk + "\\task_short_description.html", 'w') as descr_uk:
            descr_uk.write(descr.read())

    if not os.path.exists((path_uk_h:=f"{dir_name}\\{mission_name}\\translations\\uk\\hints")):
        os.makedirs(path_uk_h)