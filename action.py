import pyperclip
import re
import pyautogui
import time
from random import randint


pyautogui.PAUSE = 0.15


first_window = (30, 15)
safe_place = (20, 150)
url_place = (300, 50)
leijipingjia = (685, 95)

next_page = (1265,500)
next_page2 = (1265,550)


def ppaste(astr):
    pyperclip.copy(astr)
    pyautogui.hotkey('ctrl', 'v')


def clickk(atuple):
    pyautogui.moveTo(atuple, duration=0.101,
                     tween=pyautogui.easeInQuad, pause=0.101)
    pyautogui.click(pause=0.101)


def input_url(the_url):
    clickk(first_window)
    clickk(url_place)
    pyautogui.hotkey('ctrl', 'a', pause=0.5)
    ppaste(the_url)
    pyautogui.hotkey('enter', pause=0.5)


def get_pagesource():
    clickk(safe_place)
    pyautogui.hotkey('ctrl', 'a', pause=0.25)
    pyautogui.hotkey('ctrl', 'c', pause=0.15)
    pagesource = pyperclip.paste()
    clickk(safe_place)
    return pagesource


def change_searchwords(searchwords):
    pyautogui.hotkey('ctrl', 'f')
    ppaste(searchwords)
    pyautogui.press('enter')
    pyautogui.press('esc')
    pyautogui.click(first_window, duration=1)


def find_name():
    pyautogui.hotkey('ctrl', 'u', pause=0.5)
    pyautogui.hotkey('ctrl', 'a', pause=0.5)
    pyautogui.hotkey('ctrl', 'c', pause=0.5)
    sour = pyperclip.paste()
    pyautogui.hotkey('ctrl', 'w', pause=0.5)
    res_sou = re.findall(
        r'<meta name="keywords" content=".*?"/>', sour, flags=re.DOTALL)[0][31:-3]
    return res_sou


def get_in_leijipingjia():
    for m in range(5):
        pyautogui.press('pagedown')
    pyautogui.click(leijipingjia, duration=0.5)


def find_nextpage():
    pyautogui.hotkey('ctrl', 'f', pause=0.15)
    pyautogui.press('enter', pause=0.15)
    pyautogui.press('esc', pause=0.15)
