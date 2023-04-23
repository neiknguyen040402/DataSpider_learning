from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='venv/chromedriver.exe')  #trỏ đến vị trí lưu chrome driver
driver.get('https://vnexpress.net/')

print(driver.title)               #lấy tiêu đề
print(driver.page_source)         #lấy source

articles = driver.find_elements(By.CSS_SELECTOR, 'article.item-news')
for article in articles:
    try:
        title = article.find_element(By.TAG_NAME, 'h3').text
        desc = article.find_element(By.TAG_NAME, 'p').text
        link = article.find_element(By.CSS_SELECTOR, 'h3.title-news > a').get_attribute('href')
        print(title)
        print(desc)
        print(link)
        print("============")
    except NoSuchElementException:
        pass

driver.close()   #đóng trình duyệt
# driver.quit()    #đóng tất cả thứ liên quan driver mở ra