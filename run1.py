import os
from ConfigParser import SafeConfigParser
from commands import *
import time
from time import time, sleep
import smtplib
import datetime
import string
import suds
from suds.client import Client


threshold       = 10
SMS_max         = 4
alert_interval  = 2700                                           #40'
sms_interval    = 180                                            #3 phut'
start_work_hour = 8
end_work_hour   = 22
weekend_days        = 1    # So^' ngay` nghi? cuoi' tua^n`
time_now = getoutput("date +'%R:%S'")
#SMS_count        = 0
#alert_level      = 0
#sent_alert_level = 0
#critical         = 0
#my_string        = ""
#timing_by_sec    = int(getoutput("date +%s"))    # seconds since 1970-01-01 00:00:00 UTC
#timing_sms_sent  = 0



def send_absolute_SMS():
    SMS_count = 0
    url = "http://222.255.8.122:8888/ws/wsdl/MainProcessor.wsdl"
    client = Client(url)	     
    if (critical >= threshold):
       client.service.sendText("0908446886", "test", "bachpf", "84qpL+cmQJc=")
       SMS_count = SMS_count + 1
       timing_sms_sent = getoutput("date +%s")
       sleep(2)

def send_SMS_to ():
    timing_by_sec = int(getoutput("date +%s"))
#    if (alert_level != sent_alert_level) and (timing_by_sec >= ( timing_sms_sent + sms_interval)):
    if (timing_by_sec >= ( timing_sms_sent + sms_interval)):
       send_absolute_SMS()
       critical = threshold - 1
       sent_alert_level = alert_level
    else:
        if (SMS_max > SMS_count) and (timing_by_sec >= ( timing_sms_sent + sms_interval)):
            send_absolute_SMS()
	    critical = threshold - 1
        elif (timing_by_sec >= ( timing_sms_sent + alert_interval)):
	    SMS_count = 0
	    sent_alert_level = 0
	    critical         = 0

#SMS_count        = 0
alert_level      = 0
sent_alert_level = 0
critical         = 0
my_string        = ""
timing_by_sec    = int(getoutput("date +%s"))    # seconds since 1970-01-01 00:00:00 UTC
timing_sms_sent  = 0


while (1):
  current_time = int(getoutput("date +%k"))
  day_of_week  = int(getoutput("date +%u"))
  
  if (current_time >= start_work_hour) and (current_time < end_work_hour ) and (day_of_week <= ( 7 - weekend_days )):
     msg        = ""
     ping_dantri0 = 'ping -I vlan0108 -c 3 -W 1 dantri.com.vn'
     ping_dantri = ping_dantri0+ '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
     if (getoutput(ping_dantri) >=50):
#        msg = msg +"Die"
	critical = threshold
     send_SMS_to()
     sleep(10)
  else:
	sleep(2700)









