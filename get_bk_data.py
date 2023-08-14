import pyautogui
import time
import subprocess
import os

def get_data(path, cmp_name):
    # Replace forward slashes with backslashes in the path
    f_path = path.replace('/', '\\')
    
    # Create the new folder path
    new_folder = 'C:\\Users\\12158\\Desktop\\Reports\\' + cmp_name + ' 2022\\'
    
    # Check if the new folder already exists, and create it if it doesn't
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    
    # Construct the path to the QIF file within the new folder
    qif_path = os.path.join(new_folder, cmp_name + '.QIF')

    # Start Quicken
    process = subprocess.Popen(r'C:\Program Files (x86)\Quicken\qw.exe')

    # Wait for Quicken to open
    time.sleep(5)

    # Open selected company's QDF
    pyautogui.hotkey('ctrl', 'o')
    pyautogui.typewrite(f_path)
    pyautogui.press('enter')

    # Generate QIF from open QDF file
    pyautogui.hotkey('alt', 'f')
    pyautogui.press('down', 10)
    pyautogui.press('right')
    pyautogui.press('enter')
    pyautogui.typewrite(qif_path)
    pyautogui.press('tab', 3)
    pyautogui.typewrite('1')
    pyautogui.press('right')
    pyautogui.typewrite('01')
    pyautogui.press('right')
    pyautogui.typewrite('2022')
    pyautogui.press('tab')
    pyautogui.typewrite('12')
    pyautogui.press('right')
    pyautogui.typewrite('31')
    pyautogui.press('right')
    pyautogui.typewrite('2022')
    pyautogui.press('tab', 8)
    pyautogui.press('enter')
    pyautogui.press('enter')

    process.terminate()
    return qif_path


