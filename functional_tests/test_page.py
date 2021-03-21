from selenium import webdriver
from account.models import *
from article.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import timezone
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class TestPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        Article.objects.create(headline="News Article Headline", body="News body", url="bbc.co.uk", image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/BBC_News_2019.svg/1200px-BBC_News_2019.svg.png", 
        category="politics", source="BBC", favourite=False, date=timezone.now())

    def tearDown(self):
        self.browser.close()
    
    def test_like_button(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)

        self.browser.find_element_by_css_selector('[class="btn btn-outline-info"]').click()
        time.sleep(1)

    def test_register(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)

        self.browser.find_element_by_id('register_button').click()
        time.sleep(1)

        username = self.browser.find_element_by_id('username')
        inputPassword1 = self.browser.find_element_by_id('inputPassword1')
        inputPassword2 = self.browser.find_element_by_id('inputPassword2')
        inputDoB = self.browser.find_element_by_id('inputDoB')
        inputEmail = self.browser.find_element_by_id('inputEmail')
        time.sleep(1)

        username.send_keys("testing")
        inputPassword1.send_keys("newsapptest123")
        inputPassword2.send_keys("newsapptest123")
        inputDoB.send_keys("01/01/1999")
        inputEmail.send_keys("testing@testing.com")
        time.sleep(1)
        self.browser.find_element_by_id('registerButton').click()
        time.sleep(2)
    
    def test_comments(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)

        self.browser.find_element_by_id('register_button').click()
        time.sleep(1)

        username = self.browser.find_element_by_id('username')
        inputPassword1 = self.browser.find_element_by_id('inputPassword1')
        inputPassword2 = self.browser.find_element_by_id('inputPassword2')
        inputDoB = self.browser.find_element_by_id('inputDoB')
        inputEmail = self.browser.find_element_by_id('inputEmail')
        time.sleep(1)

        username.send_keys("user321")
        inputPassword1.send_keys("newsapptest123")
        inputPassword2.send_keys("newsapptest123")
        inputDoB.send_keys("01/01/1999")
        inputEmail.send_keys("testing@testing.com")
        time.sleep(1)
        self.browser.find_element_by_id('registerButton').click()
        time.sleep(3)

        self.browser.find_element_by_id('commentsButton').click()
        time.sleep(3)

        self.browser.find_element_by_id('modalBtnClick').click()
        time.sleep(3)
        
        description = self.browser.find_element_by_id('id_description')
        description.send_keys("commenting")
        s1= Select(self.browser.find_element_by_id('id_post'))
        s1.select_by_index(1)
        s2= Select(self.browser.find_element_by_id('id_person'))
        s2.select_by_index(1)
        self.browser.find_element_by_id('submitComment').click()
        time.sleep(1)
        self.browser.find_element_by_id('closeComments').click()
        time.sleep(1)
        self.browser.find_element_by_id('homeButton').click()
        time.sleep(1)
        self.browser.find_element_by_id('commentsButton').click()
        time.sleep(3)

        self.browser.find_element_by_id('deleteButton').click()
        time.sleep(1)
        self.browser.find_element_by_id('confirmDeleteBook').click()
        time.sleep(1)
        self.browser.find_element_by_id('closeComments').click()
        time.sleep(1)
        self.browser.find_element_by_id('commentsButton').click()
        time.sleep(1)
        time.sleep(2)
        