import os, socket, smtplib, mimetypes, time
from email.message import EmailMessage
from module.manifest import resultDir
from module.mail_config import recipient, sender, password, smtp_server_info


def ListBase():
    list_base = []
    for base in os.listdir(resultDir):
        if '.csv' in base:
            base = f"{resultDir}/{base}"
            list_base.append(base)

    return list_base

def Report():
    machine = socket.gethostname()
    current_date = time.strftime("%d/%m/%y")
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient 
    msg['Subject'] = f'Report {machine} - {current_date}'

    for base in ListBase():
        with open(base, 'rb') as file:
            file_data = file.read()
            file_type, _ = mimetypes.guess_type(base)
            if file_type is None:
                file_type = 'application/octet-stream'
            msg.add_attachment(
                    file_data, 
                    maintype=file_type.split('/')[0], 
                    subtype=file_type.split('/')[1],
                    filename=base
                    )
    try:
        with smtplib.SMTP_SSL(smtp_server_info, 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f'База отправлена!\n{ListBase()}')
    except Exception as err:print(err)

