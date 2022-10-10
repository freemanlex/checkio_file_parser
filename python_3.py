import referee





def next_api(directory_name: str, mission_name: str, py_iterable: bool) -> None:

    func_name, _ = referee.extract_func_names(directory_name, mission_name)

    with open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3", 'r') as python_3:
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
                d = ind
                break
        elif '==' in line and ind > c > 0:
            d = ind  # Конец кода в print(func(...))
            break

    func_str = ''.join(python_3_readLines[a: b + 1])
    example_str = ''.join(python_3_readLines[c: d + 1])
    example_str = example_str.rpartition("==")[0].strip()[7:]
    # Текст заполняемый в новый файл
    with open(f"{directory_name}\\{mission_name}\\editor\\initial_code\\python_3.tmpl", 'w') as python_3_tmpl:
       
        python_3_tmpl.write(
'''{% comment %}New initial code template{% endcomment %}
{% block env %}''' + imp_str + '''{% endblock env %}

{% block start %}
''' + func_str +
'''{% endblock start %}

{% block example %}''')

        if func_str:
            python_3_tmpl.write('''
print('Example:')
print(''' + 'list('*py_iterable + example_str + ')'*py_iterable + ''')''')

        python_3_tmpl.write('''
{% endblock %}

{% block tests %}
{% for t in tests %}
assert {% block call %}''' + 'list('*py_iterable + func_name  + '''({{t.input|p_args}})''' + ')'*py_iterable + '''{% endblock %} == {% block result %}{{t.answer|p}}{% endblock %}{% endfor %}
{% endblock %}

{% block final %}
print("The mission is done! Click \'Check Solution\' to earn rewards!")
{% endblock final %}''')
    
    print("\\editor\\initial_code\\python_3.tmpl - OK")