from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import sleep

def get_user_and_password(file):
    user, password = "", ""
    with open(file) as f:
        for line in f:
            words = line.strip().split(":")
            words = [i.strip().lower() for i in words]
            if words[0] == "username" or words[0] == "email":
                user += words[1]
            else:
                password += words[1]
    return user, password

def open_facebook(username, user_password):
    path = os.path.join(os.getcwd(), "geckodriver/geckodriver")
    browser = webdriver.Firefox(executable_path=path)
    browser.get("https://www.facebook.com/")
    user = browser.find_element_by_id("email")
    user.send_keys(username)
    sleep(5)
    password = browser.find_element_by_id("pass")
    password.send_keys(user_password)
    sleep(5)
    browser.find_element_by_id("u_0_b").click()


if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), "facebook_user_and_password.txt")
    username, user_password = get_user_and_password(file_path)

    open_facebook(username, user_password)