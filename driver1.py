from con_yuqing import Tmall_Spider
from con_yuqing import yq_task
from con_yuqing import CantFindNameError
from con_yuqing import keep_Onewindow

from selenium import webdriver
import time
import pandas as pd

from random import randint


class driver():

    def __init__(self):
        self.upload_path = "C:\\Users\\cheng.lu\\Desktop\\task_data\\"
        # 使用driver1进行上传

        # yq_task 处理完压缩文件以后的结果文件夹
        self.driver = webdriver.Chrome()
        self.zhanghao = 'driver1@connext.com.cn'
        self.mima = 'driver11'

    def login(self):
        self.driver.set_window_size(1600, 850)
        self.driver.get('http://47.103.81.169/Admin')

        self.driver.find_element_by_xpath(
            '//input[@name="username"]').send_keys(self.zhanghao)  # 输入账号
        self.driver.find_element_by_xpath(
            '//input[@name="password"]').send_keys(self.mima)  # 输入密码
        self.driver.find_element_by_xpath(
            '//div[@class="geetest_radar_tip"]').click()  # 点击自动验证
        self.driver.find_element_by_xpath(
            '//button[@class="layui-btn btn-submit"]').click()  # 点击登录
        time.sleep(5)

    def get_PingLunWindow(self):
        # 进入评论管理页面
        self.driver.find_element_by_xpath('//a[@data-id="167"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//a[@data-id="169"]').click()
        time.sleep(1)

        # 第一层iframe
        xf = self.driver.find_element_by_xpath(
            '//iframe[@onload="layui.layer.close(1)"]')
        self.driver.switch_to.frame(xf)

    def get_PingLunTask(self, num=0):
        # 在 评论管理里面 选择运行中的task
        self.driver.find_element_by_xpath('//input[@type="text"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//dd[@lay-value="0"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//span[@id="search"]').click()
        time.sleep(2)

        # 获取Number
        filepath = '//tr[@data-index="%s"]//div[contains(@class,"layui-table-cell")]' % num
        taskNo = self.driver.find_element_by_xpath(filepath).text
        # 查看
        filepath = '//tr[@data-index="%s"]//a[@lay-event="detail"]' % num
        self.driver.find_element_by_xpath(filepath).click()

        #------------→→→→第二层iframe
        xf1 = self.driver.find_element_by_xpath('//iframe[@scrolling="auto"]')
        self.driver.switch_to.frame(xf1)

        task_name = self.driver.find_element_by_xpath(
            '//label[text()="任务名称"]/parent::div//input[@type="text"]').get_attribute('value')
        pinpai_name = self.driver.find_element_by_xpath(
            '//label[text()="品牌名称"]/parent::div//input[@type="text"]').get_attribute('value')
        hangye_name = self.driver.find_element_by_xpath(
            '//label[text()="行业名称"]/parent::div//input[@type="text"]').get_attribute('value')
        good_name = self.driver.find_element_by_xpath(
            '//label[text()="商品名称"]/parent::div//input[@type="text"]').get_attribute('value')
        link = self.driver.find_element_by_xpath(
            '//label[text()="商品链接"]/parent::div//input[@type="text"]').get_attribute('value')

        self.task = pd.Series({'No': taskNo, '任务名称': task_name, '品牌名称': pinpai_name,
                               '行业名称': hangye_name, '商品名称': good_name, '商品链接': link})

        # 跳出当前iframe #点× 回到第一层iframe ←←←--------
        self.driver.switch_to.parent_frame()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '//a[@class="layui-layer-ico layui-layer-close layui-layer-close1"]').click()

    def upload_PingLunTask(self, filename):
        # 点击上传button 前台进入第二iframe
        uploadpath = '//div[text()="%s" ]/ancestor::tr//a[@lay-event="upload"]' % self.task['No']
        self.driver.find_element_by_xpath(uploadpath).click()
        time.sleep(2)

        # 第二层iframe
        xf1 = self.driver.find_element_by_xpath('//iframe[@scrolling="auto"]')
        self.driver.switch_to.frame(xf1)

        # input 文件路径 上传
        self.driver.find_element_by_xpath(
            '//input[@type="file"]').send_keys(self.upload_path + filename)
        time.sleep(5)

        # 上传文件button
        self.driver.find_element_by_xpath('//button[@id="upload"]').click()
        # 跳出当前iframe
        driver.switch_to.parent_frame()

    def tiaochu_iframe(self):
        self.driver.switch_to.parent_frame()

    def close_driver(self):
        self.driver.close()

if __name__ == '__main__':
    from con_yuqing import Tmall_Spider

    driver3 = Tmall_Spider()

    driver2 = driver()
    driver2.login()

    main_ct = 0
    while True:
        main_ct += 1
        try:
            driver2.get_PingLunWindow()
            driver2.get_PingLunTask()

            # driver3.run_task(driver2.task['商品链接'])
            #driver2.upload_PingLunTask(driver3.skuname + '.xlsx')

            try:
                driver3.run_task(driver2.task['商品链接'])
                driver2.upload_PingLunTask(driver3.skuname + '.xlsx')
            except CantFindNameError:
                driver2.upload_PingLunTask('错误提示' + '.xlsx')

        except Exception as e:
            time.sleep(8)
            print(e)
            print('当前错误计数  %s' % main_ct)
            try:
                driver2.tiaochu_iframe()
            except:
                continue
                

        try:
            if main_ct % 11 == 0:
                driver3.get('www.tmall.com')

            if main_ct % 23 == 0:
                driver3.get('www.taobao.com')

            if main_ct % 41 == 0:
                driver3.run_task(
                    'https://detail.tmall.hk/hk/item.htm?id=538868157890&skuId=3219421974803')

            if main_ct % 51 == 0:
                keep_Onewindow()
        except:
            pass

    # driver2.close_driver()
