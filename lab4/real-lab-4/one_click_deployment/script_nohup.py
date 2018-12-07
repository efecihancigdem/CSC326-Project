import os
import redis

r=redis.Redis('localhost',port='6379')
ip_addr=r.get('ip_addr')
os.system("nohup sudo python package/frontend/front_end_server.py "+ip_addr)