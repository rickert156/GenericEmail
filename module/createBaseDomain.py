import json, os, csv
from module.manifest import domains_dir, source_dir, status_processing
from module.colors import RED, RESET, YELLOW, GREEN

#######################################
# : Функция инициализации обработки баз
#######################################
def initProcessing():
    value_init = False
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(
                f'{RED}Create dir {source_dir}\n{RESET}'
                f'{YELLOW}Please, add source base{RESET}'
                )
    else:
        count_base = 0
        for base in os.listdir(source_dir):
            if '.csv' in base:count_base+=1

        if count_base != 0:value_init = True
        else:print(f'{YELLOW}Add a base!{RESET}')
    
    if not os.path.exists(domains_dir):os.makedirs(domains_dir)

    return value_init
#######################################
# End: Конец функции инициализации
#######################################


#######################################
# : Основная функция скрипта
#######################################
def GenerateJSON():
    status_init = initProcessing()
    if status_init:
        # Получаем полный список исходных баз
        list_base = ListBase()
        for base in list_base:
            ExtractInfo(base_name=base)
    else:print(f'{RED}Иницилизация прошла неуспешно!{RESET}')

#######################################
# End: Конец основной функции
#######################################


#######################################
# : Набор небольших функций
#######################################
# Ищем базы csv с колонками Company, Domain
def ListBase():
    list_base = []
    for base in os.listdir(source_dir):
        if '.csv' in base:
            base = f'{source_dir}/{base}'
            with open(base, 'r') as file:
                headers = csv.DictReader(file).fieldnames
                try:
                    if 'Domain' in headers and 'Company' in headers:list_base.append(base)
                except TypeError:print('Заголовки отсутствуют')
    return list_base

def RecordingDomain(domain:str, company:str, location:str, category:str):
    domainJson = f'{domain}.json'
    path_domain_json = f'{domains_dir}/{domainJson}'
    site = f'https://{domain}'

    data = {
        "domain":domain,
        "site":site,
        "email":[],
        "company":company,
        "location":location,
        "category":category,
        "status":status_processing
            }

    with open(path_domain_json, 'w') as file:
        json.dump(data, file, indent=4)


# Собираем инфу с колонок базы
def ExtractInfo(base_name:str):
    with open(base_name, 'r') as file:
        count_domain = 0
        for row in csv.DictReader(file):
            count_domain+=1
            domain = row['Domain']
            company = row['Company']

            try:location = row['Location']
            except:location = None
            
            try:category = row['Category']
            except:category = None
            
            print(f'Number: [{count_domain}]\n'
                  f'Company Name: {company}\n'
                  f'Domain: {domain}\n'
                  f'Location: {location}\n'
                  f'Category: {category}\n'
                  )
            RecordingDomain(domain=domain, company=company, location=location, category=category)


#######################################
# End: Набор небольших функций
#######################################
try:
    GenerateJSON()
except KeyboardInterrupt:print(f'\n{GREEN}Exit...{RESET}')
