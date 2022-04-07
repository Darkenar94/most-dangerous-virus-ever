
import time,os
import pyautogui

def get_path():
    path = os.path.join(os.path.expanduser("~"), "AppData")
    if not os.path.exists(path):
        return os.path.expanduser("~") + r"\OneDrive\AppData"
    return path

def get_folder_path(text):
    return text.split("\n")[0:-1][-1]

def read_file(file_path):
    file = open(file_path, "r")
    text = file.read()
    file.close()
    return get_folder_path(text)

def menage_screenshots(i, zero_min, five_min, folder_path):
    if time.localtime().tm_sec == 0:
        try:
            if str(time.localtime().tm_min)[i] == "0" and zero_min == True:
                save_screenshot(folder_path)
                return False, True
            elif str(time.localtime().tm_min)[i] == "5" and five_min == True:
                save_screenshot(folder_path)
                return True, False
        except:
            pass
    return zero_min, five_min

def save_screenshot(folder_path):
    screenshot = pyautogui.screenshot()
    screenshot_file = os.path.join(folder_path, "S" + os.path.split(folder_path)[1] + ".dcx")
    screenshot_number = int(os.path.split(screenshot_file)[1][1:-4])
    screenshot_name = "S" + str(screenshot_number) + ".dcx"
    while os.path.exists(screenshot_file):
        screenshot_number += 1 
        screenshot_name = "S" + str(screenshot_number) + ".dcx" 
        screenshot_file = os.path.join(folder_path, screenshot_name) 
    screenshot_file = os.path.join(folder_path, screenshot_name[0:-4] + ".png")
    screenshot.save(screenshot_file) 
    os.rename(screenshot_file, screenshot_file[0:-4] + ".dcx") 

time.sleep(1200)#20min.

path = get_path()
file_path = os.path.join(path, "98349098023490.dcx")
folder_path = read_file(file_path)

zero_min, five_min = True, True

while True:
    if not time.localtime().tm_min == 60:
        if len(str(time.localtime().tm_min)) == 1:
            zero_min, five_min = menage_screenshots(0, zero_min, five_min, folder_path)
        elif len(str(time.localtime().tm_min)) == 2:
            zero_min, five_min = menage_screenshots(1, zero_min, five_min, folder_path)
