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

def email(msg):
    parser = SafeConfigParser()
    parser.read('config.txt')
    for section_name in parser.sections():
       sender = parser.get(section_name,'sender')
       password = parser.get(section_name,'password')
       recipient = parser.get(section_name,'recipient')
    subject = 'Alert GateWay VTC'
    BODY = string.join((
        "From: %s" % sender,
        "To: %s" % recipient,
        "Subject: %s" % subject ,
        "",
        "\n",
        msg
        ), "\r\n")
    session = smtplib.SMTP('smtp.gmail.com:587')
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)
    session.sendmail(sender, recipient, BODY)
    session.quit()

def alert(msg):
  now = datetime.datetime.now()
#chuan  msg = now.strftime("Date: %d-%m-%Y") + "\n" + now.strftime("Time : %H:%M") + "\n" + msg
#  msg = now.strftime("Date: %d-%m-%Y") + "\n" + now.strftime("Time : %H:%M"  ) + msg

#  msg = now.strftime("Date: %d-%m-%Y") + "\n" + now.strftime("Time : %H:%M. ") + msg
  date = now.strftime("Date: %d-%m-%Y")
  time = now.strftime("Time : %H:%M"  ) 
#  msg = 
  msg = date + "   "+ time + "       " + msg
  threshold       = 10
  SMS_max         = 4
  alert_interval  = 7200                                           #2 tieng roi quay vong
  sms_interval    = 300                                            #5 phut' thi nhan tin 1 lan
  weekend_days        = 1    # So^' ngay` nghi? cuoi' tua^n`
  SMS_count        = 0
  alert_level      = 0
  sent_alert_level = 0
  critical         = 0
  my_string        = ""
  timing_by_sec    = int(getoutput("date +%s"))    # seconds since 1970-01-01 00:00:00 UTC
  timing_sms_sent  = 0
  url = "http://222.255.8.122:8888/ws/wsdl/MainProcessor.wsdl"
  client = Client(url)
  parser = SafeConfigParser()
  parser.read('config.txt')
  for section_name in parser.sections():
    user_sms = parser.get(section_name,'user_sms')
    password_sms = parser.get(section_name,'password_sms')
  while (1):
     current_time = int(getoutput("date +%k"))
     day_of_week  = int(getoutput("date +%u"))

     if (current_time >= 8) and (current_time < 22 ) and (day_of_week <= ( 7 - weekend_days )): #gio lam viec la 8h,ket thuc luc 22h
        critical = threshold
     timing_by_sec = int(getoutput("date +%s"))
     if (alert_level != sent_alert_level) and (timing_by_sec >= ( timing_sms_sent + 300)): #sau moi lan gui tin nhan thanh cong thi 5' se gui 1 lan,tong cong chi gui 4 tin nhan
#sau do se vao vong lap 2 tieng sau moi check tiep
         if (critical >= threshold):
              client.service.sendText("0908446886", msg, user_sms, password_sms)
	      email(msg)
              SMS_count = SMS_count + 1
              timing_sms_sent = int(getoutput("date +%s"))
              sleep(2)
         critical = threshold - 1
         sent_alert_level = alert_level
     else:
          if (SMS_max > SMS_count) and (timing_by_sec >= ( timing_sms_sent + 300)):
                 if (critical >= threshold):
                       client.service.sendText("0908446886", msg, user_sms, password_sms)
		       email(msg)
                       SMS_count = SMS_count + 1
                       timing_sms_sent = int(getoutput("date +%s"))
                       sleep(2)
                 critical = threshold - 1
          elif (timing_by_sec >= ( timing_sms_sent + alert_interval)):
                SMS_count = 0
                sent_alert_level = 0
                critical         = 0
     sleep(10)
  else:
        sleep(2700)


def check_ping_gmail(vlanx):

    ping_gmail0 = 'ping -I %s -c 3 -W 1 smtp.gmail.com' %vlanx
    ping_gmail = ping_gmail0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    ping_gmail_result = getoutput(ping_gmail)
    if (getoutput(ping_gmail) == 0) :
	return True
    return False

def check_host_gw(vlanx,gw):
    ping_host_gw0 = 'ping -c 3 -W 1 %s' %gw
#    ping_host_gw = ping_host_gw0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'   
#    ping_host_gw0 = 'ping -I %s -c 3 -W 1 smtp.gmail.com' %vlanx
    ping_host_gw = ping_host_gw0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    ping_host_gw_result = getoutput(ping_host_gw)
    if (ping_host_gw_result >= "50") :
	return True
    else:
	msg = "%s bi die" %(vlanx)
        alert(msg)
    return False

def check_host_gw_ro(vlanx,gw):
    ping_host_gw0 = 'ping -c 3 -W 1 %s' %gw
    ping_host_gw = ping_host_gw0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    ping_host_gw_result = getoutput(ping_host_gw)
    if (ping_host_gw_result >= '50') :
        return True
    else:
        return False

def update_ro_st99(vlanx,gw):
    g1 = ''
    if check_host_gw_ro(vlanx,gw):
       g1="nexthop via %s dev %s weight 3 "    %(gw,vlanx)
    return g1
    
def print_ro_st99():
    parser = SafeConfigParser()
    parser.read('config.ini.txt')
    g = 'ip ro replace default table 99 '
    g1 = ''
    for section_name in parser.sections():
       vlan = parser.get(section_name,'vlan')
       ipwan = parser.get(section_name,'ip')
       gateway = parser.get(section_name,'gw')
       g1 += update_ro_st99(vlan,gateway)
    return g+g1

def run_ro_st99():
   while True:
   	s= print_ro_st99()
        sleep(1) #delay 1s roi chay tiep luon

    


def download(vlanx,ip):
##Ban khoan giua dung urllib2 hay wget
##Download giua cac interface ma dung wget thi dung ex : wget --bind-address=14.160.47.142 link
#Check download dai 123,tinh toc do theo kbps

    xoa_file_123 = getoutput("rm -f testdownload.test_123") 
    g_123 = 'wget --bind-address=%s http://123.30.53.118/testdownload.test_123' %ip
    wget_start_123 = time()
    sh_123 = getoutput(g_123)
    wget_end_123 = time()
    f_123 = open("testdownload.test_123")
    data_123 = f_123.read()
    
    giaydownload_123 = wget_end_123 - wget_start_123
    tocdo_123 = (len(data_123) / 1024.0) / giaydownload_123
    f_123.close()
    xoa_file_123 = getoutput("rm -f testdownload.test_123")

#    print "Download file dai 123 tu %s , toc do:%s , so giay la:%s" %(vlan,tocdo_123,giaydownload_123)
# 	check download dai 222
    xoa_file_222 = getoutput("rm -f testdownload.test_222")
    g_222 = 'wget --bind-address=%s http://222.255.27.172/testdownload.test_222' %ip
    wget_start_222 = time()
    sh_222 = getoutput(g_222)
    wget_end_222 = time()
    f_222 = open("testdownload.test_222")
    data_222 = f_222.read()
    giaydownload_222 = wget_end_222 - wget_start_222
    tocdo_222 = (len(data_222) / 1024.0) / giaydownload_222
    f_222.close()
    xoa_file_222 = getoutput("rm -f testdownload.test_222")
#    print "Download file dai 222 tu %s , toc do:%s , so giay la:%s" %(vlan,tocdo_222,giaydownload_222)
#    print "wget download toi so giay -> %s , toc do download la %s" % (int(giaydownload),int(tocdo))
 
     
parser = SafeConfigParser()
parser.read('config.ini.txt')

for section_name in parser.sections():
   vlan = parser.get(section_name,'vlan')
   ipwan = parser.get(section_name,'ip')
   gateway = parser.get(section_name,'gw')
   subnet = parser.get(section_name,'subnet')
   dns = parser.get(section_name,'dns')
   check_host_gw(vlan,gateway)

#while True:
#  print_ro_st99()
#run_ro_st99()

#while True:
#   s= print_ro_st99() 
#   sh = getoutput(s)
#   print print_ro_st99()
#   sleep(900)

# Sleep trong 15 phut 15*60
#   print download(vlan,ipwan)
#Da cho chay thu chuong trinh, tam thoi in vao ip r s t 99 
#Ket qua la chuong trinh chay de update print ro st 99 mat 28 giay(quet toan bo cac vlan trong file config)
#Thu cho slepp trong 15 phut,ket qua chay OKIE. cu 15' lai quet 1 lan,neu gateway die thi se khong update r s t,trong vi du nay la 99
