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


def check_host_gw(vlanx):
    ping_host_gw0 = 'ping -I %s -c 10 -f -W 2 smtp.gmail.com' %vlanx
    ping_host_gw = ping_host_gw0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    while vlanx <> "vlan0113":   
       if vlanx == "vlan0104":
          ping_host_0104 = 'ping -I vlan0104 -c 10 -f -W 2 smtp.gmail.com'
	  ping_host_gw104 = ping_host_0104 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
          ping_host_gw_result0104 = int(getoutput(ping_host_gw104))
          if (ping_host_gw_result0104 >= 50) :
		getoutput("ip ru de pref 51")
		getoutput("ip ru ad from 192.168.16.0/24 lookup 53 pref 51")
		getoutput("ip ru de pref 52")
		getoutput("ip ru ad from 192.168.15.0/24 lookup 53 pref 52")
                getoutput("ip ru de pref 55")
                getoutput("ip ru ad from 192.168.52.0/24 lookup 53 pref 55")
		return False
          else:
#		print "dang xu ly vlan0104"
		getoutput("ip ru de pref 51")
                getoutput("ip ru ad from 192.168.16.0/24 lookup 54 pref 51")
                getoutput("ip ru de pref 52")
                getoutput("ip ru ad from 192.168.15.0/24 lookup 54 pref 52")
                getoutput("ip ru de pref 55")
                getoutput("ip ru ad from 192.168.52.0/24 lookup 54 pref 55")
		return True

       if vlanx == "vlan0106":
          ping_host_0106 = 'ping -I vlan0106 -c 10 -f -W 2 smtp.gmail.com'
          ping_host_gw106 = ping_host_0106 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
          ping_host_gw_result0106 = int(getoutput(ping_host_gw106))
          if (ping_host_gw_result0106 >= 50) :
                getoutput("ip ru de pref 56")
                getoutput("ip ru ad from 192.168.10.209 lookup 53 pref 56")
                return False
          else:
#                print "dang xu ly vlan0106"
                getoutput("ip ru de pref 56")
                getoutput("ip ru ad from 192.168.10.209 lookup 56 pref 56")

       if vlanx == "vlan0107":
           ping_host_0107 = 'ping -I vlan0107 -c 10 -f -W 2 smtp.gmail.com'
           ping_host_gw107 = ping_host_0107 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
           ping_host_gw_result0107 = int(getoutput(ping_host_gw107))
           if (ping_host_gw_result0107 >= 50) :
		getoutput("ip ru de pref 21")
                getoutput("ip ru ad from all to 192.168.23.110 lookup 59 pref 21") #Chet duong nay thi switch duong
                getoutput("ip ru de pref 22")
                getoutput("ip ru ad from 192.168.23.110 lookup 59 pref 22")
                getoutput("ip ru de pref 61")
                getoutput("ip ru ad 192.168.25.54 lookup 59 pref 61")
                getoutput("ip ru de pref 62")
                getoutput("ip ru ad 192.168.25.118 lookup 59 pref 61")
                return False
           else:
#                print "dang xu ly vlan0107,vlan nay song"
                getoutput("ip ru de pref 21")
                getoutput("ip ru ad from all to 192.168.23.110 lookup 57 pref 21")
                getoutput("ip ru de pref 22")
                getoutput("ip ru ad from 192.168.23.110 lookup 57 pref 22")
                getoutput("ip ru de pref 61")
                getoutput("ip ru ad 192.168.25.54 lookup 57 pref 61")
                getoutput("ip ru de pref 62")
                getoutput("ip ru ad 192.168.25.118 lookup 57 pref 61")             
		return True

       if vlanx == "vlan0109":
          ping_host_0109 = 'ping -I vlan0109 -c 10 -f -W 2 smtp.gmail.com'
          ping_host_gw109 = ping_host_0109 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
          ping_host_gw_result0109 = int(getoutput(ping_host_gw109))
          if (ping_host_gw_result0109 >= 50) :
		getoutput("ip ru de pref 44")
		getoutput("ip ru ad from all to 192.168.25.139 lookup 62 pref 44")
		getoutput("ip ru de pref 50")
		getoutput("ip ru ad from  192.168.10.125 lookup 62 pref 50")
		return False
          else:
#		print "dang xu ly vlan0109,vlan nay song"
		getoutput("ip ru de pref 44")
                getoutput("ip ru ad from all to 192.168.25.139 lookup 59 pref 44")
                getoutput("ip ru de pref 50")
                getoutput("ip ru ad from  192.168.10.125 lookup 59 pref 50")

       ping_host_gw_result = int(getoutput(ping_host_gw))
       if (ping_host_gw_result >= 50):
           return False
       else:
           return True
       

def update_ro_st90(vlanx,gw):
    g1 = ''
    if check_host_gw(vlanx):
       g1="nexthop via %s dev %s weight 3 "    %(gw,vlanx)
    return g1
    
def print_ro_st90():
    parser = SafeConfigParser()
    parser.read('config.ini.txt')
    g = 'ip ro replace default table 90 '
    g1 = ''
    for section_name in parser.sections():
       vlan = parser.get(section_name,'vlan')
       ipwan = parser.get(section_name,'ip')
       gateway = parser.get(section_name,'gw')
       g1 += update_ro_st90(vlan,gateway)
    return g+g1

while True:
    now = datetime.datetime.now()
    msg = now.strftime("Date: %d-%m-%Y") + "\n" + now.strftime("Time : %H:%M")+ "\n" 
    f = open("/var/log/monitor-tools.log","a")
    f.write(msg)
    s= print_ro_st90()
#    print s
    f.write(s)
    f.write("\n\n")	
    getoutput(s)
#   for section_name in parser.sections():
#       vlan = parser.get(section_name,'vlan')
#       xuly_ip_ru(vlan)
    sleep(60) #delay 60s roi chay tiep luon

    
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
