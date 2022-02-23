from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

#e-devlet credentials
username = input("T.C. Kimlik No: ")
password = input("e-Devlet Şifresi: ")

#define driver
driver = webdriver.Firefox(executable_path=r'C:\Users\baris\.wdm\drivers\geckodriver\win64\v0.29.1\geckodriver.exe')

#go to adbs page
driver.get("https://adbs.uab.gov.tr/login")
#go to e-devlet authorization page
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/in-root/in-login/div/div[1]/div/div[1]/div/div/a")))

driver.find_element_by_xpath("/html/body/in-root/in-login/div/div[1]/div/div[1]/div/div/a").click()
sleep(2)

#username
driver.find_element_by_id("tridField").send_keys(username)
#password
driver.find_element_by_id("egpField").send_keys(password)
driver.find_element_by_class_name("submitButton").click()

#wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
# get the errors (if there are)
errors = driver.find_elements_by_class_name("flash-error")
# if we find that error message within errors, then login is failed
if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")
#sleep because it links to login page and then links to main page
sleep(3)

#go to education
driver.get("https://adbs.uab.gov.tr/users/my-educations/1")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/in-root/in-users/in-dashboard-layout/main/in-education-single/div/div/div[2]/div/div[2]/div/ul/li[8]/in-loading-button/dx-button")))
sleep(2)

goToLesson = driver.find_element_by_xpath("/html/body/in-root/in-users/in-dashboard-layout/main/in-education-single/div/div/div[2]/div/div[2]/div/ul/li[8]/in-loading-button/dx-button")
goToLesson.location_once_scrolled_into_view
driver.execute_script("arguments[0].click();", goToLesson)
sleep(2)

#accept the conditions
driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div[2]/div[1]/div/div").click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/in-root/in-users/in-dashboard-layout/main/in-lecture/div[2]/div[1]/div/div[2]/span[2]/in-loading-button/dx-button")), 10)

#start by skipping the first lessons
driver.find_element_by_xpath("/html/body/in-root/in-users/in-dashboard-layout/main/in-lecture/div[2]/div[1]/div/div[2]/span[2]/in-loading-button/dx-button").click()
sleep(20)
clickCount = 0

while True:
    # learn the text of timer at the start
    timer = driver.find_element_by_xpath(
        "/html/body/in-root/in-users/in-dashboard-layout/main/in-lecture/div[1]/in-timer/div/h4").text
    print("Time: " + timer)
    # lesson time by seconds
    minuteTime = int(timer[:2]) * 60
    secondTime = int(timer[3:])
    print("Time by seconds: ", (minuteTime + secondTime))
    #if timer is 00:00 click the button
    if timer == "00:00":
        driver.find_element_by_xpath("/html/body/in-root/in-users/in-dashboard-layout/main/in-lecture/div[2]/div[1]/div/div[2]/span[2]/in-loading-button/dx-button").click()
        clickCount += 1
        print("Clicked ", clickCount, " times!")
    # wait till timer ends
    sleep(minuteTime + secondTime + 10)
    #wait to throw exception
    driver.implicitly_wait(30)
    sleep(5)