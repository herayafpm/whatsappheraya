import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlencode
from bs4 import BeautifulSoup


class WhatsAppElements:
    search = (By.CSS_SELECTOR, "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
    form = (By.CSS_SELECTOR, "footer._2cYbV > div.copyable-area > div > span > div._6h3Ps > div._2lMWa > div.p3_M1 > div > div._13NKt.copyable-text.selectable-text")
    header_user = (By.CSS_SELECTOR, "header._23P3O > div._1yNrt > div > div > div._2cNrC")
    tutup_user = (By.CSS_SELECTOR, "div#app > div > span:nth-of-type(4) > div > ul > div > div > li:nth-of-type(5)")

class WhatsApp:
    browser =  None
    timeout = 10  # The timeout is set for about ten seconds
    def __init__(self, wait, screenshot=None, session=None):
        self.browser = webdriver.Chrome(executable_path="./driver/chromedriver_96/chromedriver.exe")# change path
        self.browser.get("https://web.whatsapp.com/") #to open the WhatsApp web
        # you need to scan the QR code in here (to eliminate this step, I will publish another blog
        WebDriverWait(self.browser,wait).until(EC.presence_of_element_located(WhatsAppElements.search)) #wait till search element appears

    def unread_usernames(self, scrolls=100):
        initial = 10
        usernames = []
        for i in range(0, scrolls):
            self.browser.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_2nY6U _3C4Vf"):
                if i.find("div", class_="_3OvU8"):
                    username = i.find("div", class_="zoWT4").text
                    usernames.append(username)
            initial += 10
        # Remove duplicates
        usernames = list(set(usernames))
        return usernames
    def get_last_message_for(self, name):
        messages = list()
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name+Keys.ENTER)
        time.sleep(1)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-in"):
            message = i.find("span", class_="selectable-text")
            if message:
                message2 = message.find("span")
                messages.append(message2.text)
        messages = list(filter(None, messages))
        return messages
    def send_message(self,message,wait=10):
        WebDriverWait(self.browser,wait).until(EC.presence_of_element_located(WhatsAppElements.form))
        form = self.browser.find_element(*WhatsAppElements.form)
        form.send_keys(message+Keys.ENTER)
        # _2qR8G _1wMaz _19zgN _18oo2
        # time.sleep(3)
        # footer_message = self.browser.find("footer",class_="_2cYbV")
        # form_text = footer_message.find("div",class_="copyable-area").find("div",class_="_6h3Ps")
        # form_text.find("div",class_="_13NKt copyable-text selectable-text").sendKeys(message)
    def tutup_tab_user(self,wait=10):
        WebDriverWait(self.browser,wait).until(EC.presence_of_element_located(WhatsAppElements.header_user))
        header_user = self.browser.find_element(*WhatsAppElements.header_user)
        header_user.click()
        WebDriverWait(self.browser,wait).until(EC.presence_of_element_located(WhatsAppElements.tutup_user))
        tutup_user = self.browser.find_element(*WhatsAppElements.tutup_user)
        tutup_user.click()
    