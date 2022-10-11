import os


# Функция для изменения строчек теста в такс-дискрипте на новую строку next-API
def task_desc_change(path: str) -> None:

    with open(f'{path}', mode='r', encoding='utf-8') as task_description:
        lines = task_description.readlines()

    if_str = '<pre class="brush: {% if is_js %}javascript{% else %}python{% endif %}">{{init_code_tmpl}}</pre>\n'
    for ind, line in enumerate(lines):
        if "Example" in line:
            ex = ind
        elif all([ex, ind > ex,'{% if interpreter.slug' in line]):
            task_start = ind
        elif all([task_start, ind > task_start, '{% endif' in line]):
            lines[task_start: ind + 1] = if_str
        else:
            lines[ind] = line.replace("interpreter.slug == \"js-node\"", "is_js")
        
    with open(rf'{path}', mode='w', encoding='utf-8') as task_description: 
        task_description.write(''.join(lines))

    if (index:=path.find("\\translations")) == -1:
        index = path.find("\\info")
    print(f'{path[index:]} - OK')

def next_api(directory_name: str, mission_name: str) -> None:
    
    # Парсинг файла task_description.html
    for parent, _, files in os.walk(f'{directory_name}\\{mission_name}'):
        if 'task_description.html' in files:
            task_desc_change(parent + '\\' + 'task_description.html')

    # create uk
    if not os.path.exists((path_uk:=f"{directory_name}\\{mission_name}\\translations\\uk\\info")):
        os.makedirs(path_uk)
        
    if not os.path.exists(path_uk + "\\task_description.html"):

        with open(f"{directory_name}\\{mission_name}\\info\\task_description.html", 'r') as descr,\
             open(path_uk + "\\task_description.html", 'w') as descr_uk:
            descr_uk.write(descr.read())

    if not os.path.exists(path_uk + "\\task_short_description.html"):

        with open(f"{directory_name}\\{mission_name}\\info\\task_short_description.html", 'r') as descr,\
             open(path_uk + "\\task_short_description.html", 'w') as descr_uk:
            descr_uk.write(descr.read())
