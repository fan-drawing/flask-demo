import time
from selenium import webdriver
from selenium.webdriver.common.by import By
 
# 通过指定chromedriver的路径来实例化driver对象，chromedriver放在当前目录。
# driver = webdriver.Chrome(executable_path='./chromedriver')
# chromedriver已经添加环境变量
driver = webdriver.Chrome()

# 控制浏览器访问url地址
driver.get("https://www.baidu.com/")

eles = driver.find_elements(By.CLASS_NAME, "hotsearch-item")
index = 0
for ele in eles:
  index += 1
  print("%d:%s" % (index, ele.find_element(By.CLASS_NAME, "title-content-title").text))
# 在百度搜索框中搜索'python'
driver.find_element(By.ID, "kw").send_keys('python')
# 点击'百度搜索'
driver.find_element(By.ID, "su").click()
 
time.sleep(6)
# 退出浏览器
driver.quit()

 