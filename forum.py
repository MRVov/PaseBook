# -*- coding: utf-8 -*-
import random
import time
from invents import invents
from splinter import Browser

def startz():
	inn=invents()
	inn.generate()
	
	browser = Browser()
	#browser.driver.set_window_size(150, 150)
	browser.visit('http://forum.xxx.ru/ucp.php?mode=register')
	browser.find_by_id('agreed').first.click()
	#browser.find_by_id('username').inn.MailAddress
	browser.fill('username', inn.MailAddress)
	browser.fill('email', inn.MailAddress+'@mail.ru')
	browser.fill('email_confirm', inn.MailAddress+'@mail.ru')
	browser.fill('new_password', 'plitko')
	browser.fill('password_confirm', 'plitko')
	browser.find_by_name('submit').first.click()
	
	browser.visit('http://forum.xxx.ru/ucp.php?i=173')
	browser.fill('username', inn.MailAddress)
	browser.fill('password', 'plitko')
	browser.find_by_name('login').first.click()
	
	browser.visit('http://forum.xxx.ru/ucp.php?i=173')
	#browser.fill('location', inn.generate_residence().lower())
	#time.sleep(10)
	browser.select('bday_day', inn._BirthDay)
	browser.select('bday_month', inn.BirthMonth3)
	print inn.BirthMonth3
	browser.select('bday_year', str(inn.BirthYear))
	browser.find_by_name('submit').first.click()
	
	print inn.MailAddress
	
	for z in range (1,random.randint(130, 255)):
		browser.visit('http://forum.xxx.ru/posting.php?mode=reply&f=3&t=2')
		browser.fill('message', 'mmm')
		time.sleep(1)
		browser.find_by_name('post').first.click()
		
		#time.sleep(5)

	browser.quit()

#startz()	
for i in range(1, 1000):
	print i
	startz()





