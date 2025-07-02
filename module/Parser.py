import requests, os, csv, json
from bs4 import BeautifulSoup
from SinCity.Agent.header import header
from module.colors import RED, RESET, YELLOW
from module.miniTools import CurrentDataJson
from manifest import status_done, variation_page

    
#######################################
# : Скрапер имейлов
#######################################
def MainEmail(response, url:str):
    email_list = []
    contact_page_list = []
    contact_page = None

    bs = BeautifulSoup(response.text, 'lxml')
    htmlEmail = ExtractEmail(bs, url=url)
    if htmlEmail != None:
        print(htmlEmail)
        for email in htmlEmail:
            if email not in email_list:email_list.append(email)
    for email in bs.find_all('a'):
        try:
            if 'mailto' in email['href']:
                email = email['href'].split('mailto:')[1]
                if '?' in email:email = email.split('?')[0]
                if email not in email_list and '@' in email:email_list+=[email]
            else:
                for variation in variation_page:
                    if variation in email['href']:
                        if email['href'] not in contact_page_list and '#' not in email['href']:
                            contact_page_list+=[email['href']]


        except:pass
        
        if len(contact_page_list) != 0 and len(email_list) == 0:
            number_contact_page = 0
            for contact in contact_page_list:
                domain = url.split('//')[1]
                if domain in contact:contact_page = contact
                else:contact_page = f'{url}/{contact}'
                break

    return email_list, contact_page
#######################################
# End: Скрапер имейлов
#######################################

def ExtractEmail(bs, url:str):
    email_list = []
    for block in bs.find_all(['p', 'span']):
        block = block.text
        if '@' in block:
            email = block.strip()
            if ' ' in email:email = email.replace(' ', '\n')
            if '\n' in email:email = email.split('\n')[1]
            if ': ' in email:email = email.split(': ')[1]
            if '\xa0' in email:email = email.split('\xa0')[1]
            if '@' in email:
                if email not in email_list:email_list.append(email)
    if len(email_list) == 0:email_list = None
    return email_list
    

#######################################
# : Начало скрапера
#######################################
def scrape(site:str, path_file:str):
    head = header()
    try:
        response = requests.get(site, headers=head)
    
        status = response.status_code
        if status == 200:
            email, contact_pages = MainEmail(response, url=site)
            return email, contact_pages
        else:
            print(f'{YELLOW}Site: {site}\tStatus Code: {status}{RESET}\n')
            
            data = CurrentDataJson(path_file=path_file)
            data['status'] = status_done
            data['status_code'] = status
            data['email'] = None
            with open(path_file, 'w') as file:
                json.dump(data, file, indent=4)

    except requests.exceptions.ConnectionError:
        print(f"{RED}Site {site} doesn't exist{RESET}\n")

        data = CurrentDataJson(path_file=path_file)
        data['status'] = status_done
        data['email'] = None
        with open(path_file, 'w') as file:
            json.dump(data, file, indent=4)

