import referee


# Функция для обрезки экзампла в файле js_node.tmpl
def example_cutter(exmpl):  

    s = ""
    for char in exmpl:
        if char in "[{()}]":
            s += char
            if s[-2:] in ("[]", "()", "{}"):
                s = s[:-2]
        elif char == ",":
            exmpl = exmpl.replace(',', ('.', '*')[not s], 1)
    
    return exmpl.split("*", 1)[0]


def next_api(directory_name, mission_name):

    _, js_func_name = referee.extract_func_names(directory_name, mission_name)

    js_node = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\js_node", 'r')
    js_node_readLines = js_node.readlines()

    js_imp_str = ''  # импортируемые библиотеки
    js_func_str = ''  # initial код функции
    js_a = 0
    js_b = 0  # Markers for 'def' search
    js_example_str = ''  # Строка, в которой будет храниться код console.log(func(...))
    js_count = False  # Переменная для поимки первого примера
    js_c = 0
    js_d = 0  # Markers for 'assert' search

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
            if js_count:  # На втором кругу попадаем сюда, получаем конец первого примера и выходим из цикла
                js_ex = ''.join(js_node_readLines[js_c: (js_c + 1, ind)[bool(ind)]])
                break
            js_c = ind  # Начало кода из первого примера
            js_count = True

    
    js_func_str = ''.join(js_node_readLines[js_a: js_b])
    # Так как со стройкой екзампла в джаве есть трудность (в большом количестве запятых еще до самого екзампла), реализовал обрезку функцией
    js_example_str = example_cutter(js_ex[line.find('ual(')+4:])

    js_node_tmpl = open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\js_node.tmpl", 'w')
    js_node_tmpl.write(
'''{% comment %}New initial code template{% endcomment %}
{% block env %}import assert from "assert";'''+ js_imp_str[ : -1] +'''{% endblock env %}

{% block start %}
''' + js_func_str +
'''{% endblock start %}

{% block example %}''')
    if js_func_str:
        js_node_tmpl.write('''
console.log('Example:');
console.log(''' + js_example_str + ''';''')
    js_node_tmpl.write('''
{% endblock %}

// These "asserts" are used for self-checking
{% block tests %}
{% for t in tests %}
assert.strictEqual({% block call %}''' + js_func_name + '''({{t.input|j_args}}){% endblock %}, {% block result %}{{t.answer|j}}{% endblock %});{% endfor %}
{% endblock %}

{% block final %}
console.log("Coding complete? Click \'Check Solution\' to earn rewards!");
{% endblock final %}''')

    js_node_tmpl.close()
    js_node.close()
    
    print("\\editor\\initial_code\\js_node.tmpl - OK")