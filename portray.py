# encoding: utf-8
import time
import os
#import virtkey
from pykeyboard import PyKeyboard
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import sys

if len(sys.argv) < 2:
	print("[Error] please enter a search url")
	sys.exit(0)
searchurl = sys.argv[1]
wb_data = requests.get(searchurl)
soup = BeautifulSoup(wb_data.text, 'lxml')

#获取每集的图片url和名称
imgs = soup.select('body > div.main > div.boxs > ul > li > a > img')
name = list()
url = list()
count = 0
for i in imgs:
    #if count <= 5:#to skip some albums
    #    count+=1
    #    continue
    count+=1
    url.append(i.get('src').replace('0.','{}.'))
    name.append(i.get('alt'))
#获取每集张数
numlist = soup.select('body > div.main > div.boxs > ul > li > p:nth-of-type(1)')
num = list()
count = 0
for i in numlist:
    #if count <= 5:#to skip some albums
    #    count+=1
    #    continue
    count+=1
    num.append(i.text.split(' ')[1])
print(num)
print(url)

#create directories
path="/home/wjh/Downloads/"
for i in range(len(url)):
	os.mkdir(path+str(i))

print('Please wait...Firefox loading...')
print('---------------------------------')
driver = webdriver.Firefox()
k = PyKeyboard()
for c in range(0,len(num),1):
	
	for i in range(1, int(num[c])+1, 1):

		urll = ("https://www.meitulu.com/img.html?img="+url[c]).format(str(i))
		attempt = 0
		while True:
			try:	
				driver.get(urll)
			except TimeoutException:
				k.tap_key(k.function_keys[5])
				time.sleep(5)
				if attempt < 5:
					continue
			break
		element = driver.find_element_by_id('img').find_element_by_tag_name('img')
		img_url = element.get_attribute('src')
		action = ActionChains(driver).move_to_element(element).context_click(element).perform()
		time.sleep(1)
		k.tap_key("v")
		time.sleep(1)
		k.tap_key(k.enter_key) #Enter
		time.sleep(1)
	os.system("mv ~/Downloads/*.jpg ~/Downloads/"+str(c))
driver.close()

