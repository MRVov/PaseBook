# -*- coding: utf-8 -*-
from model import *
from invents import invents
from tools import *
from variables import *
from control import *
import time

inn=invents()
md=model()
mdt=md_task()

class intel_control(control_google):
	def init_task(self):
		
		if not mdt.get_task():
			print 'Not active task'
			return False
		
		if mdt.task_login:
			self.init_user(mdt.task_login)
		else:
			self.init_user(md.get_random_user())
			
		self.process_task(mdt.task_type, mdt.task_url, mdt.task_text)
		
	def process_task(self, type, url, comment):
		if mdt.task_comm_oid:
			self.google_communities_join(mdt.task_comm_oid)
			
		if type=='google_like':
			self.google_post_like(url)
		
		if type=='google_dislike':
			self.google_post_dislike(url)
		
		if type=='google_comment':
			self.google_post_comment(url, comment)
		
		if type=='google_share':
			self.google_post_share(url, comment)
		
		if type=='google_create_comm_post':
			self.google_communities_post(mdt.task_comm_oid, comment)
			
		if type=='youtube_like':
			self.youtube_like(url)
			
		if type=='youtube_dislike':
			self.youtube_dislike(url)
		
		if type=='youtube_comment':
			self.youtube_comment(url, comment)
		
		if type=='youtube_subscribe':
			self.youtube_subscribe('MrLemonPancakes')
		mdt.close_task(self.login)
		
	def init_user(self, login):
		def search_f():
			xml_photo_arr=md.get_photo_arr()
			
			for i in range(100):
				image=inn.get_image_name()
				if not(image in xml_photo_arr): return image
				
			print 'Photos ended'
			return ''
		
		password=md.get_xml_attr(login, 'password')
		self.init_browser(login, password)
		
		inn.generate()
		
		if not md.get_xml_attr(login, 'profile'):
			if not self.get_profile_id():
				self.register_google_plus(inn.FirstName, inn.LastName)
				
				md.set_xml_attr(login, 'first_name', inn.FirstName)
				md.set_xml_attr(login, 'last_name', inn.LastName)
	
			profile_id=self.get_profile_id()
			
			md.set_xml_attr(login, 'profile', profile_id)
			
		self.profile_id=md.get_xml_attr(login, 'profile')
		
		if not md.get_xml_attr(login, 'first_name'):
			self.change_name(inn.FirstName, inn.LastName)
			
			md.set_xml_attr(login, 'first_name', inn.FirstName)
			md.set_xml_attr(login, 'last_name', inn.LastName)
			
		if not md.get_xml_attr(login, 'birth_year'):
			BirthYear=inn.BirthYear
			vals=inn.generate_university(BirthYear)
			vals2=inn.generate_work_place(BirthYear)
		
			vals.update(vals2)
			vals['place_lived']=inn.generate_residence()
			
			self.profile_edit(vals)
			
			md.set_xml_attr(login, 'birth_year', str(BirthYear))
			
		if not md.get_xml_attr(login, 'photo'):
			file_name=search_f()
			if file_name:
				self.change_photo(inn.get_image_path()+file_name)
				md.set_xml_attr(login, 'photo', file_name)
			
		if len(password)<len_pass:
			new_passwd=inn.generate_pass()
			
			print 'Change passwd old password- %s' % new_passwd
			self.change_pass(password, new_passwd)
			
			md.set_xml_attr(login, 'password', new_passwd)
			print 'New passwd-%s' % new_passwd
			
		print 'User init done'
		#self.quit()
	
def parse_string(string):
	res=string.split(';')
	
	login=res[0].replace('@gmail.com', '')
	password=res[1]
	phone=res[4]
	
	print login
	print password
	print phone
	
	if md.user_exist(login):
		print 'Login-%s EXIST!!!' % login
		return 0
	
	md.add_user(login)
	md.set_user_pass(login, password)
	md.set_phone(login, phone)
	
	md.nailed_file()
	#intel_init(login)	
	


ic=intel_control()
ic.init_task()

		
