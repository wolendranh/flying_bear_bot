from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

location = "Drahobrat"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.headless = True

driver = webdriver.Chrome(executable_path='/Users/y.hulpa/PycharmProjects/flying_bear_bot/selenium_drivers/chromedriver', options=options)
driver.get("https://snig.info/uk")

elem = driver.find_elements_by_xpath("//a[contains(@href, '/uk/{0}') and contains(@class, 'card--object')]".format(location))[0]
elem.click()

videos = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/uk/{}') and contains(@class, 'card--object')]".format(location))))

videos.click()

videos = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-ui")))
player = driver.find_element_by_class_name('fp-ui')
player.click()
active_video = WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, "//span[contains(@class, 'fp-elapsed')]"), "00:01"))
screenshot = player.screenshot("{}.png".format(location))

driver.close()
