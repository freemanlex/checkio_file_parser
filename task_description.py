import os


# Функция для изменения строчек теста в такс-дискрипте на новую строку next-API
def task_desc_change(path):  
    task_description = open(f'{path}', mode='r', encoding='utf-8')
    lines = task_description.readlines()
    if_str = '<pre class="brush: {% if is_js %}javascript{% else %}python{% endif %}">{{init_code_tmpl}}</pre>\n'
    if if_str not in lines:
        task_start = task_end = ex = 0
        for ind, line in enumerate(lines):
            if "Example" in line:
                ex = ind
                  # Определяем границы искомого куска кода по "ключевым" меткам '{% if' и '{% endif'
            elif ind > ex and '{% if interpreter.slug' in line:
                task_start = ind
            elif ind > task_start and '{% endif' in line:
                task_end = ind
            else:
                line.replace("if interpreter.slug == \"js-node\"", "if is_js")
        lines[task_start: task_end + 1] = if_str  # Заменяем ненужный кусок на актуальный код
    task_description.close()
    task_description = open(rf'{path}', mode='w', encoding='utf-8')
    task_description.write(''.join(lines))  # Заново открытый файл перетираем корректным кодом
    task_description.close()
    index = path.find("\\translations")
    if index == -1:
        index = path.find("\\info")
    print(f'{path[index:]} - OK')

def next_api(directory_name, mission_name):
    
    # Парсинг файла task_description.html
    # Используем библиотеку "os" и находим все файлы таск-дискрипта. Используя функцию task_desc_change, изменяем эти файлы
    walking = os.walk(f'{directory_name}\\{mission_name}')
    for i in walking:
        if 'task_description.html' in i[2]:  # Находим по директориям где есть нужный нам файл
            for u in i[2]:
                if u == 'task_description.html':  # Берем нужный нам файл и крепим к директории
                    path_info = i[0] + '\\' + u
                    task_desc_change(path_info)  # Вызываем функцию передавая ей каждый раз новый путь для изменений

    # create uk
    path_uk = f"{directory_name}\\{mission_name}\\translations\\uk\\info"
    if not os.path.exists(path_uk):
        os.makedirs(path_uk)
    if not os.path.exists(path_uk + "\\task_description.html"):
        descr = open(f"{directory_name}\\{mission_name}\\info\\task_description.html", 'r')
        descr_uk = open(path_uk + "\\task_description.html", 'w')
        descr_uk.write(descr.read())
        descr.close()
        descr_uk.close()
    if not os.path.exists(path_uk + "\\task_short_description.html"):
        descr = open(f"{directory_name}\\{mission_name}\\info\\task_short_description.html", 'r')
        descr_uk = open(path_uk + "\\task_short_description.html", 'w')
        descr_uk.write(descr.read())
        descr.close()
        descr_uk.close()