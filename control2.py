# -*- coding: utf-8 -*-

from invents import invents
import time
from variables import *
inn=invents()



from splinter import Browser


count=0

def reguster():
	browser = Browser()
	inn.generate()
	
	browser.visit('http://hh.ru/auth/employer')
	
	browser.fill('companyName', inn.generate_work_place(1982)['company'])
	browser.fill('firstName', inn.FirstName)
	browser.fill('lastName', inn.LastName)
	browser.fill('email', inn.MailAddress+'@arterp.ru')
	
	browser.fill('phoneCode', inn.phone_code)
	browser.fill('phoneNumber', inn.phone)
	
	time.sleep(3)
	browser.find_by_xpath('//*[starts-with(@class,"HH-Form-SubmitButton")]').first.click()
	
	time.sleep(5)
	browser.find_by_xpath('//*[starts-with(@class,"g-button m-button_mid")]').first.click()
	
	#count=count+1
	#print count
	browser.quit()

#reguster()

#for i in range(30):
#	print i
#	reguster()
#print inn.Passwd


def post_resume(login, passw, sity):
	sity=unicode(sity)
	browser = Browser(user_agent=useragent)
	browser.visit('http://hh.ru/auth/employer')
	
	browser.fill('username', login)
	browser.fill('password', passw)
	
	time.sleep(1)
	browser.find_by_xpath('//*[starts-with(@class,"HH-SimpleValidation-Submit")]').first.click()
	time.sleep(3)
	#browser.click_link_by_href('hh.ru/employer/vacancy.do')
	#browser.visit('http://hh.ru/employer/vacancy.do')
	browser.find_by_xpath('//*[starts-with(@href,"/employer/vacancy.do")]').first.click()
	
	time.sleep(3)
	try:
		browser.find_by_xpath('//*[starts-with(@class,"newpopup__button")]').first.click()
		browser.find_by_xpath('//*[starts-with(@class,"newpopup__closeable")]').first.click()
	except:
		pass

	v_name=u'Стажер-разработчик Python (OpenERP)'
	v_desc=u"""
	Обязанности:

	    Программирование OpenERP
	
	
	Требования:
	
	    Опыт работы с Python, Опыт работы с реляционными СУБД
	
	
	Условия:
		Удаленное обучение.
	    Работа постоянная, удаленная, сдельная.
	    Для стажера сумма вознаграждения по результатам собеседования..
	
	
	Подробнее
	http://arterp.ru/vacancy-openerp-trainee/

	"""
	browser.fill('name', v_name)
	browser.fill('areaName', sity)
	
	browser.choose('scheduleId', '3')
	browser.choose('employmentId', '1')
	
	browser.find_by_xpath('//*[starts-with(@class,"b-forma-text")]').first.select("1")
	browser.find_by_id('HH-specializationChooser-checkbox_50').first.check()
	#Stage
	browser.find_by_id('HH-specializationChooser-checkbox_172').first.check()
	
	
	frame=browser.find_by_xpath('//*[starts-with(@class,"jsxComponents-Editor-Frame")]')[0]
	
	print frame.value
	print frame['class']
	
	#frame.type('type', 'typing text')
	#with browser.get_iframe(frame_name) as iframe:
	#frame.find_by_tag('html')[0].value
	
	#.first.fill('gggg')
		#iframe.find_by_xpath('//span[@class="hAa Qo Bg"]').first.click()
	#print browser.find_by_name('description').first.visible
	#browser.find_by_name('description').first.fill('dddss')

	
#post_resume('yaroslav.odintsov309@arterp.ru', 'Cj5yzG', u'Сарапул')

index=16

post_resume(hh_users[index][0], hh_users[index][1], sity_full[index])

#print len(sity_full)	