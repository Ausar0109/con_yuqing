from selenium import webdriver
import time
from random import choice

randomlist = [0] * 35 + [1] * 3 + [2] * 2

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "C:\\Users\\cheng.lu\\Desktop\\yq_mid\\"}
options.add_experimental_option("prefs", prefs)


class driver2():

    def __init__(self):
        self.download_path = "C:\\Users\\cheng.lu\\Desktop\\yq_mid\\"
        # 使用driver2进行下载的压缩包，会进入这个文件夹
        self.upload_path = "C:\\Users\\cheng.lu\\Desktop\\yq_res\\"
        # yq_task 处理完压缩文件以后的结果文件夹
        self.driver = webdriver.Chrome(options=options)
        self.zhanghao = 'driver2@connext.com.cn'
        self.mima = 'driver22'

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

    def get_yuqingWindow(self):
        # 进入语义分析的模块
        self.driver.find_element_by_xpath('//a[@data-id="187"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//a[@data-id="189"]').click()
        time.sleep(1)

        # 第一层iframe
        xf = self.driver.find_element_by_xpath(
            '//iframe[@onload="layui.layer.close(1)"]')
        self.driver.switch_to.frame(xf)

    def get_yuqingTask(self, num=0):
        # 选择运行中
        self.driver.find_element_by_xpath('//input[@type="text"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//dd[@lay-value="0"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//span[@id="search"]').click()
        time.sleep(2)

        # 获取Number
        filepath = '//tr[@data-index="%s"]//div[contains(@class,"layui-table-cell")]' % num
        self.taskNo = self.driver.find_element_by_xpath(filepath).text
        # 下载
        download_path = '//tr[@data-index="%s"]//a[@lay-event="download_file"]' % num
        self.driver.find_element_by_xpath(download_path).click()
        time.sleep(2)

    def upload_yuqingTask(self, result_fileName):
        # 上传  点击上传的按钮 进入第二层iframe的前台
        uploadpath = '//div[text()="%s" ]/ancestor::tr//a[@lay-event="upload"]' % self.taskNo
        self.driver.find_element_by_xpath(uploadpath).click()

        #------------→→→→  进入第二层iframe
        xf1 = self.driver.find_element_by_xpath('//iframe[@scrolling="auto"]')
        self.driver.switch_to.frame(xf1)

        time.sleep(2)
        self.driver.find_element_by_xpath(
            '//input[@type="file"]').send_keys(self.upload_path + result_fileName + '【分析结果】.xlsx')
        # 点击上传按钮
        time.sleep(3)
        self.driver.find_element_by_xpath('//button[@id="upload"]').click()

        # 跳出第二层iframe，回到第一层iframe ←←←--------
        self.driver.switch_to.parent_frame()

    def tiaochu_iframe(self):
        self.driver.switch_to.parent_frame()

    def close_driver(self):
        self.driver.close()

if __name__ == '__main__':
    from con_yuqing import *
    lc = driver2()
    lc.login()

    while True:
        try:
            lc.get_yuqingWindow()

            iii = choice(randomlist)
            print('----------------%s' % iii)

            lc.get_yuqingTask(iii)
            time.sleep(2)

            try:
                nam1 = yq_task()
                lc.upload_yuqingTask(nam1)
            except:
                lc.upload_yuqingTask('错误提示') 

            
        except Exception as e:
            time.sleep(10)
            print(e)
            try:
                clean_all()
                lc.tiaochu_iframe()
            except:
                pass
