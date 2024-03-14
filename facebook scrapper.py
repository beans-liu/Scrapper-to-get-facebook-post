from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
driver.get('https://www.facebook.com')
#登入
email = driver.find_element(by=By.ID, value="email")
password = driver.find_element(by=By.ID, value="pass")

email.send_keys('')  #輸入帳號
password.send_keys('') #輸入密碼

login_btn = driver.find_element(by=By.NAME, value='login')
login_btn.click()
time.sleep(2)

# //*[@id="mount_0_0_ie"]/div/div[1]/div/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div
# /html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div
def scroll_down(num):
    next_post_container = driver.find_element(By.XPATH, f'//div[@aria-posinset="{num+1}"]')
    # next_post_container = driver.find_element(By.XPATH, '//*[contains(@aria-posinset)]')
    # next_post_container = driver.find_element(By.CSS_SELECTOR, f'div[aria-posinset="{num+1}"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", next_post_container)
    time.sleep(random.uniform(5, 10)) 

def get_post_content(post_element):
    try:
        button = post_element.find_element(By.XPATH, './/ancestor::div[contains(text(), "查看更多")]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(random.uniform(5, 10))
    except NoSuchElementException:
        pass

    text = post_element.text.strip()
    return text

def get_class_name():

  div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[style*='text-align: start']"))
  )

  parent_span = div.find_element(By.XPATH, './ancestor::span')
  return parent_span.get_attribute('class')

def get_likes_number(element,likes_btn_class,close_btn_class):
    try:
        likes_btn = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.XPATH, f".//div[contains(@class,'{likes_btn_class}')]")))
        driver.execute_script("arguments[0].click();", likes_btn)
        time.sleep(3)
        like=driver.find_element(By.XPATH,"//*[contains(@aria-label,'全部,')]")
        like_class = like.get_attribute('class')
        likes = driver.find_elements(By.XPATH, f"//*[@class='{like_class}']")
        like_list={}
        for i in likes:
            it=i.get_attribute('aria-label')
            if it == None:
                continue
            parts = it.split(', ')
            key = parts[0]
            value = parts[1]
            like_list[key] = value
        time.sleep(2)

        close_btn = element.find_element(By.XPATH,f"//*[@class='{close_btn_class}']")
        action = ActionChains(driver)
        action.move_to_element(close_btn).click().perform()
        return like_list
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_likes_number_first(element,likes_btn_class):
    try:
        likes_btn = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.XPATH, f".//div[contains(@class,'{likes_btn_class}')]")))
        driver.execute_script("arguments[0].click();", likes_btn)
        time.sleep(3)
        like=driver.find_element(By.XPATH,"//*[contains(@aria-label,'全部,')]")
        like_class = like.get_attribute('class')
        likes = driver.find_elements(By.XPATH, f"//*[@class='{like_class}']")
        like_list={}
        for i in likes:
            it=i.get_attribute('aria-label')
            if it == None:
                continue
            parts = it.split(', ')
            key = parts[0]
            value = parts[1]
            like_list[key] = value
        time.sleep(2)

        close_btn = WebDriverWait(element, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, '關閉')]"))
        )
        key='close_btn'
        value=close_btn.get_attribute('class')
        time.sleep(random.uniform(1,3))
        driver.execute_script("arguments[0].click();", close_btn)
        like_list[key]=value
        return like_list
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_likes_class(element):
        target_like = WebDriverWait(element, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, '看看誰對這個傳達了心情')]"))
        )
        like_area = target_like.find_element(By.XPATH,'./../..')
        like_area_class = like_area.get_attribute('class')
        all_likes = WebDriverWait(target_like, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '所有心情')]"))
        )
        
        likes_btn = WebDriverWait(all_likes, 10).until(EC.element_to_be_clickable((By.XPATH, "./..")))
        likes_btn_class = likes_btn.get_attribute('class')
        return {'likes_btn':likes_btn_class,'like_area':like_area_class}

def get_comments_shares(post_container):
  comments = post_container.find_element(By.XPATH, ".//*[contains(text(), '則留言')]")
  shares = post_container.find_element(By.XPATH, ".//*[contains(text(), '次分享')]")
  number = comments.get_attribute('innerText')
  snumber = shares.get_attribute('innerText')
  
  return {'comment_number':number[:-3],'share_number':snumber[:-3]}

def get_postid(post_container, url):
    try:
        date_urls = post_container.find_element(By.XPATH, f'.//a[contains(@href,"https://www.facebook.com/{url}/posts")]')
        temp_p = date_urls.get_attribute('href')
        temp_p = temp_p.split('?__cft')[0]
        post_id = temp_p.split("/posts/")[1]
        return {'post_id': post_id}
    except NoSuchElementException:
        return {'post_id':"no post_id"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_post(url, post_number):

  driver.get(url)
  time.sleep(5)

  crawled_posts = set()
  post_list = []
  # post_container = driver.find_element(By.XPATH, f'//div[@aria-posinset="1"]')
  # likes_dic = get_likes_class(post_container)
  num = 1 #1
  url_name = url[25:]
  while len(post_list) < post_number:

    try:
      post_container = driver.find_element(By.XPATH, f'//div[@aria-posinset="{num}"]')
      # post_container = driver.find_element(By.XPATH, '//*[@id="mount_0_0_Pz"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div')
      if num == 1: #1
         c_name = get_class_name()
      post_element = post_container.find_element(By.XPATH, f".//span[@class = '{c_name}']")
      post_id = get_postid(post_container, url_name)
      text = get_post_content(post_element)
      comments_shares = get_comments_shares(post_container)

      # if num == 1: #1
      #   try:
      #     temp_like = get_likes_number_first(post_container,likes_dic['likes_btn'])
      #     likes_number = dict(list(temp_like.items())[:-1])
      #   except:
      #      pass
      # else:
      #   likes_number = get_likes_number(post_container,likes_dic['likes_btn'],temp_like['close_btn'])
      if text not in crawled_posts:
        crawled_posts.add(text)
        post_dict = {'index': len(post_list)+1, 'target': url_name, 'text': text}
        post_dict.update(comments_shares)
        # post_dict.update(likes_number)
        post_dict.update(post_id)
        print(post_dict)
        post_list.append(post_dict)

    except NoSuchElementException:
      print("no such element")
      pass

    print("next")
    scroll_down(num)
    num += 1

  return post_list

urls = ['https://www.facebook.com/dpptw','https://www.facebook.com/TPPfanpage', 'https://www.facebook.com/mykmt']
result = []
for url in urls:
    temp_r = get_post(url, 3)
    result.append(temp_r)

urls = ['https://www.facebook.com/TPPfanpage']
for url in urls:
    temp_r = get_post('https://www.facebook.com/TPPfanpage', 3)
    result.append(temp_r)

#輸出檔案
flat_list = [item for sublist in result for item in sublist]
df = pd.DataFrame(flat_list)
df.to_excel('output_party_2.xlsx', index=False)
#csv
flat_list = [item for sublist in result for item in sublist]
df = pd.DataFrame(flat_list) 
df.to_csv('output_party_2.csv', encoding='utf-8')
df = pd.read_csv('output_party_2.csv', encoding='utf-8')