from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import random as rd
import time
import pandas as pd
import re
from dotenv import load_dotenv
import os

load_dotenv()

class TweetScrap():
    def __init__(self,title,from_date,to_date,limit_time):
        
        self.proxy_ip =  os.getenv('PROXY_IP')
        self.proxy_port = os.getenv('PROXY_PORT')
        self.proxy_options = {
            'proxy': {
                'httpProxy': f'{self.proxy_ip}:{self.proxy_port}',
                'ftpProxy': f'{self.proxy_ip}:{self.proxy_port}',
                'sslProxy': f'{self.proxy_ip}:{self.proxy_port}',
                'proxyType': 'MANUAL',
            }
        }
        self.word = self.change_word(title)
        self.from_date = from_date
        self.to_date = to_date
        self.limit_time = limit_time

    def wait(self,duration='short'):
        if duration =='short':
            return time.sleep(rd.randrange(1,3))
        elif duration =='medium':
            return time.sleep(rd.randrange(3,6))
        elif duration =='long':
            return time.sleep(rd.randrange(9,12))

    def change_word(self,word):
        split_word =  word.split(" ")
        words = ""
        for i in range(len(split_word)):
            words = words + split_word[i] + "%20"
        return words
    
    def open_web(self):
        self.driver = webdriver.Chrome(options=webdriver.ChromeOptions().add_experimental_option('proxy', self.proxy_options))
    
    def open_twitter(self):      
        self.driver.get(f'https://www.twitter.com')
        self.wait('medium')

    def login(self):
        masuk_btn = self.driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div')
        masuk_btn.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')))
        #find
        username_field = self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        login_selanjutnya_button = self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')

        #do login
        username_field.send_keys(os.getenv('UNAME'))
        self.wait()
        login_selanjutnya_button.click()
        self.wait()
        password_field = self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        masuk_button = self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
        self.wait()
        password_field.send_keys(os.getenv('PASSWORD'))
        masuk_button.click()
        self.wait('medium')

    def query_from_date(self,query,since,until):
        self.driver.get(f'https://twitter.com/search?q={query}lang%3Aid%20since%3A{since}%20until%3A{until}&src=typed_query&f=live')
        self.wait()

    def get_tweets(self,max_time_each = 300):
        swr = 0
        #choose the date
        until = self.to_date
        since = self.from_date
        #scraptime
        scraptime = max_time_each
        #path
        self.query_from_date(query=self.word,since=since,until=until)
        pyautogui.moveTo(383, 442)
        start_time = time.time()
        all_tweets = []
        verify_tweet_list = []
        time.sleep(1)
        end_count = 0
        all_time =  start_time + scraptime

        while time.time() < all_time:
            try:
                users = self.driver.find_elements(By.XPATH,"//*[@class='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1awozwy r-18u37iz']")
                #print('users:', users)
                tweets = self.driver.find_elements(By.XPATH,"//*[@class='css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim']")
                #print('tweet:',tweets)
                tweet_list = [tweet.text for tweet in tweets]
                #print('tweetlist:',tweet_list)
                users_list = [user.text for user in users]
                #print('uslist:',users_list)
                if tweet_list != verify_tweet_list:
                    end_count = 0
                    for user,tweet in zip(users_list,tweet_list):
                        split_data = user.split('\n')
                        accountname = split_data[0]
                        #print('accname:',accountname)
                        username = split_data[1]
                        #print('uname:',username)
                        date = split_data[3]
                        #print('date:',date)

                        tweet = re.sub(r"\n", " ", tweet)

                        all_tweets.append({'accountname':accountname,'username':username,'tweet': tweet,'date':date})
                verify_tweet_list = tweet_list
                pyautogui.scroll(-1500)
                time.sleep(0.3)
                pyautogui.scroll(-1000)
                time.sleep(1)
                if tweet_list == verify_tweet_list:
                    if end_count == 10:
                        all_time = time.time()
                    end_count = end_count + 1
            except:
                pyautogui.scroll(-1500)
                time.sleep(0.3)
                pyautogui.scroll(-1000)
                time.sleep(1)
                if end_count == 10:
                    all_time = time.time()
                end_count = end_count + 1
                continue
        

        if all_tweets != []:
            swr = 0 
            df_tweets = pd.DataFrame(all_tweets)
            output_filename = f'tweets_{self.word}_id_{since}_{until}.csv'
            df_tweets.to_csv(output_filename, index=False)
            print(f"Data saved to {output_filename} , length:{len(all_tweets)}")

        elif all_tweets == []:
            if swr > 4:
                self.driver.quit() 
            swr = swr + 1    
    
    def quit(self):
        # Close the browser
        self.driver.quit()
    
    def main(self):
        self.open_web()
        
        self.open_twitter()
        
        self.login()
        
        self.get_tweets(self.limit_time)
        
        self.quit()
        

