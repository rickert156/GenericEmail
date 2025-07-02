import json, os, csv
from module.manifest import resultPath, resultNoEmailPath, done_dir, resultDir

def CurrentDataJson(path_file:str):
    with open(path_file, 'r') as file:
        data = json.load(file)
    return data

def RecordingCSV(company:str, email:str, domain:str, category:str, location:str):
    if not os.path.exists(resultPath):
        with open(resultPath, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Company', 'Email', 'Domain', 'Location', 'Category'])

    with open(resultPath, 'a+') as file:
        write = csv.writer(file)
        write.writerow([company, email, domain, location, category])

def RecordingCSVnoEmail(company:str, domain:str, category:str, location:str):
    if not os.path.exists(resultNoEmailPath):
        with open(resultNoEmailPath, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Company', 'Domain', 'Location', 'Category'])
    
    with open(resultNoEmailPath, 'a+') as file:
        write = csv.writer(file)
        write.writerow([company, domain, location, category])


def createDirs():
    if not os.path.exists(done_dir):os.makedirs(done_dir)
    if not os.path.exists(resultDir):os.makedirs(resultDir)

