from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from random import choice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as E
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class MyException(Exception):
    def __init__(self, arg):
        self.msg = arg

def ErrorPrint(*msgs):
    print "Browser Error:",
    for i in msgs[:-1]:
        print i,
    print msgs[-1]

def create_script(url):
    script = 'var element = document.createElement("MyExtensionDataElement");'
    script += 'element.setAttribute("attribute1", "' + url + '");'
    script += 'document.documentElement.appendChild(element);'
    script += 'var evt = document.createEvent("Events");'
    script += 'evt.initEvent("myCustomEvent", true, false);'
    script += 'element.dispatchEvent(evt);'
    return script

class Browser:
    def __init__(self, unstable_strategy = False):
        profile = webdriver.FirefoxProfile("/home/george/.mozilla/firefox/2zvawikk.default")
        if unstable_strategy:
            print "unstable strategy: ON"
            profile.set_preference("webdriver.load.strategy", "unstable")
        driver = webdriver.Firefox(profile)
        self.driver = driver

    def load_page(self, url):
        script = create_script(url)
        self.driver.execute_script(script)
        self.driver.get(url)
        print "Title:", self.driver.title

    def shut_down(self):
        self.driver.quit()

    def close_tab(self):
        if len(self.driver.window_handles) > 1:
            #close window
            self.driver.close()
            #switch to the next one in the queue
            self.driver.switch_to.window(self.driver.window_handles[0])

    def middle_click(self):
        link = self._link_generator()
        if link is not None:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(link)
                actions.context_click(link)
                actions.send_keys(Keys.ARROW_DOWN)
                #actions.send_keys(Keys.ARROW_DOWN)
                actions.send_keys(Keys.ENTER)
                actions.perform()
            except E.MoveTargetOutOfBoundsException:
                pass

    def left_click(self):
        link = self._link_generator()
        if link:
            self.load_page(link.get_attribute("href"))
        else:
            ErrorPrint("no link in this page")

    def go_back(self):
        self.driver.back()
        print self.driver.title

    def _get_element(self, tag_name):
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
            return element
        except:
            ErrorPrint(tag_name, "could not be found")
            return None

    def _check_url(self, url):
        if url is None:
            return False
        #if not("#" in url) and (url.startswith("http://")):
        if (url.startswith("http://") or url.startswith("https://")) and not("#" in url):
            return True
        return False

    def _link_generator(self):
        link = None
        counter = 0
        while not link:
            #in order to avoid infinite loop
            if counter > 100:
                ErrorPrint("too many broken links")
                break
            #find all links
            links = self.driver.find_elements_by_tag_name('a')
            if len(links) == 0:
                ErrorPrint("no links here")
                break
            #pick a link
            link = choice(links)
            #check if it is displayed
            try:
                if link.is_displayed():
                    try:
                        #check if "normal" url
                        if self._check_url(link.get_attribute('href')):
                            return link
                        else:
                            link = None
                    except E.NoSuchAttributeException:
                        ErrorPrint("no href")
                        link = None
                else:
                    link = None
            except E.StaleElementReferenceException:
                ErrorPrint("stale")
                link = None
            counter += 1
        return link

    def get_number_of_windows(self):
        return len(self.driver.window_handles)
