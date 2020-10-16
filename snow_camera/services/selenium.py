from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

SNIG_URL = "https://snig.info/uk"


def get_location_snow_camera_screenshot(location: str):
    options = webdriver.ChromeOptions()
    options.binary_location = settings.GOOGLE_CHROME_BIN
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True

    driver = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH, options=options)
    driver.get(SNIG_URL)

    elem = driver.find_elements_by_xpath(
        "//a[contains(@href, '/uk/{0}') and contains(@class, 'card--object')]".format(location))[0]
    elem.click()

    videos = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/uk/{}') and contains(@class, 'card--object')]".format(location))))

    videos.click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-ui")))
    player = driver.find_element_by_class_name('fp-ui')
    player.click()
    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element(
        (By.XPATH, "//span[contains(@class, 'fp-elapsed')]"), "00:01")
    )
    player.screenshot("/tmp/{}.png".format(location))
    driver.close()
    return "/tmp/{}.png".format(location)
