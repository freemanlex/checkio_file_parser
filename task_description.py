import os


# Функция для изменения строчек теста в такс-дискрипте на новую строку next-API
def task_desc_change(path: str) -> None:

    with open(f'{path}', mode='r', encoding='utf-8') as task_description:
        lines = task_description.readlines()
        if_str = '<pre class="brush: {% if is_js %}javascript{% else %}python{% endif %}">{{init_code_tmpl}}</pre>\n'
        #if if_str not in lines:
        task_start = task_end = ex = 0
        for ind, line in enumerate(lines):
            print(line)
            if "Example" in line:
                ex = ind
            # Определяем границы искомого куска кода по "ключевым" меткам '{% if' и '{% endif'
            elif all([ex, ind > ex,'{% if interpreter.slug' in line]):
                task_start = ind
            elif all([task_start, ind > task_start, '{% endif' in line]):
                task_end = ind
            else:
                lines[ind] = line.replace("interpreter.slug == \"js-node\"", "is_js")
        if task_start:
            lines[task_start: task_end + 1] = if_str  # Заменяем ненужный кусок на актуальный код

    with open(rf'{path}', mode='w', encoding='utf-8') as task_description: 
        task_description.write(''.join(lines))  # Заново открытый файл перетираем корректным кодом

    index = path.find("\\translations")
    if index == -1:
        index = path.find("\\info")
    print(f'{path[index:]} - OK')

def next_api(directory_name: str, mission_name: str) -> None:
    
    # Парсинг файла task_description.html
    for parent, _, files in os.walk(f'{directory_name}\\{mission_name}'):
        if 'task_description.html' in files:
            task_desc_change(parent + '\\' + 'task_description.html')

    # create uk
    path_uk = f"{directory_name}\\{mission_name}\\translations\\uk\\info"
    if not os.path.exists(path_uk):
        os.makedirs(path_uk)
        
    if not os.path.exists(path_uk + "\\task_description.html"):

        with open(f"{directory_name}\\{mission_name}\\info\\task_description.html", 'r') as descr,\
             open(path_uk + "\\task_description.html", 'w') as descr_uk:
            descr_uk.write(descr.read())

    if not os.path.exists(path_uk + "\\task_short_description.html"):

        with open(f"{directory_name}\\{mission_name}\\info\\task_short_description.html", 'r') as descr,\
             open(path_uk + "\\task_short_description.html", 'w') as descr_uk:
            descr_uk.write(descr.read())
