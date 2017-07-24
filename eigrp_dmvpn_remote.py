#! /usr/bin/python
lines = open('input').read().split('\n')

Site_Name               =       lines[0].strip()
Loopback0_IP            =       lines[1].strip()
Tunnel0_IP				      =       lines[2].strip()
Remote_Public_IP        =       lines[3].strip()
Default_Gateway_IP      =       lines[4].strip()
Remote_subnet1          =       lines[5].strip()
Remote_subnet2          =       lines[6].strip()
Remote_subnet3          =       lines[7].strip()
Remote_subnet4          =       lines[8].strip()
SW_next_hop_IP          =		    lines[9].strip()

print "\n\n"
print "========HERE ARE ALL THE INPUTS========"


print "Site_Name                "+Site_Name
print "Loopback0_IP             "+Loopback0_IP
print "Tunnel0_IP               "+Tunnel0_IP
print "Remote_Public_IP         "+Remote_Public_IP
print "Default_Gateway_IP       "+Default_Gateway_IP
print "Remote_subnet1       	"+Remote_subnet1
print "Remote_subnet2       	"+Remote_subnet2
print "Remote_subnet3       	"+Remote_subnet3
print "Remote_subnet4       	"+Remote_subnet4
print "SW_next_hop_IP           "+SW_next_hop_IP


print "===================================="
print "\n\n"

target = open('configs_output', 'w')
target.truncate()

target.write("\n\n")

target.write("conf t"+"\n")
target.write("\n")

target.write("crypto isakmp policy 10"+"\n")
target.write(" encr aes"+"\n")
target.write(" authentication pre-share"+"\n")
target.write(" group 2"+"\n")
target.write("\n")

target.write("crypto isakmp key Y3sterDAYishi5t0ry address 67.22.227.170"+"\n")
target.write("\n")

target.write("crypto ipsec transform-set IPSEC_TRANS esp-aes esp-sha-hmac"+"\n")
target.write(" mode transport"+"\n")
target.write("\n")

target.write("crypto ipsec profile IPSEC_PROFILE"+"\n")
target.write(" set security-association lifetime seconds 10000"+"\n")
target.write(" set transform-set IPSEC_TRANS"+"\n")
target.write(" set pfs group2"+"\n")
target.write("\n")


target.write("ip access-list extended acl-allow-in"+"\n")
target.write(" permit ip host 67.22.227.170 any"+"\n")
target.write("\n")

target.write("ip access-list extended acl-allow-out"+"\n")
target.write(" permit ip host "+Remote_Public_IP+" host 67.22.227.170"+"\n")
target.write("\n")

target.write("interface Loopback0"+"\n")
target.write(" ip address "+Loopback0_IP+" 255.255.255.255"+"\n")
target.write("\n")

target.write("ip route 67.22.227.170 255.255.255.255 "+Default_Gateway_IP+" name TO_KOLO_ASR1"+"\n")
target.write("ip route 67.22.227.160 255.255.255.224 "+Default_Gateway_IP+" name BACKDOOR_MGMT_1"+"\n")
target.write("ip route 204.101.63.192 255.255.255.248 "+Default_Gateway_IP+" name BACKDOOR_MGMT_2"+"\n")
target.write("ip route 158.106.88.128 255.255.255.224 "+Default_Gateway_IP+" name BACKDOOR_MGMT_3"+"\n")
target.write("ip route 207.164.20.48 255.255.255.240 "+Default_Gateway_IP+" name BACKDOOR_MGMT_4"+"\n")
target.write("ip route 0.0.0.0 0.0.0.0 "+Default_Gateway_IP+" 254"+"\n")
target.write("\n")

target.write("ip route "+Remote_subnet1[:-3]+" 255.255.255.0 "+SW_next_hop_IP+"\n")
target.write("ip route "+Remote_subnet2[:-3]+" 255.255.255.248 "+SW_next_hop_IP+"\n")
target.write("ip route "+Remote_subnet3[:-3]+" 255.255.255.248 "+SW_next_hop_IP+"\n")
target.write("ip route "+Remote_subnet4[:-3]+" 255.255.252.0 "+SW_next_hop_IP+"\n")
target.write("\n")

target.write("ip prefix-list REDIST_TO_EIGRP seq 5 permit "+Remote_subnet1+"\n")
target.write("ip prefix-list REDIST_TO_EIGRP seq 10 permit "+Remote_subnet2+"\n")
target.write("ip prefix-list REDIST_TO_EIGRP seq 15 permit "+Remote_subnet3+"\n")
target.write("ip prefix-list REDIST_TO_EIGRP seq 20 permit "+Remote_subnet4+"\n")
target.write("\n")

target.write("route-map REDIST_TO_EIGRP permit 10"+"\n")
target.write(" match ip address prefix-list REDIST_TO_EIGRP"+"\n")
target.write("route-map REDIST_TO_EIGRP permit 20"+"\n")
target.write(" match interface Loopback0"+"\n")
target.write("\n")

target.write("router eigrp 100"+"\n")
target.write(" network "+Tunnel0_IP+" 0.0.0.0\n")
target.write(" redistribute static route-map REDIST_TO_EIGRP"+"\n")
target.write(" redistribute connected route-map REDIST_TO_EIGRP"+"\n")
target.write(" eigrp stub redistributed"+"\n")
target.write("\n")



target.write("interface Tunnel0"+"\n")
target.write(" bandwidth 50000"+"\n")
target.write(" ip address "+Tunnel0_IP+" 255.255.248.0"+"\n")
target.write(" no ip redirects"+"\n")
target.write(" ip mtu 1360"+"\n")
target.write(" ip nhrp authentication CiSc0!@#"+"\n")
target.write(" ip nhrp map 172.28.0.1 67.22.227.170"+"\n")
target.write(" ip nhrp map multicast 67.22.227.170"+"\n")
target.write(" ip nhrp network-id 99"+"\n")
target.write(" ip nhrp holdtime 120"+"\n")
target.write(" ip nhrp nhs 172.28.0.1"+"\n")
target.write(" ip tcp adjust-mss 1320"+"\n")
target.write(" tunnel source GigabitEthernet0/0/1"+"\n")
target.write(" tunnel destination 67.22.227.170"+"\n")
target.write(" tunnel key 4096"+"\n")
target.write(" tunnel protection ipsec profile IPSEC_PROFILE"+"\n")
target.write("\n")

target.write("end\n")
target.write("remove the static route from Kolotek core switch pointing to PAN\n")
target.write("remove static routes from PAN in Kolotek pointing to tunnel\n")


target.close()

raw_input("Press Enter to display the configs will be applied...")

from subprocess import call

script ="cat configs_output"
call(script, shell=True)

quit()
