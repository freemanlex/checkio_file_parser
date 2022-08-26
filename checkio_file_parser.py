'''
Парсер для файлов next-API платформы Checkio
'''
import os, json, re
# from googletrans import Translator

# Вставить путь к папке миссии
directory_name = 'C:\\Users\\ТЕХНОРАЙ\\Documents\\GitHub'
# Вставить название миссии
mission_name = 'checkio-mission-acceptable-password-4'  

# Функция для обрезки экзампла в файле js_node.tmpl
def example_cutter(exmpl):  
    js_fin = exmpl
    js_ex_reverse = js_fin[::-1]  # Переворачивается пример, для удобной обрезки по "ключевой" метке
    for i in range(len(js_ex_reverse)):
        if js_ex_reverse[i] == ',' and js_ex_reverse[i + 1] == ')':  # "Ключевая" метка это ",)", в прямой строке "),"
            js_ex_reverse = js_ex_reverse[i + 1:]  # что является концом условия и началом предполагаемого ответа
            js_fin = js_ex_reverse[::-1] + ")\n"
            break
    return js_fin  # Возврат отредактированного куска

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
        lines[task_start: task_end + 1] = if_str  # Заменяем ненужный кусок на актуальный код
    task_description.close()
    task_description = open(rf'{path}', mode='w', encoding='utf-8')
    task_description.write(''.join(lines))  # Заново открытый файл перетираем корректным кодом
    task_description.close()
    index = path.find("\\translations")
    if index == -1:
        index = path.find("\\info")
    print(f'{path[index:]} - OK')

# parsing function arguments
def args_parse(line: str) -> dict:

    # replacing commas inside typehints with '.', commas between args with '*'
    cache = ''
    for char in line:
        if char == '[':
            cache += char
        elif char == ']':
            cache = cache[:-1]
        elif char == ',':
            line = line.replace(',', ('.', '*')[not cache], 1)
    # replacing '.' inside typehints back to ','
    line = line.replace('.', ',')
    # creating dict with name of args and if present - typehint and default value
    final_dict = {}
    for arg in map(str.strip, line.split('*')):
        val = typehint = None
        if '=' in arg:
            arg, val = list(map(str.strip, arg.split('=')))
        if ':' in arg:
            arg, typehint = list(map(str.strip, arg.split(':')))
        final_dict[arg] = typehint, val

    return final_dict

# getting function names
referee_py = open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'r')
for line in referee_py.readlines():
    if line.lstrip().startswith("\"python"):
        func_name = line.split(":")[1].strip()[1:-2]
    elif line.lstrip().startswith("\"js"):
        js_func_name = line.split(":")[1].strip()[1:-1]
        break
referee_py.close()

# Парсинг файла init.js
# Просто перетираем файл на новый код
try:
    init_js = open(f"{directory_name}\\{mission_name}\\editor\\animation\\init.js", 'w')
    init_js.write(
'''requirejs(['ext_editor_io2', 'jquery_190'],
    function (extIO, $) {
        var io = new extIO({});
        io.start();
    }
);
''')
except: print("init.js - PROBLEM!!")
else: print("\\editor\\animation\\init.js - OK")
finally: init_js.close()


# Парсинг файла python_3.tmpl

python_3 = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3", 'r')
python_3_readLines = python_3.readlines()

imp_str = ''  # импортируемые библиотеки
func_str = ''  # initial код функции
a = 0
b = 0  # Markers for 'def' search
example_str = ''  # Строка, в которой будет храниться код print(func(...))
end = ''
c = 0
d = 0  # Markers for 'assert' search

for ind, line in enumerate(python_3_readLines):
    if line.startswith('from') or line.startswith('import'):
        imp_str += line.strip()  # Ищем по тексту импортированные библиотеки
    elif line.startswith('def'):
        a = ind
        init_string = line[line.index('(') + 1: line.index(')')]
    elif line.lstrip().startswith('return'):
        b = ind  # Конец initial кода функции
    elif line.lstrip().startswith('assert'):
        c = ind  # Начало кода в print(func(...))
        if '==' in line:
            end = line[ : line.index(' ==')]
            break
    elif '==' in line:
        d = ind  # Конец кода в print(func(...))
        end = line[ : line.index(' ==')]  # Отрезать часть "ожидаемый" ответ
        break  # Примеров может быть много, чтобы забрать самый первый пример, мы выходим на данном моменте из цикла

func_str = ''.join(python_3_readLines[a: b])
example_str = ''.join(python_3_readLines[c: d])[11: ] + end if d != 0 else ''.join(end)[11: ]

# Текст заполняемый в новый файл
python_3_tmpl = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3.tmpl", 'w')
if func_str:    
    python_3_tmpl.write(
'''{% comment %}New initial code template{% endcomment %}
{% block env %}''' + imp_str[: -1] + '''{% endblock env %}

{% block start %}''' 
+ func_str +
"""{% endblock start %}

{% block example %}
print('Example:')
print(""" + example_str + ''')
{% endblock %}
''')
python_3_tmpl.write(
'''{% block tests %}
{% for t in tests %}
assert {% block call %}''' + func_name + '''({{t.input|p_args}}){% endblock %} == {% block result %}{{t.answer|p}}{% endblock %}{% endfor %}
{% endblock %}''')
if func_str:    
    python_3_tmpl.write(
'''
{% block final %}
print("The mission is done! Click \'Check Solution\' to earn rewards!")
{% endblock final %}''')

python_3_tmpl.close()
python_3.close()
print("\\editor\\initial_code\\python_3.tmpl - OK")


# Парсинг файла js_node.tmpl

js_node = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\js_node", 'r')
js_node_readLines = js_node.readlines()

js_imp_str = ''  # импортируемые библиотеки
js_func_str = ''  # initial код функции
js_a = 0
js_b = 0  # Markers for 'def' search
js_example_str = ''  # Строка, в которой будет храниться код console.log(func(...))
js_count = 0  # Переменная для поимки первого примера
js_c = 0
js_d = 0  # Markers for 'assert' search
js_ex = ''

for ind, line in enumerate(js_node_readLines):
    if line.startswith('import'):
        if not line.startswith('import assert from "assert"'):
            js_imp_str += line  # Ищем по тексту импортированные библиотеки
    elif line.startswith('function'):
        js_a = ind
        js_bracket = line.index('(')   # Начало initial кода функции
    elif line.startswith("}"):
        js_b = ind + 1  # Конец initial кода функции
    elif line.strip().startswith("assert"):  # Начало кода console.log(func(...))
        if js_count == 1:  # На втором кругу попадаем сюда, получаем конец первого примера и выходим из цикла
            js_d = ind
            js_ex = ''.join(js_node_readLines[js_c : js_d])[line.find('ual(') + 4 : ]
            break
        js_c = ind  # Начало кода из первого примера
        js_count += 1


js_func_str = ''.join(js_node_readLines[js_a : js_b])
# Так как со стройкой екзампла в джаве есть трудность (в большом количестве запятых еще до самого екзампла), реализовал обрезку функцией
js_example_str = example_cutter(js_ex) if js_d != 0 else example_cutter(''.join(js_node_readLines[js_c])[13 : ])

js_node_tmpl = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\js_node.tmpl", 'w')
if js_func_str:
    js_node_tmpl.write(
'''{% comment %}New initial code template{% endcomment %}
{% block env %}import assert from "assert";'''+ js_imp_str[ : -1] +'''{% endblock env %}

{% block start %}'''
+ js_func_str +
'''{% endblock start %}

{% block example %}
console.log('Example:');
console.log(''' + js_example_str +
'''{% endblock %}
''')
js_node_tmpl.write(
'''// These "asserts" are used for self-checking
{% block tests %}
{% for t in tests %}
assert.strictEqual({% block call %}''' + js_func_name + '''({{t.input|j_args}}){% endblock %}, {% block result %}{{t.answer|j}}{% endblock %});{% endfor %}
{% endblock %}''')
if js_func_str:
    js_node_tmpl.write(
'''
{% block final %}
console.log("Coding complete? Click \'Check Solution\' to earn rewards!");\n{% endblock final %}''')

js_node_tmpl.close()
js_node.close()
print("\\editor\\initial_code\\js_node.tmpl - OK")

# old init files deleting
files_to_del = "js_node", "python_3", "python_27"
for file in files_to_del:
    try:
        os.remove(f"{directory_name}\\{mission_name}\\editor\\initial_code\\" + file)
    except:
        pass

# Парсинг файла task_description.html
# Используем библиотеку "os" и находим все файлы таск-дискрипта. Используя функцию task_desc_change, изменяем эти файлы
walking = os.walk(f'{directory_name}\\{mission_name}')
for i in walking:
    if 'task_description.html' in i[2]:  # Находим по директориям где есть нужный нам файл
        for u in i[2]:
            if u == 'task_description.html':  # Берем нужный нам файл и крепим к директории
                path_info = i[0] + '\\' + u
                task_desc_change(path_info)  # Вызываем функцию передавая ей каждый раз новый путь для изменений


# text_1 = os.walk(f'{directory_name}\\{mission_name}\\hints')
# text_2 = open(f"{directory_name}\\{mission_name}\\hints\\{list(text_1)[0][2][0]}", 'r')
# texts = text_2.read()
# new_text = ''''''
# trns = Translator()

# for i in texts.split('\n'):
#     if i.strip().startswith('<'):
#         continue
#     else:
#         new_text += i + '\n'

# text_2.close()
# print('HINTS:\n', trns.translate(new_text, src='en', dest='uk').text)

# task_desc_trns = open(f"{directory_name}\\{mission_name}\\info\\task_description.html", 'r')
# task_2 = task_desc_trns.read()
# new_text = ''''''

# for i in task_2.split('\n'):
#     if i.strip().startswith('<'):
#         continue
#     else:
#         new_text += i + '\n'

# task_desc_trns.close() 
# print('-'*200, '\nTASK:\n', trns.translate(new_text, src='en', dest='uk').text)


# Парсинг файла referee.py
# Имена функций мы уже получили в двух переменных выше "func_name" для пайтона и "js_func_name" для джавы




try:
    referee_py = open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'w')
    referee_py.write(
'''from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.io_template import CheckiOReferee
# from checkio.referees.checkers import to_list

from tests import TESTS

api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        # checker=to_list,
        function_name={
            "python": ''' + func_name + ''',
            "js": ''' + js_func_name + '''
        },
        cover_code={
            'python-3': {},
            'js-node': {
                # "dateForZeros": True,
            }
        }
    ).on_ready)\n''')
except: print("\\verification\\referee.py - PROBLEM!")
else: print("\\verification\\referee.py - OK")
finally: referee_py.close()


# extracting dictionary with tests
test_py = open(f"{directory_name}\\{mission_name}\\verification\\tests.py", 'r')
test_py_readlines = test_py.readlines()
for ind, line in enumerate(test_py_readlines):
    if line.startswith("TESTS ="):
        tests_dict = eval(''.join(test_py_readlines[ind: ])[8: ])
        break
test_py.close()

for category in tests_dict.values():
    for dictionary in category:
        inp = dictionary['input']
        if type(inp) != list:
            dictionary['input'] = [inp]

tests_dict = json.dumps(tests_dict, indent=4)
tests_dict = re.sub('\"input\": [\n[ ]{18}', '\"input\": [', tests_dict)
tests_dict = re.sub('\n[ ]{12}]', ']', tests_dict)
tests_dict = tests_dict.replace('true', 'True').replace('false', 'False')

test_py = open(f"{directory_name}\\{mission_name}\\verification\\tests.py", 'w')
test_py.write(
'''\"\"\"
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
\"\"\"

TESTS = ''' + tests_dict)
test_py.close()

# create uk
path_uk = f"{directory_name}\\{mission_name}\\translations\\uk\\info"
if not os.path.exists(path_uk):
    os.makedirs(path_uk)
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