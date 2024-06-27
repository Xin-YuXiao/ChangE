from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

# 设置下载目录
download_dir = r"C:\Users\xiaoyu\Desktop\Tsinghua\downloads"

# 配置Firefox选项   Xiao_20240314    2975800832xxy.
options = webdriver.FirefoxOptions()

# 设置下载首选项
options.set_preference("browser.download.folderList", 2)  # 使用自定义下载路径
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", download_dir)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # 如果需要添加更多的MIME类型

# 使用配置文件初始化浏览器
browser = webdriver.Firefox(options=options)

# 打开数据下载页面
browser.get("https://moon.bao.ac.cn/ce5web/searchOrder_dataSearchData.search")

# 手动登录时暂停
sleep(60)

# 要下载的页数
page_n = 159
file_n = 0

def is_downloadable(title):
    # 检查文件是否为需要下载的类型
    return any(ext in title for ext in ['.2B', '.2BL', '2A', '.2AL', '2C', '.2CL'])

for page_i in range(page_n):
    elements = browser.find_elements(By.CLASS_NAME, "search-item-title")  # 查找全部数据项的标题
    download_buttons = browser.find_elements(By.CLASS_NAME, "downloadNow")  # 查找全部下载按钮
    
    for element_i, download_button in zip(elements, download_buttons):
        title = element_i.text  # 获取数据项的标题
        if is_downloadable(title):
            download_button.click()
            file_n += 1
            print(file_n)
            # sleep(1)  # click之后有一定的延迟，这时已经可以进行下一个下载了，不需要sleep

    # 尝试找到并点击“下一页”按钮
    try:
        # 使用 XPath 查找包含特定属性和类的 <a> 标签
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'x-btn') and contains(@data-qtip, 'Next Page')]"))
        )
        print("找到了下一页按钮")
        
        # 滚动到按钮位置
        browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
        sleep(1)  # 确保滚动完成

        # 使用 JavaScript 点击按钮
        browser.execute_script("arguments[0].click();", next_button)
        sleep(5)  # 等待页面刷新并加载数据
    except Exception as e:
        print(f"在第 {page_i + 1} 页无法找到下一页按钮: {e}")
        break

browser.quit()
