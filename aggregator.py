'''
Next-API converter for CheckiO missions
'''
import os
import init_js, referee, tests, python_3, js_node, task_description
# from googletrans import Translator

# Directory path
directory_name = 'C:\\Users\\ТЕХНОРАЙ\\Documents\\GitHub'
# Mission name
mission_name = 'checkio-mission-acceptable-password-5'  

# Converting init.js
init_js.next_api(directory_name, mission_name)

# Create and fill python_3.tmpl
python_3.next_api(directory_name, mission_name)

# Create and fill js_node.tmpl
js_node.next_api(directory_name, mission_name)

# Converting task_description files
task_description.next_api(directory_name, mission_name)

# Converting referee.py
referee.next_api(directory_name, mission_name)

# Converting tests.py
tests.next_api(directory_name, mission_name)

# old init files deleting
for file in ("js_node", "python_3", "python_27"):
    try:
        os.remove(f"{directory_name}\\{mission_name}\\editor\\initial_code\\" + file)
    except:
        pass

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
