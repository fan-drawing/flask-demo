# 自动化测试工具 Selenium3

## 浏览器驱动 webdriver

引用方法 from selenium import webdriver
.click() 点击事件
.clear() 输入内容清除
.send_keys("前端开发出路") 内容的输入
.maximize_window() 设置浏览器最大化
.get("url") 打开网页
.find_element_by_id(‘kw’) 根据id定位获取元素

除此之外还有键盘和鼠标事件

``` python
from selenium import webdriver
import time
# 打开浏览器
driver = webdriver.Edge()
# 设置浏览器最大化
driver.maximize_window()
# 设置隐式等待
driver.implicitly_wait(10)
# 打开网页
driver.get("http://www.baidu.com")
# 定位搜素框
sercah_element = driver.find_element_by_id('kw')
# 输入内容
sercah_element.send_keys("前端开发出路")
time.sleep(3)
# 等待3秒
driver.find_element_by_id('su').click()
time.sleep(12)
# 退出浏览器
driver.quit()
```


# 定位

``` python
ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"
```