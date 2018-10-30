from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
chrome_options.add_argument('window-size=1366x768') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
driver = webdriver.Chrome(executable_path="../chrome_driverFile/chromedriver_win32/chromedriver.exe",chrome_options=chrome_options)
driver.get("http://12366.cqsw.gov.cn:7004/ssoserver/login")
time.sleep(1)
driver.save_screenshot("../saved_images/报税网首页.png")
#输入账号
driver.find_element_by_id("username").send_keys("15223064509")
#输入密码
driver.find_element_by_name("password").send_keys("cy989898")
#保存验证码的图片
driver.save_screenshot("../saved_images/验证码.png")
#输入验证码
check_code = input("请输入验证码:")
print(r"验证码是多少:%s" % check_code)
driver.find_element_by_id("captcha").send_keys(check_code)
#点击登录按钮
driver.find_element_by_xpath("//*[@id=\"zrrLoginBtn\"]").click()
#休眠一下等待登录成功
time.sleep(3)
#保存登录成功的快照
driver.save_screenshot("../saved_images/登录成功.png")
#消除弹窗提示
driver.find_element_by_id("closeWid").click()
#点击申报纳税a标签
driver.find_element_by_xpath("//*[@id=\"left-contain\"]/ul[1]/li[2]/ul/li[4]/a").click()
#点击增值税纳税a标签
driver.find_element_by_xpath("//*[@id=\"left-contain\"]/ul[1]/li[2]/ul/li[4]/ul/li[1]/a").click()
#保存截图
driver.save_screenshot("../saved_images/增值税.png")
#保存成功登录好的html到本地
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
        driver.switch_to_window(handle)
        routeWindowHandle=driver.current_window_handle
        routeTitle=driver.title
        break
time.sleep(6)
print(f"4. switch to routeWindow, routeWindowHandle = {routeWindowHandle},routeTitle = {routeTitle}, currentHandle = {driver.current_window_handle}, currentTitle = {driver.title}")
#截取当前页面
driver.save_screenshot("../saved_images/点击填表申报以后.png")
#退出成功
driver.quit()
print("全部执行结束")