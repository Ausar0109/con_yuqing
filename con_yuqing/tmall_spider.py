from .action import *
import time
import re
import pandas as pd
from jieba.analyse import textrank


def find_from_source(asource):
    asource = asource.replace('\r\n', '')
    pinglun1 = pd.Series(re.findall(
        r'有内容按默.{10,10000}?（匿', asource, flags=re.DOTALL))
    pinglun1 = pinglun1.map(lambda x: x[6:])
    pinglun2 = pd.Series(re.findall(
        r'名）.{10,10000}?（匿', asource, flags=re.DOTALL))
    pinglun = pd.concat([pinglun1, pinglun2])

    pinglun = pinglun.str.replace('.{5,5}解释：.*', '')
    pinglun = pinglun.str.replace('.*此用户没有填写评论!', '')
    pinglun = pinglun.str.replace('收货.*天后追加：', '。')
    pinglun = pinglun.str.replace('超级会员|名）|.{5,5}（匿', '')

    pinglun = pinglun.str.replace('颜色分类：.*', '')
    pinglun = pinglun.str.replace('组合套餐：.*', '')
    pinglun = pinglun.str.replace('尺码：.*', '')

    return pinglun


class Tmall_Spider():

    def __init__(self):
        self._pagesource = None
        self.skuname = None
        self.filepath = "C:\\Users\\cheng.lu\\Desktop\\task_data\\"

    def get(self, the_url):
        input_url(the_url)  # 每次调用，先进入第一窗口

    @property
    def pagesource(self):
        '''获得当前页面的页面内容，实际上只有复制-粘贴操作，需要保证进入了目标页面'''
        self._pagesource = get_pagesource()
        return self._pagesource

    def dowith_yanzheng(self):
        pyautogui.click((957, 591), duration=1, pause=2)

        clickk((820, 590))
        pyautogui.dragTo((1120, 595), tween=pyautogui.easeInBack, duration=2)
        time.sleep(5)

        get_in_leijipingjia()

    def run_task(self, task_url):
        self.res = pd.Series([task_url, ])
        self.get(task_url)
        self.skuname = find_name()

        get_in_leijipingjia()  # 进入累计评价的子 iframe
        change_searchwords('下一页')  # 更改了搜索词为 ’下一页‘  回到第一窗口

        countnum = 0
        clickk(first_window)
        
        while True:
            pagesource = self.pagesource  # 调用self.pagesource 时 ，返回pagesource，并带有动作

            if '访问验证' in pagesource:
                self.dowith_yanzheng()
                pagesource = self.pagesource

            _df = find_from_source(pagesource)
            self.res = pd.concat([self.res, _df])

            if 1 <= len(_df) < 20:
                break
            elif len(_df) == 0:
                self.get(task_url)
                get_in_leijipingjia()

            if '为什么被折叠' in pagesource:
                break

            if countnum > 200:
                break

            find_nextpage()

            if countnum % 11 == 0 or countnum == 0:
                clickk(next_page)
            clickk(next_page2)

            countnum += 1

        rizhipath = self.filepath + self.skuname + '.xlsx'
        pd.DataFrame([]).to_excel(rizhipath)

        excelWriter = pd.ExcelWriter(rizhipath)

        self.res.drop_duplicates(inplace=True)
        self.res.to_excel(excelWriter, index=False,
                          encoding='gb18030', sheet_name='源数据', header=None)

        gjc = []
        for x in self.res.map(textrank):
            for y in x:
                gjc.append(y)
        pd.Series(gjc).value_counts().to_excel(excelWriter, sheet_name='源数据词频')

        excelWriter.save()
        excelWriter.close()
