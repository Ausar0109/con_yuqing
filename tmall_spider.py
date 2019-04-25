from .action import *
import time
import re
import pandas as pd


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
    pinglun = pinglun[pinglun.map(lambda x: False if '下一页' in x else True)]
    pinglun = pinglun[pinglun.map(lambda x: False if '查看更多的' in x else True)]
    return pinglun


class Tmall_Spider():

    def __init__(self):
        self._pagesource = None
        self.skuname = None
        self.countnum = None
        self.res = pd.Series()

    def get(self, the_url):
        input_url(the_url)
        time.sleep(0.5)

    @property
    def pagesource(self):
        self._pagesource = get_pagesource()
        return self._pagesource

    def run_task(self, task_url):
        self.get(task_url)
        self.skuname = find_name()
        self.countnum = int(re.findall(
            '累计评价 [0-9].*', self.pagesource)[0][5:-1])
        self.countnum = 99 if self.countnum // 20 > 100 else self.countnum // 20

        get_in_leijipingjia()
        change_searchwords('下一页')

        for i in range(self.countnum):
            pagesource = self.pagesource  # 调用self.pagesource 时 ，返回pagesource，并带有动作
            _df = find_from_source(pagesource)
            self.res = pd.concat([self.res, _df])

            if '为什么被折叠' in pagesource:
                break

            find_nextpage()
            if i < 3:
                clickk(next_page)
                clickk(next_page2)
            else:
            	clickk(next_page2)
            time.sleep(randint(10, 20) / 30)
