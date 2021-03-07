from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

import time

from util.config_extension import ConfigExtension
from util.file_extension import FileExtension

class InstagramBot:    
    users_to_follow = []
    date_start_execution = datetime.now().strftime("%m%d%Y%H%M%S")

    def __init__(self):
        self.username = ConfigExtension.get('AUTH')['username']
        self.password = ConfigExtension.get('AUTH')['password'][1:-1]        
        self.hashtag = ConfigExtension.get('TARGET')['hashtag']
        self.posts_finished_filepath = 'posts\\' + 'posts_finished_' + self.date_start_execution + '.txt'
        self.users_followed_filepath = 'users\\' + 'users_followed_' + self.date_start_execution + '.txt'
        self.number_of_times_to_scroll_feed = int(ConfigExtension.get('SETTINGS')['number_of_times_to_scroll_feed'])

        FileExtension.create_file(self.posts_finished_filepath, '------- posts finished -------\n')
        FileExtension.create_file(self.users_followed_filepath, '------- users followed -------\n')

        self.driver = webdriver.Chrome(ChromeDriverManager().install())

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

    def search_posts_by_hashtag(self):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + self.hashtag + "/")

        time.sleep(3) 
    
    def get_posts_and_follow_people_who_commented(self):
        driver = self.driver

        count = 0
        while True:
            posts_urls = self.get_posts()
            
            for i, post_url in enumerate(posts_urls):
                if i == 30:
                    time.sleep(60 * 5)

                driver.get(post_url)

                time.sleep(3)

                try:
                    self.find_people_on_comments_and_follow()

                    self.store_finished_posts(post_url)
                except Exception as e:
                    print(e)
                    time.sleep(5)

            self.scroll_over_feed()

            count = count + 1
            if (count == self.number_of_times_to_scroll_feed):
                break
    
    def get_posts(self):
        driver = self.driver

        posts_finished = FileExtension.read_lines_all_files_on_folder('posts')

        posts_urls = []
        while len(posts_urls) < 32:    
            posts_elements = driver.find_elements_by_tag_name("a")

            posts_urls = [elem.get_attribute("href") for elem in posts_elements]
            posts_urls = [
                    link for link in posts_urls
                    if 'https://www.instagram.com/p' in link
                        and (link not in posts_finished)
                ]

            if len(posts_urls) < 32:
                self.scroll_over_feed()

        return posts_urls    

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

            time.sleep(2)

            try:
                already_followed_user = driver.find_element_by_xpath("//span[contains(@class, 'vBF20')]/button/div/span[contains(@class, 'glyphsSpriteFriend_Follow u-__7')]")

                self.store_followed_users(profile)
            except Exception as err:
                continue

            try:
                time.sleep(2)

                follow_button = driver.find_element_by_xpath("//span[contains(@class, 'vBF20')]/button")

                time.sleep(2)

                follow_button.click()

                self.store_followed_users(profile)

                time.sleep(2)                
            except Exception as err:
                continue    

    def store_finished_posts(self, url: str):
        FileExtension.append_to_file(self.posts_finished_filepath, url + '\n')

    def store_followed_users(self, url: str):
        FileExtension.append_to_file(self.users_followed_filepath, url + '\n')

    def scroll_over_feed(self):
        driver = self.driver

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)   

instagram_bot = InstagramBot()

instagram_bot.login()
instagram_bot.search_posts_by_hashtag()
instagram_bot.get_posts_and_follow_people_who_commented()