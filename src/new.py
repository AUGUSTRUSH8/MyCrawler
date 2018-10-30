'''
Created on 2018年10月30日

@author: AUGUSTRUSH
'''
'''
dzswj.cq-l-tax.gov.cn
12366.cqsw.gov.cn
以上两个网址都可以登进系统，可能重庆纳税网站正在完成新旧系统的迁移工作
'''
#前提：需要pip后者conda安装selenium包
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
#登录函数
def Login(driver):
    driver.get("http://12366.cqsw.gov.cn:7004/ssoserver/login")
    #延时一秒
    time.sleep(1)
    #截取当前登录页面图片并保存
    driver.save_screenshot("../saved_images/报税网首页.png")
    #获取当前需要登录的用户名密码
    (username, password), = readCSVFile().items()
    #输入账号
    driver.find_element_by_id("username").send_keys(username)
    #输入密码
    driver.find_element_by_name("password").send_keys(password)
    #保存验证码的图片
    driver.save_screenshot("../saved_images/验证码.png")
    #阻塞输入验证码
    check_code = input("请输入验证码:")
    print(r"验证码是多少:%s" % check_code)
    #向登录页面输入验证码信息
    driver.find_element_by_id("captcha").send_keys(check_code)
    #点击登录按钮
    driver.find_element_by_xpath("//*[@id=\"zrrLoginBtn\"]").click()
    #休眠一下等待登录成功
    time.sleep(3)
    #保存登录成功的快照
    driver.save_screenshot("../saved_images/登录成功.png")
    #消除弹窗提示 此处需注意，该网站会不定期的在初次登录时候弹出通知信息框
    #因此这里的弹窗信息是不确定的，但每次都是调用相同的弹窗组件提示显示，
    #所以以下执行两次关闭弹窗点击
    driver.find_element_by_id("closeWid").click()
    driver.find_element_by_id("closeWid").click()
    #截取点击完弹窗按钮后的页面
    driver.save_screenshot("../saved_images/消除弹窗主页面.png")
    #销毁无头浏览器进程--重要，否则会一直阻塞
    driver.quit()
#点击"申请纳税"按钮
def clickPayTaxButton(driver):
    #点击申报纳税a标签
    driver.find_element_by_xpath("//*[@id=\"left-contain\"]/ul[1]/li[2]/ul/li[4]/a").click()
#begin----增值税纳税函数模块起始
#点击"增值税小规模纳税人申报"a标签
#此处会跨域请求获取资源，并展现在当前页面当中，当前window_handle
def clickThroughVATaTag():
    #点击增值税纳税a标签
    driver.find_element_by_xpath("//*[@id=\"left-contain\"]/ul[1]/li[2]/ul/li[4]/ul/li[1]/a").click()
    #保存截图
    driver.save_screenshot("../saved_images/增值税.png")
    #保存当前页面的html到本地
    with open("../saved_htmlFile/cqTax.html","w",encoding="utf-8") as f:
        f.write(driver.page_source)
    #切换到iframe里面去
    driver.switch_to.frame("mainframe")
    #点击填表申报
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/ul[1]/li[5]/a").click();
    #点击后等待5秒
    time.sleep(5)
    # 拿到所有的窗口
    allHandles = driver.window_handles
    routeWindowHandle = 0
    routeTitle = 'None'
    for handle in allHandles:
        if handle!=driver.current_window_handle:
            #切换到新开页面
            driver.switch_to_window(handle)
            routeWindowHandle=driver.current_window_handle
            routeTitle=driver.title
            break
    time.sleep(6)
    print(f"4. switch to routeWindow, routeWindowHandle = {routeWindowHandle},routeTitle = {routeTitle}, currentHandle = {driver.current_window_handle}, currentTitle = {driver.title}")
    #截取当前页面
    driver.save_screenshot("../saved_images/点击填表申报以后.png")
#end----增值税纳税函数模块结束
def readCSVFile():
    # 读取csv至字典
    csvFile = open("../usernameAndPassword/userInfo.csv", "r")
    reader = csv.reader(csvFile)
    # 建立空字典
    result = {}
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1:
            continue
        result[item[0]] = item[1]
    csvFile.close()
    return result
def main():
    #初始化浏览器
    chrome_options = Options()
    chrome_options.add_argument('window-size=1366x768') #指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    #初始化一个局部对象driver
    driver = webdriver.Chrome(executable_path="../chrome_driverFile/chromedriver_win32/chromedriver.exe",chrome_options=chrome_options)
    return driver
if __name__ == "__main__":
    #获得初始化了参数的driver对象，它一旦初始化就全局使用
    driver=main()
    #执行登录操作
    Login(driver)
    print("登录结束")
    #首页打开后，默认会展开"办税服务"下拉菜单，然后需要
    #点击"申请纳税"子菜单，否则会报invisible异常（所见即所得）
    clickPayTaxButton(driver)
              