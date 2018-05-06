# -*- coding: utf-8 -*-

import urllib
import base64
import os
import urllib2
from time import sleep
import datetime
import time

import simplejson as json

from variables import *
import tempfile

def recognize_captcha(url, cook=None):
	try_count=6
	wait_sec=7
	
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0',
			'Cookie': cook,
			}

	req = urllib2.Request(url)
	req.add_header("Cookie", cook) # передаём cookie
	f = urllib2.urlopen(req)

	#data = f.read()
	#print headers
	#f = urllib.urlopen(url, None, headers )
	#print f.info()
	image=f.read()
	
	

	param={
		'method':'base64',
		'is_russian':'0',
		'key':antigate_key,
		'body':base64.b64encode(image)
		}
	
	host='http://antigate.com/in.php'
	param=urllib.urlencode(param)
	
	cap_req = urllib.urlopen(host, param, headers)
	#cap_req.info()
	body = cap_req.read().split('|')
	
	captcha_id=0
	
	if len(body) == 2:
		captcha_id = int(body[1])
	else:
		print 'Error antigate state- %s' % body
		return -1

	for i in range(try_count):
		check_url='http://antigate.com/res.php?key=%s&action=get&id=%d' % (antigate_key, captcha_id)
		f = urllib.urlopen(check_url, None, headers)

		check_body=f.read()
		if check_body[:3]=='OK|':return check_body[3:]
		sleep(wait_sec-i)
		
	return 'NO WOIT MORE'

import getpass, imaplib
import email

def get_email_confirm(email_name, email_domain, robot_name, search_string, search_len):
	try_count=10
	wait_time=60
	
	pdd_host='imap.yandex.ru'
	pdd_user='all@arterp.ru'
	pdd_pass='kabanina'
	
	M = imaplib.IMAP4(pdd_host)
	M.login(pdd_user, pdd_pass)
	M.select()
	#http://www.travelingfrontiers.com/projects/doku.php?id=imapv4_protocol
	
	for i in range(try_count):
		
		typ, data = M.search(None, '(HEADER TO "<%s@%s>" FROM "%s")' % (email_name, email_domain, robot_name))	

		if data[0]!=None:
			ids_arr=data[0].split()
			
			mess_id=ids_arr[0]
		
			typ, body=M.fetch(mess_id, '(RFC822)')
			print body
			srart_flag=body.find(search_string)
			return body[srart_flag+len(search_string):srart_flag+search_len+len(search_string)]
		
	M.close()
	M.logout()
	
#print get_email_confirm('dendmi743', 'arterp.ru', 'Facebook', '&code=3D', 9)

def ban_list(operation, url):

	url_ban_arr=[
				'talkgadget.google.com',
				'doubleclick.net',
				'google-analytics.com',
				]
	oper_ban_arr=[
				'chat/v1/',
				'voice/v1/',
				'talkgadget',
				'JsRemoteLog',
				'.mp3',
				#'apps-static/',
				#'settings/_/ac-static/',
				#'diagnostics/?soc-app=',

				'_/diagnostics/',
				'_/notifications/',
				'action=notificationswidget',
				'_/jserror?script=',
				'_/setbrowserprefs/',
				'/-iSVw94VnNc4/T9kJ016IDtI/AAAAAAAAAFg/',
				
				]
	for i in url_ban_arr:
		if url.find(i)>0:
			#print 'Ban by URL-%s'% url
			return False
		
	for i in oper_ban_arr:
		if operation.find(i)>0:
			#print 'Ban by Oper-%s'% operation
			return False
		
	return True

def get_image_load_data(image_path, user_id):
	def _jd2(*args):
		jsonstr = json.dumps(args, separators=(",",":"))
		return jsonstr
	
	return _jd2({
				"createSessionRequest": {
					"fields": [
						{
							"external": {
								"filename": os.path.basename(image_path), 
								"formPost": {}, 
								"name": "file", 
								"size": os.path.getsize(image_path)
							}
						}, 
						{
							"inlined": {
								"content": str(int(time.time())) + str(datetime.datetime.now().microsecond / 1000), 
								"contentType": "text/plain", 
								"name": "batchid"
							}
						}, 
						{
							"inlined": {
								"content": "sharebox", 
								"contentType": "text/plain", 
								"name": "client"
							}
						}, 
						{
							"inlined": {
								"content": "true", 
								"contentType": "text/plain", 
								"name": "disable_asbe_notification"
							}
						}, 
						{
							"inlined": {
								"content": "updates", 
								"contentType": "text/plain", 
								"name": "streamid"
							}
						}, 
						{
							"inlined": {
								"content": "true", 
								"contentType": "text/plain", 
								"name": "use_upload_size_pref"
							}
						}, 
						{
							"inlined": {
								"content": user_id, 
								"contentType": "text/plain", 
								"name": "effective_id"
							}
						}, 
						{
							"inlined": {
								"content": user_id, 
								"contentType": "text/plain", 
								"name": "owner_name"
							}
						}
					]
				}, 
				"protocolVersion": "0.8"
			})[1:-1]
			
from StringIO import StringIO			

debug_stream = StringIO()
			
def show_debug(pos=None):
	if not pos: print debug_stream.getvalue()
	else:
		pnow = debug_stream.pos
		debug_stream.seek(pos)
		print debug_stream.read()
		debug_stream.seek(pnow)
		
def run_debug(callback, *args, **kwargs): # ** *
	pos = debug_stream.pos
	ret = callback(*args, **kwargs)
	show_debug(pos)
	return ret

def dump_to_file(browser):
	tf = tempfile.NamedTemporaryFile().name+'.html'
	f = open(tf, "w")
	f.write(browser.html)
	f.close()
	print tf
