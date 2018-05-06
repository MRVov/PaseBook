from invents import invents
import time
from tools import *
from model import model

inn=invents()
md=model()

#http://pinger.com/tfw/	
class google_register():
	def __init__(self):
		self.browser = Browser('chrome', user_agent=useragent)
		
	def register(self, vals, captcha=True):	
		load_page='https://accounts.google.com/SignUp?hl=ru'
		self.browser.visit(load_page)

		self.browser.fill('FirstName', vals.FirstName)
		#browser.wk_fill
		self.browser.fill('LastName', vals.LastName)
		
		self.browser.fill('GmailAddress', vals.MailAddress)
		
		self.browser.fill('Passwd', vals.Passwd)
		self.browser.fill('PasswdAgain', vals.Passwd)
		

		self.browser.fill('BirthDay', vals.BirthDay)

		self.browser.find_by_id('month-label').first.click()
		self.browser.find_by_id(':'+vals.BirthMonth2).first.click()
		
		self.browser.fill('BirthYear', vals.BirthYear)
		
		self.browser.find_by_id('Gender').first.click()
		
		if vals.Gender:
			self.browser.find_by_id(':d').first.click()
		else:
			self.browser.find_by_id(':c').first.click()
			
		self.browser.fill('RecoveryPhoneNumber', self.get_phone())
		
		if captcha:
			cap_element=self.browser.find_by_xpath('//img[@width="300"]').first
			cap_code=recognize_captcha(cap_element['src'])
			self.browser.fill('recaptcha_response_field', cap_code)
		else:
			self.browser.find_by_id('SkipCaptcha').first.check()
					
		self.browser.find_by_id('TermsOfService').first.check()
		
		self.browser.find_by_id('submitbutton').first.click()
		
		self.browser.find_by_id('next-button').first.click()
		
		self.browser.fill('smsUserPin', self.get_phone_pin())
		self.browser.find_by_name('VerifyPhone').first.click()
		
		self.browser.find_by_xpath('//div[@class="a-f-e c-b c-b-M ZQb fMa"]').first.click()

	def get_phone_pin(self):
		return raw_input("Input phone PIN ") 	
	
	def get_phone(self):
		#phone='+1 (661) 728-1795'
		phone=raw_input("Input phone number ")   
		#phone=input("Input phone number")
		self.phone=phone
		return phone
	


def intelb():
	
	inn.generate()
	
	print inn.FirstName
	print inn.LastName
	print inn.MailAddress
	print inn.Passwd
	
	#return 0
	gr=google_register()
	gr.register(inn, captcha=False)
	
	#md.add_user(inn.MailAddress)
		
	#md.set_user_pass(inn.MailAddress, inn.Passwd)
	#md.set_birth(inn.MailAddress, inn.BirthYear,  inn.BirthMonth, inn.BirthYear)
	#md.set_phone(inn.MailAddress, gr.phone)
		
	#md.set_xml_attr(inn.MailAddress, 'first_name', inn.FirstName)
	#md.set_xml_attr(inn.MailAddress, 'last_name', inn.LastName)