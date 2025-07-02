import socket
# Машина, с которой парсится база

machine = socket.gethostname()
base_name = 'TrustPilot'

# Директория для хранения информации о доменах
domains_dir = 'Domains'

# Директория с исходной базой с доменами, именами компаний, категориями
source_dir = 'Source'
done_dir = 'Done'
status_processing = 'Processing...'
status_done = 'Complite'

resultDir = 'Result'
resultFile = f'GenericEmails_{base_name}_{machine}.csv'
resultNoEmail = f'NoEmails_{base_name}_{machine}.csv'

resultPath = f'{resultDir}/{resultFile}'
resultNoEmailPath = f'{resultDir}/{resultNoEmail}'


variation_page = [
        'contact',
        'contact-us',
        'contactus',
        'letstalk',
        'lets-talk',
        'kontakt',
        'contacto',
        'connect',
        'about'
        ]
