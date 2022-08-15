'''
Парсер для файлов next-API платформы Checkio
'''
from os import walk
from googletrans import Translator


directory_name = 'C:\\Users\\Infotech_5\\OneDrive\\Документы\\GitHub'  # Всавить путь к папке мисси
mission_name = 'checkio-mission-bigger-price'  # Всавить название миссии


def example_cutter(exmpl):  # Функция для обрезки экзампла в файле js_node.tmpl
    js_fin = exmpl
    js_ex_reverse = js_fin[::-1]  # Переворачивается пример, для удобной обрезки по "ключевой" метке
    for i in range(len(js_ex_reverse)):
        if js_ex_reverse[i] == ',' and js_ex_reverse[i + 1] == ')':  # "Ключевая" метка это ",)", в прямой строке "),"
            js_ex_reverse = js_ex_reverse[i + 1:]  # что является концом условия и началом предполагаемого ответа
            js_fin = js_ex_reverse[::-1] + ")\n"
            break
    return js_fin  # Возврат отредактированного куска


def task_desc_change(path):  # Функция для изменения строчек теста в такс-дискрипте на новую строку next-API
    task_descrption = open(f'{path}', mode='r', encoding='utf-8')
    lines = task_descrption.readlines()

    if_str = ['<pre class="brush: {% if is_js %}javascript{% else %}python{% endif %}">{{init_code_tmpl}}</pre>\n']
    if ''.join(if_str) not in lines:
        print(lines)
        task_start = 0
        task_end = 0
        for i in range(len(lines)):  # Определяем границы искомого куска кода по "ключевым" меткам '{% if' и '{% endif'
            if lines[i].startswith('{% if'):
                task_start = i
            elif lines[i].startswith('{% endif'):
                task_end = i
        lines[task_start:task_end+1] = if_str  # Заменяем ненужный кусок на актуальный код
    task_descrption.close()
    task_descrption = open(rf'{path}', mode='w', encoding='utf-8')
    task_descrption.write(''.join(lines))  # Заново открытый файл перетираем корректным кодом
    task_descrption.close()
    print(f'{path} - OK')



# Парсинг файла init.js
# Просто перетираем файл на новый код
init_js = open(f"{directory_name}\\{mission_name}\\editor\\animation\\init.js", 'w')
init_js.write('''requirejs(['ext_editor_io2', 'jquery_190'],
    function (extIO, $) {
        var io = new extIO({});
        io.start();
    }
);
''')
init_js.close()
print('\033init.js - OK')

# Парсинг файла python_3.tmpl
python_3_tmpl = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3.tmpl", 'w')
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
func_name = ''  # Название функции для вставки в код

for i in range(len(python_3_readLines)):
    if python_3_readLines[i].startswith('from') or python_3_readLines[i].startswith('import'):
        imp_str += python_3_readLines[i]  # Ищем по тексту импортированные библиотеки
    elif python_3_readLines[i].startswith('def'):
        a = i
        bracket = python_3_readLines[i].index('(')   # Начало initial кода функции
        func_name = python_3_readLines[i][4:bracket]
    elif python_3_readLines[i].startswith('if'):
        b = i  # Конец initial кода функции
    elif python_3_readLines[i].startswith('    assert'):
        c = i  # Начало кода в print(func(...))
        if '==' in python_3_readLines[i]:
            end = python_3_readLines[i][:python_3_readLines[i].index(' ==')]
            break
    elif '==' in python_3_readLines[i]:
        d = i  # Конец кода в print(func(...))
        end = python_3_readLines[i][:python_3_readLines[i].index(' ==')]  # Отрезать часть "ожидаемый" ответ
        break  # Примеров может быть много, чтобы забрать самый первый пример, мы выходим на данном моменте из цикла

func_str = ''.join(python_3_readLines[a:b])
example_str = ''.join(python_3_readLines[c:d])[11:]+end if d != 0 else ''.join(end)[11:]

# Текст заполняемый в новый файл
python_3_tmpl.write('''{% comment %}New initial code template{% endcomment %}
{% block env %}''' + imp_str[:-1] + '''{% endblock env %}

{% block start %}
''' + func_str +
"""{% endblock start %}

{% block example %}
print('Example:')
print(""" + example_str + ''')
{% endblock %}

{% block tests %}
{% for t in tests %}
assert {% block call %}''' + func_name + '''({{t.input|p_args}})
{% endblock %} == {% block result %}{{t.answer|p}}{% endblock %}{% endfor %}
{% endblock %}

{% block final %}
print("The mission is done! Click \'Check Solution\' to earn rewards!")
{% endblock final %}
''')

python_3_tmpl.close()
python_3.close()
print('python_3.tmpl - OK')


# Парсинг файла js_node.tmpl
js_node_tmpl = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\js_node.tmpl", 'w')
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
js_func_name = ''  # Название функции для вставки в код
js_ex = ''

for i in range(len(js_node_readLines)):
    if js_node_readLines[i].startswith('import'):
        if not js_node_readLines[i].startswith('import assert from "assert"'):
            js_imp_str += js_node_readLines[i]  # Ищем по тексту импортированные библиотеки
    elif js_node_readLines[i].startswith('function'):
        js_a = i
        js_bracket = js_node_readLines[i].index('(')   # Начало initial кода функции
        js_func_name = js_node_readLines[i][9:js_bracket]
    elif js_node_readLines[i].startswith("}"):
        js_b = i + 1  # Конец initial кода функции
    elif js_node_readLines[i].strip().startswith("assert"):  # Начало кода console.log(func(...))
        if js_count == 1:  # На втором кругу попадаем сюда, получаем конец первого примера и выходим из цикла
            js_d = i
            js_ex = ''.join(js_node_readLines[js_c:js_d])[js_node_readLines[i].find('ual(') + 4:]
            break
        js_c = i  # Начало кода из первого примера
        js_count += 1


js_func_str = ''.join(js_node_readLines[js_a:js_b])
# Так как со стройкой екзампла в джаве есть трудность (в большом количестве запятых еще до самого екзампла), реализовал обрезку функцией
js_example_str = example_cutter(js_ex) if js_d != 0 else example_cutter(''.join(js_node_readLines[js_c])[13:])

js_node_tmpl.write('''{% comment %}New initial code template{% endcomment %}
{% block env %}import assert from "assert";'''+ js_imp_str[:-1] +'''{% endblock env %}

{% block start %}
''' + js_func_str +
"""{% endblock start %}

{% block example %}
console.log('Example:');
console.log(""" + js_example_str +
'''{% endblock %}

// These "asserts" are used for self-checking
{% block tests %}
{% for t in tests %}
assert.strictEqual({% block call %}''' + js_func_name +
'''({{t.input|j_args}})
{% endblock %}, {% block result %}{{t.answer|j}}{% endblock %});{% endfor %}
{% endblock %}

{% block final %}
console.log("Coding complete? Click \'Check Solution\' to earn rewards!");\n{% endblock final %}''')

js_node_tmpl.close()
js_node.close()
print('js_node.tmpl - OK')


# Парсинг файла referee.py
# Имена функций мы уже получили в двух переменных выше "func_name" для пайтона и "js_func_name" для джавы
referee_py = open(f"{directory_name}\\{mission_name}\\verification\\referee.py", 'w')
referee_py.write('''from checkio.signals import ON_CONNECT
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
            "python":"''' + func_name + '''",
            "js": "''' + js_func_name + '''"
        },
        cover_code={
            'python-3': {},
            'js-node': {
                # "dateForZeros": True,
            }
        }
    ).on_ready)\n''')

referee_py.close()
print('referee.py - OK')


# Парсинг файла task_description.html
# Используем библиотеку "os" и находим все файлы таск-дискрипта. Используя функцию task_desc_change, изменяем эти файлы
walking = walk(f'{directory_name}\\{mission_name}')
path_info = ''
for i in walking:
    if 'task_description.html' in i[2]:  # Находим по директориям где есть нужный нам файл
        for u in i[2]:
            if u.startswith('task_description.html'):  # Берем нужный нам файл и крепим к директории
                path_info = i[0] + '\\' + u
                task_desc_change(path_info)  # Вызываем функцию передавая ей каждый раз новый путь для изменений


text_1 = walk(f'{directory_name}\\{mission_name}\\hints')
text_2 = open(f"{directory_name}\\{mission_name}\\hints\\{list(text_1)[0][2][0]}", 'r')
texts = text_2.read()
new_text = ''''''
trns = Translator()

for i in texts.split('\n'):
    if i.strip().startswith('<'):
        continue
    else:
        new_text += i + '\n'

text_2.close()
print('HINTS:\n', trns.translate(new_text, src='en', dest='uk').text)

task_desc_trns = open(f"{directory_name}\\{mission_name}\\info\\task_description.html", 'r')
task_2 = task_desc_trns.read()
new_text = ''''''

for i in task_2.split('\n'):
    if i.strip().startswith('<'):
        continue
    else:
        new_text += i + '\n'

task_desc_trns.close()
print('-'*200, '\nTASK:\n', trns.translate(new_text, src='en', dest='uk').text)
