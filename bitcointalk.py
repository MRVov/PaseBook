# -*- coding: utf-8 -*-

import random
import time
from invents import invents
from splinter import Browser
from tools import *
import urllib2
import threading

users_arr=[
	('user', 'pass'),

		]

def _login(user_index):
	print 'Wait 45 sec for logon'
	time.sleep(47)
	browser = Browser()
	
	login=users_arr[user_index][0]
	passw=users_arr[user_index][1]
	print 'Login for user %s' % login
	
	browser.visit('https://bitcointalk.org/index.php?action=login')
	browser.find_by_name('user').last.fill(login)
	browser.find_by_name('passwrd').last.fill(passw)
	browser.find_by_name('cookielength').last.fill('600')
	
	browser.find_by_xpath('//input[@value="Login"]').last.click()
	
	return browser
	
def _register(domain='gmail.com'):
	browser = Browser()
	inn=invents()
	inn.generate()
	
	browser.visit('https://bitcointalk.org/index.php?action=register')
	browser.find_by_name('user').last.fill(inn.MailAddress)
	
	browser.fill('email', inn.MailAddress+'@'+domain)
	browser.fill('passwrd1', inn.Passwd)
	browser.fill('passwrd2', inn.Passwd)
	
	url=browser.find_by_id('verificiation_image').first['src']
	url=url.replace('mycode=2;','mycode=4;')
	#print url
	
	PHPSESSID=browser.cookies['PHPSESSID']
	
	cook='PHPSESSID=%s' % PHPSESSID
	cap=recognize_captcha(url, cook=cook)
	#print cap
	browser.fill('visual_verification_code', cap)
	browser.find_by_name('regSubmit').first.click()
	
	if browser.title.find('Error')>=0:
		print 'Eror= %s' % browser.title
	else:
		print "('%s', '%s')" % (inn.MailAddress, inn.Passwd)
		time.sleep(30)
	
	browser.quit()
		
def visit(browser, post_id):
	browser.visit('https://bitcointalk.org/index.php?topic=%d' % post_id)
	
def _post_topic(browser, url, text):
	print 'Post for topic url=%s text=%s' % (url, text)
	
	browser.visit(url)
	browser.find_link_by_partial_href('index.php?action=post;').last.click()
	browser.fill('message', text)
	browser.find_by_name('post').first.click()
	
def _repost_topic(browser, url, text):
	print 'RePost for topic url=%s text=%s' % (url, text)
	off_start=url.find('#msg')

	mess_id=int(url[off_start+4:])
	
	browser.visit(url)
		
	browser.find_link_by_partial_href(';quote=%d;' % mess_id).last.click()
	txt_field=browser.find_by_name('message').last
	
	print txt_field.text
	txt=txt_field.text
	txt+='\r\n'
	txt+=text

	browser.fill('message', txt)
	
	browser.find_by_name('post').first.click()
	
def post(browser, url, text):
	text=unicode(text)
	walk(browser, 6)
	
	if url.find('#msg')>0:
		_repost_topic(browser, url, text)
	else:
		_post_topic(browser, url, text)
			
def walk(browser, minutes):
	print 'Go walk for %d minutes' % minutes
	for i in range(minutes):
		visit(browser, 454960)
		time.sleep(30)
		visit(browser, 449223)
		time.sleep(30)

def intel_forum_time(browser):
	walk(browser, 248)
		
def intel_full_dummy(browser):
	for i in range(4):
		f_arr=['я123',
			'я321',
			'Привет',
			'Хелоу',
			'Бунжур',
			'qwerty',
			'я был здесь',
			'я тоже был здесь',
			'и я был',
			
			]
		mess=random.choice(f_arr)
		post(browser, 'https://bitcointalk.org/index.php?topic=449223.60', mess)
		
def bee():	
	for i in range(4, 400):
		browser=_login(i)
		
		try:
			intel_full_dummy(browser)
		except:
			print 'error'
			
		try:
			intel_forum_time(browser)
		except:
			print 'error2'
			
		print 'Yo dawg so i heard you like'
		browser.quit()
		
browser=_login(1)
post(browser, 'https://bitcointalk.org/index.php?topic=449223.msg4957075#msg4957075', 'Передомной явилась ты?')

#def bath_register(qty=100):
#	for i in range(qty):	
#		_register()

#forum_time(0)