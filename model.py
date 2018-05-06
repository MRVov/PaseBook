# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime, timedelta
import random

from variables import *

class md_main():
	def save(self):
		handle = etree.tostring(self.tree, pretty_print=True, encoding='utf-8', xml_declaration=True)       
		applic =  open(self.file, "w")
		applic.writelines(handle)
		applic.close()
		self._nailed_file()
	def _nailed_file(self):
		fil = open(self.file,'r')
		contents = fil.read()
		replaced_contents = contents.replace('><', '>\r\n\r\n<')
		fil.close()
		
		fil = open(self.file,'w')
		fil.write(replaced_contents)
		fil.close()
		
	def append_to_root(self, et):
		user_branch = etree.tostring(et, pretty_print=True, encoding='utf-8', xml_declaration=True)
		
		root=self.tree.getroot()
		root.append(etree.XML(user_branch+'\r\n'))
		
		self.save()
		self._nailed_file()
		
class md_task(md_main):
	def __init__(self):
		self.file=xml_db_path+'tasks.xml'
		self.tree = etree.parse(self.file)
		self.active_item=None
		
	def create_task(self, url, type, task_arr=[], hours=24):
		task_branch= etree.Element("task")
		
		task_branch.set('hours', str(hours))
		task_branch.set('type', type)
		task_branch.set('url', url)
		task_branch.set('comm_oid', '')
		
				
		for i in task_arr:
			item=etree.Element("item")
			item.text=' '
			item.set('type', i)
			item.set('user', '')
			item.set('date', '')

			task_branch.append(item)
				
		self.append_to_root(task_branch)
		
	def get_task(self):
		self._reset_task_attr()
		
		res=self.tree.xpath("//item[@date='']")
		
		print 'Total dont slosed tasks %d' % len(res)
		for i in res:
			e_parent=i.getparent()
			
			hours=int(e_parent.get("hours"))
			
			time_now=datetime.now()
			
			time_last_arr=e_parent.xpath("(/item[@date!=''])[last()]")
			
			last_update_time=datetime(1977, 6, 5, 12, 10)

			if len(time_last_arr)>0:
				last_time_str=time_last_arr[0].get('date')
				last_update_time=datetime.strptime(last_time_str, date_format)
			
			print last_update_time.strftime(date_format)
			time_to_action=last_update_time+timedelta(hours=hours)
			print time_to_action.strftime(date_format)
			
			if len(time_last_arr)==0 or time_now>time_to_action:
				print 'Action time'
				self.task_type=e_parent.get("type")+'_'+i.get("type")
				self.task_url=e_parent.get("url")
				self.task_text=i.text
				self.task_login=i.get("user")
				self.task_comm_oid=e_parent.get("comm_oid")
				
				self.active_item=i
						
				return True
			
		self._reset_task_attr()
		return False
	
	def _reset_task_attr(self):
		self.task_url=''
		self.task_type=''
		self.task_text=''
		self.task_login=''
		self.task_comm_oid=''
		
	def close_task(self, login, url=None):
		self._reset_task_attr()
		
		s_now=datetime.now().strftime(date_format)
		
		if self.active_item is not None:
			self.active_item.set('date', s_now)
			self.active_item.set('user', login)

			if url:
				parent=self.active_item.getparent()
				parent.set('url', url)
				
			self.save()
			self.active_item=None	
			
		else:
			print 'ERROR Active item not found'
		
class model(md_main):
	def __init__(self):
		self.file=xml_db_path+'google.xml'
		self.tree = etree.parse(self.file)

	def add_user(self, login):
		user_branch= etree.Element("user", login=login)
		
		user_branch.append(etree.Element("password"))
		user_branch.append(etree.Element("email"))
		user_branch.append(etree.Element("phone"))
		user_branch.append(etree.Element("profile"))
		user_branch.append(etree.Element("photo"))
		user_branch.append(etree.Element("birth_day"))
		user_branch.append(etree.Element("birth_month"))
		user_branch.append(etree.Element("birth_year"))
		
		user_branch.append(etree.Element("first_name"))
		user_branch.append(etree.Element("last_name"))
		
		self.append_to_root(user_branch)

	def set_xml_attr(self, login, attr, val):
		search_string="//user[@login='%s']/%s" % (login, attr)
		
		res=self.tree.xpath(search_string)

		if len(res)==0:
			return -1
		else:
			res[0].text=val
			self.save()
			return 0
		
	def get_xml_attr(self, login, attr):
		search_string="//user[@login='%s']/%s" % (login, attr)
		
		res=self.tree.xpath(search_string)

		if len(res)==0:
			return False
		else:
			return res[0].text


	def get_profile_path(self, login):
		return self.get_xml_attr(login, 'profile')
	
	def get_birth_year(self, login):
		year=self.get_xml_attr(login, 'birth_year')
		return int(year)

	def get_user_pass(self, login):
		return self.get_xml_attr(login, 'password')

	def set_user_pass(self, login, passwd):
		self.set_xml_attr(login, 'password', passwd)
		
	def set_birth(self, login, year, month, day):
		self.set_xml_attr(login, 'birth_day', str(year))
		self.set_xml_attr(login, 'birth_month', str(month))
		self.set_xml_attr(login, 'birth_year', str(day))
		
	def set_profile_path(self, login, profile_id):
		self.set_xml_attr(login, 'profile', profile_id)
		
	def set_phone(self, login, phone):
		self.set_xml_attr(login, 'phone', phone)
		
	def get_photo_arr(self):
		ret_arr=[]
		
		for photo in self.tree.xpath('//photo'):
			if photo.text:ret_arr.append(photo.text)
		
		return ret_arr
	

