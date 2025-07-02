# Generic email parser

## Первый запуск парсера
Установка окружения + зависемостей
```sh
git clone https://github.com/rickert156/GenericEmail
```
```sh
cd GenericEmail
```
```sh
python3 -m venv venv
```
```sh
source venv/bin/activate
```
```sh
pip install -r package.txt
```
Запускаем первый раз
```sh
python3 -m module.createBaseDomain
```
Будет создана директория Source, если ее не было. В нее нужно будет добавить документ .csv, колонки, которые могут(должны быть) в таблице   
|Domain |Company|

Можно добавить колонки Category, Location   
После этого можно еще раз ввести команду для создания базы доменов
```sh
python3 -m module.createBaseDomain
```
В директории Domains будут json документы для каждого домена

## Отправка результатов
По завершению сбора рельтат будет отправлен на почту. Для этого нужно добавить почтовый конфиг module/mail_config.py
```sh
sender = ''
password = ''
smtp_server_info = ''
recipient = ''
```

## Разбивка баз на несколько
Для разделения баз(к примеру, для распределения по контейнерам) можно использовать модуль module.divideBase, обязательно передав параметром количество баз, которое должно получиться
```sh
python3 -m module.divideBase
```
