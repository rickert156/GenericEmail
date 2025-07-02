import time

def Scrolling(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    number_scrolling = 0
    while True:
        number_scrolling+=1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height or number_scrolling == 5:
            break  
        last_height = new_height
