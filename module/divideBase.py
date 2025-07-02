import os, sys, shutil
from module.manifest import domains_dir

def ListJson():
    list_json = []
    for doc in os.listdir(domains_dir):
        if '.json' in doc:list_json.append(f'{domains_dir}/{doc}')

    return list_json

def divide(count:int):
    list_json = ListJson()
    
    number_doc = 0
    global_count = 0

    for doc in list_json:
        number_doc+=1
        global_count+=1
        dir_name = f"{domains_dir}/base_{number_doc}"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        new_doc = doc.split('/')[1]
        shutil.move(doc, f"{dir_name}/{new_doc}")
        print(f"[{global_count}] {doc} -> {dir_name}/{new_doc}")
        if number_doc == count:number_doc = 0

def DivideBase():
    params = sys.argv
    if len(params) > 1:
        try:
            count = int(params[1])
            divide(count=count)
        except Exception as err:
            print(f'Проверь правильность вводимого параметра!\n{err}')
            sys.exit()
    else:
        print(f'Добавь количество директорий, по которым будет распределна база!')

DivideBase()
