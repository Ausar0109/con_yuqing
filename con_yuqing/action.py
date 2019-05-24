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

next_page = (1265, 500)
next_page2 = (1265, 540)


class CantFindNameError(Exception):

    def __init__(self, *args):
        self.args = args


def ppaste(astr):
    pyperclip.copy(astr)
    pyautogui.hotkey('ctrl', 'v')


def clickk(atuple):
    pyautogui.moveTo(atuple, duration=0.2,
                     tween=pyautogui.easeInQuad, pause=0.101)
    pyautogui.click(pause=0.101)


def input_url(the_url):
    clickk(first_window)
    pyautogui.press('f5')
    time.sleep(2)
    clickk(url_place)
    pyautogui.hotkey('ctrl', 'a', pause=1)
    ppaste(the_url)
    time.sleep(1)
    pyautogui.press('enter', pause=1)
    pyautogui.press('f5')
    time.sleep(2)


def get_pagesource():
    clickk(first_window)
    pyautogui.hotkey('ctrl', 'a', pause=0.3)
    pyautogui.hotkey('ctrl', 'c', pause=0.3)
    pagesource = pyperclip.paste()
    time.sleep(0.3)
    return pagesource


def change_searchwords(searchwords):
    pyautogui.hotkey('ctrl', 'f', pause=0.5)
    ppaste(searchwords)
    pyautogui.press('enter')
    pyautogui.press('esc')
    pyautogui.click(first_window, duration=0.5)


def find_name():
    pyautogui.hotkey('ctrl', 'u', pause=0.25)
    pyautogui.hotkey('ctrl', 'a', pause=0.25)
    pyautogui.hotkey('ctrl', 'c', pause=0.25)
    sour = pyperclip.paste()
    time.sleep(0.5)

    if '您查看的页面找不到了' in sour:
        pyautogui.hotkey('ctrl', 'w', pause=0.4)
        raise CantFindNameError

    if '您查看的商品找不到了' in sour:
        pyautogui.hotkey('ctrl', 'w', pause=0.4)
        raise CantFindNameError

    pyautogui.hotkey('ctrl', 'w', pause=0.4)
    res_sou = re.findall(
        r'<meta name="keywords" content=".*?"/>', sour, flags=re.DOTALL)[0][31:-3]

    for i in [x for x in '|><": ?!*+/.,']:
        res_sou = res_sou.replace(i, '')
    res_sou = res_sou.replace('\\', '')
    res_sou = res_sou.replace("'", '')
    return res_sou


def find_nextpage():
    pyautogui.hotkey('ctrl', 'f', pause=0.25)
    pyautogui.press('enter', pause=0.11)
    pyautogui.press('esc', pause=0.11)


def find_pic_andclick(pic_name):
    time.sleep(2)
    try:
        findres = pyautogui.locateCenterOnScreen(
            'C:\\Users\\cheng.lu\\Desktop\\' + pic_name + '.PNG', grayscale=True)
        print('Log--YuQing :::   发现 %s' % pic_name)
        clickk(findres)
        time.sleep(1)  # 如果发现了，休息2秒
    except:
        print('Log--YuQing ::: 未发现 %s' % pic_name)
        pass


def get_in_leijipingjia():
    for m in range(4):
        pyautogui.press('pagedown', pause=0.2)
    find_pic_andclick('leijipingjia')
    find_pic_andclick('red-leijipingjia')


def keep_Onewindow():
    clickk(first_window)
    pyautogui.click(button='right', pause=0.5)
    clickk((175, 195))
    pyautogui.hotkey('esc')
