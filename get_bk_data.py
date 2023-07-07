import pyautogui
import time
import subprocess

def get_data(name):
    # Start Quicken
    process = subprocess.Popen(r'C:\Program Files (x86)\Quicken\qw.exe')
    # quicken_path = r'C:\Program Files (x86)\Quicken\Quicken.exe'
    # process = subprocess.Popen([quicken_path])
    # process = subprocess.Popen('C:\\Users\\12158\\Downloads\\REIFAST CONSTRUCTION.QDF')

    # Wait for Quicken to open
    time.sleep(5)

    # Simulate keystrokes to navigate and perform tasks in Quicken
    pyautogui.hotkey('alt', 'f')
    pyautogui.press('down', 10)
    pyautogui.press('right')
    pyautogui.press('enter')
    pyautogui.typewrite('C:\\Users\\12158\\Desktop\\BSA_APP\\forms\\' + name + '.QIF')
    pyautogui.press('tab', 3)
    pyautogui.typewrite('1')
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

