#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import os
from ConfigParser import SafeConfigParser
from commands import *
import time
from time import time
#import subprocess

def check_ping_dantri(vlanx):
    
    ping_dantri0 = 'ping -I %s -c 3 -W 1 dantri.com.vn' %vlanx
    ping_dantri = ping_dantri0+ '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    if (getoutput(ping_dantri) == 0) :
#        print "%s ping toi Dantri LIVE" %vlanx
	return True 
    return False
#    else
#        print "%s ping toi Dantri.Com.vn Die roi" %vlanx
        

def check_ping_gmail(vlanx):

    ping_gmail0 = 'ping -I %s -c 3 -W 1 smtp.gmail.com' %vlanx
    ping_gmail = ping_gmail0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    ping_gmail_result = getoutput(ping_gmail)
    if (getoutput(ping_gmail) == 0) :
	return True
    return False
#        print "%s ping toi Gmail LIVE" %vlanx
#    else:
#        print "%s ping dang bi DIE" %vlanx

def check_ping_admicro(vlanx):

    ping_admicro0 = 'ping -I %s -c 3 -W 1 cp.admicro.vn' %vlanx
    ping_admicro = ping_admicro0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'
    ping_admicro_result = getoutput(ping_admicro)
    if (getoutput(ping_admicro) == 0) :
        return True
    return False




def check_host_gw(vlanx,gw):
    ping_host_gw0 = 'ping -c 3 -W 1 %s' %gw
    ping_host_gw = ping_host_gw0 + '| grep "%" | cut -d "%" -f 1 | cut -d " " -f 6'   
    ping_host_gw_result = getoutput(ping_host_gw)
    if (ping_host_gw_result == '0') :
	return True
    return False
#    	print "Fiber %s live nhe, ip la : %s" %(vlanx,gw)
#    else:    	
#	print "Fiber %s bi chet roi,ip la %s" %(vlanx,gateway)
        	

def update_ro_st99(vlanx,gw):
    g1 = ''
    if check_host_gw(vlanx,gw):
       g1="nexthop via %s dev %s weight 3 "    %(gw,vlanx)
    return g1
    
def print_ro_st99(vlanx,gw):
    parser = SafeConfigParser()
    parser.read('config.ini.txt')
    g = 'ip ro replace default table 99 '
    g1 = ''
    for section_name in parser.sections():
       vlan = parser.get(section_name,'vlan')
       ipwan = parser.get(section_name,'ip')
       gateway = parser.get(section_name,'gw')
       subnet = parser.get(section_name,'subnet')
       dns = parser.get(section_name,'dns')
       g1 += update_ro_st99(vlan,gateway)
    return g+g1
    
#def pigdig(vlanx):
##Thutuc nay de check dns query


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
#   print check_ping_dantri(vlan)
#   print check_host_gw(vlan,gateway)
s= print_ro_st99(vlan,gateway)
sh = getoutput(s)
print print_ro_st99(vlan,gateway)

#   print download(vlan,ipwan)
#Da cho chay thu chuong trinh, tam thoi in vao ip r s t 99 
#Ket qua la chuong trinh chay de update print ro st 99 mat 28 giay(quet toan bo cac vlan trong file config)
