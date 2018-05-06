# -*- coding: utf-8 -*-

import urllib , urllib2
import lxml.html

def send_request(bic):
	server='http://www.xxx.ru/help/bic.asp'
	data = {
			'bic': bic,
			}
	
	headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0',
			   }
	
	request = urllib2.Request(server, urllib.urlencode(data), headers)
	
	try:
		f = urllib2.urlopen(request)
		ht=f.read()
		#print f.code 
		doc = lxml.html.document_fromstring(ht)
		return doc
	except:
		return  False
	
def get_data(bic):
	res=send_request(bic)
	if res is not None:
		rows = res.xpath('//tr[@style="font-size: 11;"]/td')
		if len(rows)==8:
			ret_val={
					'bic':rows[1].text,
					'korr':rows[2].text,
					'name':rows[3].text,
					'limit':rows[4].text,
					'sity':rows[5].text,
					'address':rows[6].text,
					'bic_successor':rows[6].text,
					}
			
			print ret_val
		else:
			print 'Bic dont found'
	else:
		print 'Error get http'

get_data('049205772')
	

