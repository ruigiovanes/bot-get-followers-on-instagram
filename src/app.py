from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

from util.config_extension import ConfigExtension

class InstagramBot:
    posts_finished = []
    users_to_follow = []

    def __init__(self):
        self.username = ConfigExtension.get('AUTH')['username']
        self.password = ConfigExtension.get('AUTH')['password'][1:-1]        
        self.hashtag = ConfigExtension.get('TARGET')['hashtag']        
        self.number_of_times_to_scroll_feed = int(ConfigExtension.get('SETTINGS')['number_of_times_to_scroll_feed'])

        self.driver = webdriver.Firefox(
            executable_path=r'D:\Projetos\Python\Automação\Drivers\geckodriver.exe'
        )

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com")
        
        time.sleep(3)

        try:
            login_button = driver.find_element_by_xpath(
                "//a[@href='/accounts/login/?source=auth_switcher']"
            )
            login_button.click()
        except:
            print('já estamos na página de login')
            pass
        
        user_element = driver.find_element_by_xpath("//input[@name='username']")
        user_element.clear()
        user_element.send_keys(self.username)

        time.sleep(1)

        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)

        time.sleep(1)

        password_element.send_keys(Keys.RETURN)

        time.sleep(3)

    def find_profile(self, profile: str):
        driver = self.driver
        driver.get(f"https://www.instagram.com/{profile}/")
        
        time.sleep(3)

    def search_posts_by_hashtag(self):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + self.hashtag + "/")

        time.sleep(3) 
    
    def get_posts_and_follow_people_who_commented(self):
        driver = self.driver

        count = 1
        while True:
            posts_links = self.get_posts()
            for post_link in posts_links:
                driver.get(post_link)

                time.sleep(3)

                try:
                    self.find_people_on_comments_and_follow()

                    self.posts_finished.append(post_link)
                except Exception as e:
                    print(e)
                    time.sleep(5)

            self.scroll_over_feed()

            count = count + 1
            if (count > self.number_of_times_to_scroll_feed):
                break
    
    def get_posts(self):
        driver = self.driver

        posts_elements = driver.find_elements_by_tag_name("a")
        posts_links = [elem.get_attribute("href") for elem in posts_elements]
        posts_links = [link for link in posts_links if 'https://www.instagram.com/p' in link and link not in self.posts_finished]

        return posts_links    

    def find_people_on_comments_and_follow(self):
        driver = self.driver
    
        while True:
            try:
                load_comments_button = driver.find_element_by_class_name("dCJp8")
            except Exception as err:
                break

            load_comments_button.click()

        users_who_commented = driver.find_elements_by_class_name("_6lAjh")
        for i, user in enumerate(users_who_commented):
            if i == 0 or user in self.users_to_follow:
                continue

            username = user.find_element_by_tag_name("a")

            self.users_to_follow.append(username.text)

        self.follow_people()

    def follow_people(self):
        driver = self.driver

        for profile in self.users_to_follow:
            self.find_profile(profile)

            try:
                follow_button = driver.find_element_by_xpath("//button[contains(text(), 'Seguir')]")
                follow_button.click()

                time.sleep(2)
            except Exception as err:
                continue

    def scroll_over_feed(self):
        driver = self.driver

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)   

instagram_bot = InstagramBot()

instagram_bot.login()
instagram_bot.search_posts_by_hashtag()
instagram_bot.get_posts_and_follow_people_who_commented()