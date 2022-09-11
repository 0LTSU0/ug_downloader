import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

CHROMEDRIVER_PATH = "./chromedriver.exe" 
PYTHON_INTERPETER = "python3"
DOWNLOAD_PATH = r"D:\Tiedostot\UG_rip"
PROCESS_NUM = 0
driver = None
wait = None


#Start webdriver and login
def init():
    global driver, wait
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": DOWNLOAD_PATH})
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    wait = WebDriverWait(driver, 5)

    with open("./logins.json", "r") as f:
        logins = json.load(f)
    driver.get("https://www.ultimate-guitar.com/")
    
    #Get rid of gdpr thing if needed:
    bypass_gpdr()

    if logins.get("username") not in driver.page_source:
        print("[{}]".format(PROCESS_NUM), "Need to login")
        login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button/span[text()="Log in"]')))
        login_button.click()
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.OcirG.i2Ybl.GW8L7.i2Ybl > article > section > div.t1Pku > div > form > div > div.YV1G9 > input')))
        username.send_keys(logins.get("email"))
        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.OcirG.i2Ybl.GW8L7.i2Ybl > article > section > div.t1Pku > div > form > div > div.wlfii > div > input')))
        password.send_keys(logins.get("password"))
        login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.OcirG.i2Ybl.GW8L7.i2Ybl > article > section > div.t1Pku > div > form > div > div.ViYGM > button > span')))
        login_button.click()
        time.sleep(5)
        assert logins.get("username") in driver.page_source
        print("[{}]".format(PROCESS_NUM), "Login successfull")


def bypass_gpdr():
    try:
        agree_stuff = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
        agree_stuff.click()
    except Exception:
        pass


def download_tab():
    if "Oops! We couldn't find that page." not in driver.page_source:
        try:
            dl_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button/span[text()="DOWNLOAD Guitar Pro TAB"]')))
            driver.execute_script("arguments[0].click();", dl_button)
            print("[{}]".format(PROCESS_NUM), "Download started successfully")
        except Exception as e:
            print("[{}]".format(PROCESS_NUM), "Not a pro tab")
    else:
        print("[{}]".format(PROCESS_NUM), "Invalid url")


def main(start, end):
    global driver
    for i in range(start, end + 1):
        #url_process = "https://tabs.ultimate-guitar.com/tab/metallica/nothing-else-matters-guitar-pro-" + str(i)
        url_process = "https://tabs.ultimate-guitar.com/tab/download?id={}&session_id=".format(str(i))
        print("[{}]".format(PROCESS_NUM), "Procesing URL", url_process)
        driver.get(url_process)
        
        if "Oops! We couldn't find that page." not in driver.page_source:
            bypass_gpdr()
            download_tab()
        

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, help='Start index', action="store", required=True)
    parser.add_argument('--end', type=int, help='End index', action="store", required=True)
    parser.add_argument('--process_num', type=int, help='# of process', action="store", required=True)
    args = parser.parse_args()
    PROCESS_NUM = args.process_num

    #Init chrome
    init()

    #Start download
    main(args.start, args.end)


    #Testing
    #main(243583, 243584)
    #main(688019, 688019)
    #main(1239357, 1239357)

    #Close chrome
    driver.close()
