import pyautogui
import time

# Open Quicken
pyautogui.hotkey('win', 's')
pyautogui.write('Quicken')
pyautogui.press('enter')
time.sleep(5)

# Navigate to File menu
pyautogui.hotkey('alt', 'f')
