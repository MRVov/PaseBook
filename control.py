# -*- coding: utf-8 -*-

#http://splinter.cobrateam.info/docs/
#http://pydoc.net/Python/grab/0.3.9/grab.transport.splinter/
#https://github.com/cobrateam/splinter/blob/master/splinter/driver/zopetestbrowser.py
#FirefoxProfile profile = new FirefoxProfile();
#profile.setPreference("general.useragent.override", "Googlebot/2.1+http://www.googlebot.com/bot.html)"); 

#http://selenium-python.readthedocs.org/en/latest/api.html

from splinter import Browser
from variables import *
from tools import *

import time
#http://stackoverflow.com/questions/13227346/set-chrome-options-with-remote-driver
#http://stackoverflow.com/questions/15165593/set-chrome-prefs-with-python-binding-for-selenium-in-chromedriver?rq=1
class control_google():
	
	def init_browser(self, email, passwd):
		self.state='good'
		self.passwd=passwd
		self.login=email
	
		
		param={
'chrome.noWebsiteTestingDefaults': True,
'chrome.prefs': {
'profile.default_content_settings': {
'images': 2
        },
         }
    	}
		from selenium.webdriver.chrome.options import Options
		options = Options()

		#options.add_argument('--allow-running-insecure-content')
		#options.add_argument('--disable-web-security')
		#options.add_argument('--disk-cache-dir=/var/www/cake2.2.4/app/tmp/cache/selenium-chrome-cache')
		#options.add_argument('--no-referrers')
		#options.add_argument('--window-size=1003,719')
		#options.add_argument('--proxy-server=localhost:8118')
		options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")
		
		
		CHROME = {
		"browserName": "chrome",

        "chrome.prefs": {"profile.managed_default_content_settings.images": 2},
        "chrome.switches": ["disable-images"],
      

        }


		self.browser = Browser('chrome', user_agent=useragent)
		#self.browser = Browser('chrome', user_agent=useragent, desired_capabilities=CHROME)
		
		load_page='https://accounts.google.com/ServiceLogin?btmpl=mobile_tier2&hl=ru&service=mobile'
		self.browser.visit(load_page)
		
		self.browser.find_by_id('Email').first.fill( email+'@gmail.com')
		self.browser.find_by_id('Passwd').first.fill(passwd)
		
		self.browser.find_by_id('signIn').first.click()
		
	def _google_hook(self):
		if self.browser.is_element_present_by_id('358'):
			self.browser.find_by_id('358').first.click()
			
		if self.browser.is_element_present_by_id('link_dismiss'):
			try:
				self.browser.find_by_id('link_dismiss').first.click()
			except:
				pass

		if 'getstarted' in self.browser.url:
			self.browser.back()
			
		if self.browser.is_element_present_by_id('link_dismiss'):
			self.browser.find_by_id('link_dismiss').first.click()
						
	def open_profile(self):
		print 'Open light version profile'
		load_page='https://plus.google.com/app/basic/%s/about' % self.profile_id
		self.browser.visit(load_page)
		
	def save_profile(self):
		self.browser.find_by_id('177').first.click()
		
	def register_google_plus(self, firstName, lastName):
		load_page='https://plus.google.com/u/0/?gpsrc=ogpy0&tab=XX'
		self.browser.visit(load_page)
		
		self.browser.fill('firstName', firstName)
		self.browser.fill('lastName', lastName)
		
		self.browser.find_by_name('buttonPressed').first.click()
		
		self.browser.find_by_id('357').first.click()
		
	def get_profile_id(self):
		load_page='https://www.google.com/settings/general-light?ref=/settings/account'
		self.browser.visit(load_page)
		if self.browser.is_element_present_by_xpath('//a[@class="CS"]'):
			profile_link=self.browser.find_by_xpath('//a[@class="CS"]').first
			link_path=profile_link['href']
		
			return link_path.split('/')[3]
		else:
			return False
		
	def profile_edit(self, vals):
		self.open_profile()
		
		print 'Click change profile'
		self.browser.find_by_id('59').first.click()
		
		#Confirm mobile rules
		self._google_hook()
			
		self.browser.find_by_name('peWork0').first.fill(vals['company'])
		self.browser.find_by_name('peWorkTitle0').first.fill(vals['position'])
		self.browser.find_by_name('peWorkStartYear0').first.fill(vals['year_start'])
		self.browser.find_by_name('peWorkEndYear0').first.fill(vals['year_stop'])
		
		self.browser.find_by_name('peSchool0').first.fill(vals['university_name'])
		self.browser.find_by_name('peSchoolMajor0').first.fill(vals['field_education_name'])
		self.browser.find_by_name('peSchoolStartYear0').first.fill(vals['going_to_college_year'])
		self.browser.find_by_name('peSchoolEndYear0').first.fill(vals['after_graduation_year'])
		
		self.browser.find_by_name('pePlaceLived0').first.fill(vals['place_lived'])
		
		self.browser.find_by_name('pePlaceLivedIsCurrent').first.check()
		
		self.browser.find_by_name('peGender').first.select("1")
				
		print 'Done profile_edit'
		
		self.save_profile()
		
	def change_photo(self, photo_path):
		self.open_profile()
		
		print 'Click change profile'
		self.browser.find_by_id('59').first.click()

		print 'Click change photo'
		self.browser.find_by_id('375').first.click()
		
		self.browser.attach_file('photo_upload_file_name', self.photo_path)
		print 'Done profile_edit'
		
		self.browser.find_by_id('314').first.click()
		
		self.save_profile()
		
	def change_pass(self, old_pass, new_pass):
		print 'Open password  change page'
		load_page='https://accounts.google.com/b/0/EditPasswd?hl=ru'
		self.browser.visit(load_page)
		
		self.browser.find_by_id('OldPasswd').first.fill(old_pass)
		self.browser.find_by_id('Passwd').first.fill(new_pass)
		self.browser.find_by_id('PasswdAgain').first.fill(new_pass)
		
		self.browser.find_by_id('save').first.click()
		print 'Done change pass'
		
	def open_full_plus(self):
		'Print open full Google+'
		load_page='https://plus.google.com/u/0/'
		self.browser.visit(load_page)
		

	def open_full_profile(self):
		self.open_full_plus()
		self._google_hook()

		print 'Click user icon'
		self.browser.find_by_id('gbi4i').first.click()
		
		print 'Click show profile'
		#self.browser.find_by_id('gbmplp').first.click()
		self.browser.find_by_xpath('//a[@class="gbqfb gbiba gbp1"]').first.click()
		
		
	def change_name(self, firstName, lastName):
		self.open_full_plus()
		self.open_full_profile()
		
		print 'Click change name'
		time.sleep(5)
		self.browser.find_by_xpath('//div[@guidedhelpid="profile_name"]').first.click()
		
		print 'Fill values'
		time.sleep(5)
		self.browser.find_by_xpath('//input[@class="l-pR osa g-A-G"]').first.fill(firstName)
		self.browser.find_by_xpath('//input[@class="l-oR Ika g-A-G"]').first.fill(lastName)

		print 'Save results'
		self.browser.find_by_xpath('//*[starts-with(@class,"a-f-e c-b c-b-M nVrMHf nZQKMd h019o")]').first.click()
		
		print 'Confirm'
		self.browser.find_by_name('ok').first.click()
		
	def youtube_hoock(self):
		if 'ServiceLogin?' in self.browser.url:
			print 'ServiceLogin? Hook'
			self.browser.fill('Passwd', self.passwd)
			self.browser.find_by_name('signIn').first.click()
			#self.browser.back()
			
		if 'create_channel?' in self.browser.url:
			print 'create_channel? Hook'
			self.browser.click_link_by_partial_href('create_channel')
			self.browser.fill('username', self.login)
			self.browser.find_by_id('channel_submit').click()
			self.browser.back()
			self.browser.back()
			self.browser.back()
			
		if 'select_site?' in self.browser.url:
			print 'select_site? Hook'
			self.browser.find_by_xpath('//input[@type="submit"]').click()
			self.browser.back()
			self.browser.back()
			
		if 'switch-profile.g?' in self.browser.url:
			print 'switch-profile.g? Hook'
			self.browser.find_by_id('switchButton').click()
			
			
	def youtube_like(self, url):
		self.browser.visit(url)
		self.browser.click_link_by_partial_href('action_like=1')
		
		self.youtube_hoock(url)
		
		self.browser.find_by_name('action_rate').click()
		
	def youtube_dislike(self, url):
		self.browser.visit(url)
		self.browser.click_link_by_partial_href('action_dislike=1')
		
		self.youtube_hoock()
		
		self.browser.find_by_name('action_rate').click()
		
	def youtube_comment(self, url, comment):
		self.browser.visit(url)

		self.browser.click_link_by_partial_href('post_comment')
		
		self.youtube_hoock()
		try:
			self.browser.click_link_by_partial_href('post_comment')
		except:
			pass
		
		self.youtube_hoock()
		self.browser.fill('comment', comment)
		self.browser.find_by_name('action_comment').click()
		
		self.youtube_hoock()
	def youtube_subscribe(self, chane_name):
		load_page='http://m.youtube.com/user/%s' % chane_name
		self.browser.visit(load_page)
		

		self.browser.find_by_name('submit')[1].click()

		self.youtube_hoock()
		
		try:
			self.browser.find_by_name('submit')[1].click()
		except:
			pass
		
	def google_friend_connector(self):
		#self.browser.click_link_by_partial_href('post_comment')
		pass
	def blogspot_follow(self, url):
		pass
	
	def get_capture(self):
		cap_element=self.browser.find_by_xpath('//img[@width="300"]').first
		cap_code=recognize_captcha(cap_element['src'])
		self.browser.fill('recaptcha_response_field', cap_code)
		
	def blogspot_post_plus(self, url):
		self.browser.visit(url)
		frame_name=self.browser.find_by_xpath('//*[starts-with(@name,"I0_")]')[0]['name']
		print frame_name
		with self.browser.get_iframe(frame_name) as iframe:
		#	#self.browser.find_by_xpath('//span[@class="hAa Qo Bg"]').first.click()
			iframe.find_by_xpath('//span[@class="hAa Qo Bg"]').first.click()
			
	def blogspot_post(self, url, comment):
		self.browser.visit(url)
		
		with self.browser.get_iframe('comment-editor') as iframe:
			self.browser.fill('commentBody', comment)
			iframe.find_by_id('postCommentSubmit').click()
			self.youtube_hoock()
			
		with self.browser.get_iframe('comment-editor') as iframe:	
			if iframe.is_element_present_by_id('recaptcha_image'):
				self.get_capture()
				iframe.find_by_id('postCommentSubmit').click()	
				
		if 'showComment=' in self.browser.url:
			return True
		else:
			return False
		
	def google_post_like(self, url):
		self.browser.visit(url)
		
		if not self.browser.is_element_present_by_name('stupop'):
			self.browser.find_by_id('162').click()
			return True
		else:
			return False
			
	def google_post_dislike(self, url):
		self.browser.visit(url)
		
		if self.browser.is_element_present_by_name('stupop'):
			self.browser.find_by_id('162').click()
			return True
		else:
			return False
		
	def google_post_comment(self, url, comment):
		self.browser.visit(url)
		
		self.browser.fill('adcp', comment)
		self.browser.find_by_id('110').click()
		
	def google_post_share(self, url, comment):
		self.browser.visit(url)
		
		self.browser.find_by_id('396').click()
		self.browser.fill('rpPostMsg', comment)
		self.browser.find_by_id('253').click()
	
	def google_profile_join(self, id):
		self.browser.visit('https://plus.google.com/app/basic/%s/' % id)
		
		self.browser.find_by_id('59').click()
		self.circle_join()
		
	def circle_join(self):
		self.browser.find_by_name('chcccp')[3].click()
		self.browser.find_by_id('49').click()
		self.browser.reload()
		
	def google_communities_enter(self, id):
		self.browser.visit('https://plus.google.com/u/0/communities/%s/' % id)
		self._google_hook()
		
	def google_communities_join(self, id):
		self.google_communities_enter(id)
		
		if self.browser.is_element_present_by_xpath('//*[starts-with(@class,"a-f-e c-b c-b-La")]'):
			self.browser.find_by_xpath('//*[starts-with(@class,"a-f-e c-b c-b-La")]').first.click()
		
	def google_communities_post(self, id, mess):
		print 'Start  communities post'
		self.google_communities_join(id)
		time.sleep(60)
		#for i in self.browser.find_by_xpath('//a[@class="FW9qdb Wk"]'):
		#`	print i['oid']
		
		#self.browser.reload()
		self.browser.find_by_xpath('//div[@guidedhelpid="sharebox_textarea"]').first.click()
		self.browser.find_by_xpath('//div[@class="yd editable"]').first.fill(mess)
		self.browser.find_by_xpath('//div[@guidedhelpid="sharebutton"]').click()		
		time.sleep(60)
		self.browser.find_by_xpath('//div[@class="a-n Ph Hw"]').first.click()
		print '-'*30
		for i in self.browser.find_by_xpath('//a[@class="FW9qdb Wk"]'):
			print i['oid']
	def google_people_suggested(self):
		self.browser.visit('https://plus.google.com/app/basic/people/suggested?')
		for i in range(10):
			try:
				self.browser.find_by_xpath('//a[@class="vfc"]').first.click()
				self.circle_join()
			except:
				self.browser.visit('https://plus.google.com/app/basic/people/suggested?')
				
	def google_grab_comm_members(self, id, qty):
		irr_qty=int((qty-64)/20.00)+3
		print 'Irr qty= %d' % irr_qty
		
		self.browser.visit('https://plus.google.com/u/0/communities/%s/members' % id)
		ret_arr=[]
		
		js_del_all_img="""
		var images = document.getElementsByTagName('img');
			while(images.length > 0) 
			{
    		images[0].parentNode.removeChild(images[0]);
			}
		"""

		
		for i in range(irr_qty):
			elem_arr=self.browser.find_by_xpath('//div[@class="ib31if"]')
			print 'Array len %d' % len(elem_arr)
			print i
			print ''
			elem_arr[len(elem_arr)-2].right_click()
			#self.browser.execute_script(js_del_all_img)
			for elem in elem_arr:
				oid=elem['oid']
				img=self.browser.find_by_xpath('//img[@oid="%s"]' % oid)[0]
				#print img['src']
				
				if not oid in ret_arr:
					ret_arr.append(oid)
					print oid
				
		f = open('/tmp/google_oid.txt', 'w')
		for s in ret_arr:
			f.write('<item>'+ s + '</item>\n')
		f.close()
		print 'Grab done'
		
	def quit(self):
		self.browser.quit()