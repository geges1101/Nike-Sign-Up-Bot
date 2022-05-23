import json
import time
import zipfile
from threading import Thread

from selenium.webdriver.common.by import By
from seleniumwire import webdriver

path = '/Users/geges/PycharmProjects/SwooshRega/SwooshRega/chromedriver'

def acp_api_send_request(driver, message_type, data={}):
    message = {
		# this receiver has to be always set as antiCaptchaPlugin
        'receiver': 'antiCaptchaPlugin',
        # request type, for example setOptions
        'type': message_type,
        # merge with additional data
        **data
    }
    # run JS code in the web page context
    # preceicely we send a standard window.postMessage method
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))

class Bot:
    def __init__(self, email, proxy):
        string0, separator, string0_1 = proxy.partition(':')
        string1, separator, string2 = string0_1.partition(':')
        string3, separator, string4 = string2.partition(':')
        string5, separator, string6 = string4.partition(':')
        PROXY_USER = string0
        PROXY_PASS = string1
        PROXY_HOST = string3
        PROXY_PORT = string5
        print(PROXY_USER, PROXY_PASS, PROXY_HOST, PROXY_PORT)
        manifest_json = """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                        "scripts": ["background.js"]
                    },
                    "minimum_chrome_version":"22.0.0"
                }
                """

        background_js = """
                var config = {
                        mode: "fixed_servers",
                        rules: {
                        singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                        },
                        bypassList: ["localhost"]
                        }
                    };

                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }

                chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                );
                """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        pluginfile = 'plugpro/' + email + '.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_extension(pluginfile)
        self.website = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        time.sleep(1)
        self.email = email

    def register(self, link):
        self.website.get(link)
        time.sleep(18)
        print(link)
        Elem = self.website.find_element(By.XPATH, '//*[@id="__next"]/div/footer/div/div[2]/div[2]/div[2]/div/button')
        Elem.click()
        time.sleep(2)
        Elem = self.website.find_element(By.XPATH, '//*[@id="__next"]/div/footer/div/div[2]/div[2]/div[2]/div/input')
        Elem.send_keys(self.email)
        time.sleep(2)
        Elem = self.website.find_element(By.XPATH, '//*[@id="__next"]/div/footer/div/div[2]/div[2]/div[2]/div/button')
        Elem.click()
        time.sleep(8)
        with open("results", 'a') as res:
            res.writelines([self.email, '\n'])

    def makeall(self):
        link = "https://www.swoosh.nike/en-US"
        time.sleep(5)
        self.register(link)
        time.sleep(0.5)

if __name__ == "__main__":
    EMAILS = []
    PROXY = []
    with open('emails', "r") as names:
        while True:
            text = names.readline()
            if not text:
                break

            text = text.split(':')
            EMAILS.append(text[0])

    with open("proxy", "r") as status:
        while True:
            text = status.readline()
            if not text:
                break
            PROXY.append(text)

    threads = []
    PROXYNUM = 25
    for j in range(0, len(EMAILS), 10):
        for i in range(10):
            bot = Bot(EMAILS[j+i], PROXY[(i+j) % PROXYNUM])
            th = Thread(target=bot.makeall, args=())
            th.start()
            threads.append(th)
            time.sleep(2.5)
        for x in threads:
            x.join()