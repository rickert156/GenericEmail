import os, json, shutil, time, sys, subprocess
"""Мои модули"""
import __init__
from module.driver_chrome import driver_chrome
from module.colors import RED, RESET, BLUE, GREEN
from module.miniTools import CurrentDataJson, RecordingCSV, RecordingCSVnoEmail, createDirs
from module.scrolling import Scrolling
from module.report import Report
from module.manifest import domains_dir, done_dir, variation_page, resultDir

"""Сторонние модули"""
from bs4 import BeautifulSoup

def Greeting():
    text = (
    f"{GREEN}| Generic email parser\n\n"
    f"| Version:\t{__init__.__version__}\n"
    f"| Author:\t{__init__.__author__}\n{RESET}"
    )
    return text


def ListJson():
    list_json = []
    for file in os.listdir(domains_dir):
        if '.json' in file:
            file=f"{domains_dir}/{file}"
            list_json.append(file)

    return list_json

def GetGeneric():
    createDirs()
    try:
        print(Greeting())
        divide = "-"*60


        list_json = ListJson()
        """Перебираем все JSON файлы"""

        number_site = 0
        for doc in list_json:
                
            driver = driver_chrome()
                
            number_site+=1
            """Получаем данные из JSON"""
            print(doc)
            data = CurrentDataJson(path_file=doc)
        
            site = data['site']
    
            complite_json = doc.replace(domains_dir, done_dir)
            
            print(f"[{number_site}] {site}")
            try:
                driver.get(site)
            
                Scrolling(driver=driver) 
                ParserPage(
                        driver=driver, 
                        data=data, #Передаем словарь с инфой(что бы не вызывать повторно)
                        file_json=doc #Передаем док
                        )
    
                print(f"{BLUE}{doc} -> {complite_json}{RESET}\n{divide}\n")
            finally:  
                shutil.move(doc, complite_json)
                driver.quit()

    except KeyboardInterrupt:
        print(f"{RED}\nExit...{RESET}")
        sys.exit()
    except:
        if os.path.exists(doc):
            shutil.move(doc, complite_json)


#######################################
#           Функции парсера          #
#######################################
def getLinks(bs:str):
    list_url = set()
    try:
        for link in bs.find_all('a'):
            try:
                link = link.attrs['href']
                if link:list_url.add(link)
            except:
                pass
    except Exception as err:
        """
        В дальнейшем можно просто заглушить ошкибку, 
        так как в основном ошибки из-за отсутствия href у ссылок.
        Поведение ожидаемое, и только на время отладки будет
        выводиться инфа
        """
        pass
        #print(f"ERROR: {err}")
    finally:
        return list_url

def getLinkEmail(bs:str):
    list_email = set()
    try:
        for link in bs.find_all('a'):
            try:
                link = link.attrs['href']
                if 'mailto:' in link and '@' in link:
                    link = link.split("mailto:")[1]
                    list_email.add(link)
            except Exception as err:
                pass
                #print(f"{RED}ERROR: {err}{RESET}")
    finally:
        return list_email

def getTextEmail(bs:str):
    list_email = set()
    list_tags= ['a', 'div', 'p', 'span', 'li', 'header', 'footer', 'ld', 'br']
    try:
        for tag in list_tags:
            for block in bs.find_all(tag):
                text = block.get_text(separator=' ', strip=True) 
                list_text = text.split()
                for word in list_text:
                    if '@' in word:
                        word = word.strip('.,;:()[]<>|')
                        email = word.split("@")
                        try:
                            if len(email) == 2:
                                name, domain = word.split("@")
                                if len(name) > 0 and '.' in domain and len(domain) >= 5:
                                    list_email.add(word)
                        except:
                            pass
    finally:
        return list_email

def ParserPage(driver:str, data:dict, file_json:str):

    """Извлечем значения из JSON"""
    domain = data['domain']
    company = data['company']
    location = data['location']
    category = data['category']

    page_source = driver.page_source
    bs = BeautifulSoup(page_source, 'lxml')

    """Ищем все ссылки на странице"""
    list_url = getLinks(bs=bs)
    
    """Ищем имейлы в ссылках"""
    links_email = getLinkEmail(bs=bs)
    #if len(links_email) != 0:print(f"Link: {links_email}")

    """Ищем имейлы в тексте"""
    texts_email = getTextEmail(bs=bs)
    #if len(texts_email):print(f"Text: {texts_email}")
    
    """Список URL на страницы контактов"""
    contacts_url = []

    """Сливаем множества в одно"""
    list_email = links_email.union(texts_email)
    """
    Тут пока что не надо, наверное, выводить инфу,
    так как в любом случае должна выводиться ниже
    if len(list_email) != 0:print(f"{GREEN}{list_email}{RESET}")
    """
    if len(list_email) == 0:
        site = data['site']
        if len(list_url) != 0:
            for page in variation_page:
                for url in list_url:
                    if page in url:
                        if 'http' not in url and '//' not in url:
                            url = f"{site}{url}"
                        if url not in contacts_url:contacts_url.append(url)
    
    if len(list_email) == 0 and len(contacts_url) != None:
        for url in contacts_url:
            print(f"{BLUE}Contact Page: {url}{RESET}")
            driver.get(url)
            new_page_source = driver.page_source
            bs = BeautifulSoup(new_page_source, 'lxml')
            new_texts_email = getTextEmail(bs=bs)
            new_links_email = getLinkEmail(bs=bs)
            if len(new_texts_email) != 0:
                for email in new_texts_email:
                    list_email.add(email)
            if len(new_links_email) != 0:
                for email in new_links_email:
                    list_email.add(email)
        
    if len(list_email) != 0:
        number_email = 0
        for email in list_email:
            number_email+=1
            print(f"{GREEN}[{number_email}] {email}{RESET}")
            RecordingCSV(
                    company=company, 
                    email=email, 
                    domain=domain, 
                    category=category, 
                    location=location
                    )
        
        data['email'] = list(list_email)
        with open(file_json, 'w') as file:
            json.dump(data, file, indent=4)

    if len(list_email) == 0:
        print(f"{RED}На сайте не обнаружена имейлов{RESET}")
        RecordingCSVnoEmail(
                company=company,
                domain=domain,
                category=category,
                location=location
                )

def run_command(command:str):
    print(command)
    subprocess.run(command, shell=True)

while True:
    try:
        if len(os.listdir(domains_dir)) > 0:
            GetGeneric()
        else:
            print(f"{GREEN}Parsing Complited!{RESET}")
            Report()
            sys.exit()
    except Exception as err:
        print(f'{RED}MAIN BLOCK ERROR: {err}{RESET}')
        cancel_python3 = "killall python3"
        cancel_chromium = "killall chromium"
