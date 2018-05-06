# -*- coding: utf-8 -*-

from datetime import datetime

acc_log=models.SiteLogEntry.objects

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def write_log(request):
	user=None
	
	if request.user:
		user=request.user.username
		
	acc_log.create(
				uri=request.path, #
				client_ip=get_client_ip(request),
				referer =request.META.get('HTTP_REFERER', ''),
				created =datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				parameters= request.method,
				user =user
				)