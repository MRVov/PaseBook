# -*- coding: utf-8 -*-

import psycopg2
import random
import datetime

conn = psycopg2.connect("dbname='forum' user='forum' host='127.0.0.1' port='35432' password='U9CIZnLRwy9fJ9RWKamANZQoYPdjNSUu'")
print 'Succesfully connected'
cur = conn.cursor()

hamsters_arr=[335, 348, 349, 358, 363, 367, 381, 383, 386, 
			330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340]
papa_arr=[540,  541, 543, 544, 545, 546, 547]

def get_user_name(user_id):
	cur.execute('SELECT username FROM f_users WHERE user_id=%d' % user_id)
	return cur.fetchall()[0][0]

def print_time(stamp):
	t=datetime.datetime.fromtimestamp(stamp)
	print unicode(t)
	
def register_change():
	cur.execute("""SELECT user_id, user_regdate from f_users WHERE user_id>100;""")
	for i in  cur.fetchall():
		id=int(i[0])
		t=random.randint(1262304000, 1325376000)
		print id
		print t
		cur.execute("UPDATE f_users SET user_regdate = %d WHERE user_id = %d;" % (t, id))
	
def topic_mix(topic_id, per_min=60, per_max=300):
	sql="""SELECT post_id, post_time, poster_id from f_posts WHERE topic_id="""+str(topic_id)+""" and post_subject LIKE 'Re:%' ORDER BY post_id"""
	print sql
	topic_id=int(topic_id)
	cur.execute(sql)
	res=cur.fetchall()
	first=res[0]
	
	start_date=int(first[1])
	print 'Print start time'
	print_time(start_date)
	
	start_date=datetime.datetime.fromtimestamp(start_date)
	
	time_offset=0
	topic_last_poster_id=0
	topic_last_poster_name=''
	topic_last_post_time=0
	for i in  res:
		id=int(i[0])
		#t=int(i[1])
		#t=start_date
		epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
		min_offset=random.randint(per_min, per_max)
		time_offset+=min_offset
		#print min_offset+120
		curr_offset = datetime.timedelta(minutes=time_offset)
		
		t=start_date+curr_offset- epoch

		t=t.total_seconds()
		#print t
		
		
		poster=int(i[2])
		if poster not in papa_arr:
			poster=random.choice(hamsters_arr)
			
		print_time(t)	
		cur.execute("UPDATE f_posts SET poster_id = %d, post_time=%d WHERE post_id = %d;" % (poster, t, id))
		#print id
		#print t
		topic_last_poster_id=poster
		topic_last_post_time=t
		w=random.randint(500, 1000)
		user_name=get_user_name(topic_last_poster_id)
	SQL="UPDATE f_topics SET topic_last_poster_id=%d, topic_last_post_time=%d, topic_views=%d, topic_last_poster_name='%s' WHERE topic_id=%d;"% (topic_last_poster_id, topic_last_post_time, w, user_name, topic_id)
	cur.execute(SQL)
	
topic_mix(506)
conn.commit()
conn.close()

#https://bitcointalk.org/
