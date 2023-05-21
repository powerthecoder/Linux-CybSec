import os
import time



# update and upgrade
# install fail2ban
# configure fail2ban (->restart)
# install ufw
# enable and configure ufw (ask user for ports)
# configure ufw to protect against portscans and botattacks
# install sshd
# configure sshd (->restart) (no keys)
# configure IPTables for PortScanning and BotAttacks
# install portsentry
# configure portsentry
# install and run chrootkit


print("Starting Script")
print("""
-----------------------
RUN IN SUDO
-----------------------
""")
time.sleep(5)

# Update and Upgrade
print("###### Updating Software and Operating System ######")
os.system("apt-get update -y && apt-get upgrade -y")


# Install Fail2Ban
print()
print("###### Installing Fail2Ban ###### ")
print()
time.sleep(1)
os.system("apt-get install -y fail2ban")
# Configure Fail2Ban
print("###### Configuring Fail2Ban ######")
os.system("cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.backup")
os.system("wget -O /etc/fail2ban/jail.conf https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/jail.local")
os.system("systemctl restart fail2ban")

# Install UFW 
print()
print("###### Installing UFW ######")
print()
time.sleep(1)
os.system("apt-get install -y ufw")
os.system("ufw enable")
# Configure UFW
print()
print("###### Configuring UFW ######")
print()
ports = input("Enter Ports (123/tcp,124/udp,125,100:200): ")
os.system(f"ufw allow {ports}")
os.system("ufw deny proto tcp flags FIN,SYN,RST,PSH,ACK,URG NONE FIN,SYN SYN,RST FIN,RST FIN,ACK FIN ACK,URG URG ACK,FIN FIN ACK,PSH PSH ALL ALL NONE FIN,PSH,URG SYN,FIN,PSH,URG SYN,RST,ACK,FIN,URG")
os.system("ufw deny proto icmp")
os.system("ufw route allow proto tcp synproxy all")
os.system("ufw limit proto tcp from any to any port 22")

# Install SSHD
print()
print("###### Installing SSHD ######")
print()
time.sleep(1)
os.system("apt-get install -y openssh-server")
# Configure SSHD
print("###### Configuring SSHD ######")
os.system("cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup")
os.system("wget -O /etc/ssh/sshd_config https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/sshd_config")
os.system("systemctl restart sshd")
os.system("systemctl restart ssh")

# Configure IPTables
print()
print("###### Configuring IPTables ######")
print()
time.sleep(1)
os.system("""
### 1: Drop invalid packets ###
/sbin/iptables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP

### 2: Drop TCP packets that are new and are not SYN ###
/sbin/iptables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP

### 3: Drop SYN packets with suspicious MSS value ###
/sbin/iptables -t mangle -A PREROUTING -p tcp -m conntrack --ctstate NEW -m tcpmss ! --mss 536:65535 -j DROP

### 4: Block packets with bogus TCP flags ###
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN,RST,PSH,ACK,URG NONE -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN FIN,SYN -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,RST FIN,RST -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,ACK FIN -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,URG URG -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,FIN FIN -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,PSH PSH -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL ALL -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL NONE -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL FIN,PSH,URG -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL SYN,FIN,PSH,URG -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP

### 5: Block spoofed packets ###
/sbin/iptables -t mangle -A PREROUTING -s 224.0.0.0/3 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 169.254.0.0/16 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 172.16.0.0/12 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 192.0.2.0/24 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 192.168.0.0/16 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 10.0.0.0/8 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 0.0.0.0/8 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 240.0.0.0/5 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 127.0.0.0/8 ! -i lo -j DROP

### 6: Drop ICMP/Ping (you usually don't need this protocol) ###
/sbin/iptables -t mangle -A PREROUTING -p icmp -j DROP

### 7: Drop fragments in all chains ###
/sbin/iptables -t mangle -A PREROUTING -f -j DROP

### 8: Limit connections per source IP ###
/sbin/iptables -A INPUT -p tcp -m connlimit --connlimit-above 111 -j REJECT --reject-with tcp-reset

### 9: Limit RST packets ###
/sbin/iptables -A INPUT -p tcp --tcp-flags RST RST -m limit --limit 2/s --limit-burst 2 -j ACCEPT
/sbin/iptables -A INPUT -p tcp --tcp-flags RST RST -j DROP

### 10: Limit new TCP connections per second per source IP ###
/sbin/iptables -A INPUT -p tcp -m conntrack --ctstate NEW -m limit --limit 60/s --limit-burst 20 -j ACCEPT
/sbin/iptables -A INPUT -p tcp -m conntrack --ctstate NEW -j DROP

### 11: Use SYNPROXY on all ports (disables connection limiting rule) ###
#/sbin/iptables -t raw -D PREROUTING -p tcp -m tcp --syn -j CT --notrack
#/sbin/iptables -D INPUT -p tcp -m tcp -m conntrack --ctstate INVALID,UNTRACKED -j SYNPROXY --sack-perm --timestamp --wscale 7 --mss 1460
#/sbin/iptables -D INPUT -m conntrack --ctstate INVALID -j DROP

### SSH brute-force protection ###
/sbin/iptables -A INPUT -p tcp --dport ssh -m conntrack --ctstate NEW -m recent --set
/sbin/iptables -A INPUT -p tcp --dport ssh -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 10 -j DROP

### Protection against port scanning ###
/sbin/iptables -N port-scanning
/sbin/iptables -A port-scanning -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s --limit-burst 2 -j RETURN
/sbin/iptables -A port-scanning -j DROP
""")

# Install PortSentry
print()
print("###### Installing PortSentry ######")
print()
time.sleep(1)
os.system("apt install -y portsentry")
# Configure PortSentry
print()
print("###### Configuring PortSentry ######")
print()
os.system("cp /etc/portsentry/portsentry.conf /etc/portsentry/portsentry.conf.backup")
os.system("wget -O /etc/portsentry/portsentry.conf https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/portsentry.conf")
os.system("systemctl restart portsentry")

# Install chrootkit
print()
print("###### Installing RKHUNTER ######")
print()
time.sleep(1)
os.system("apt-get install -y rkhunter")
# Run chrootkit
print()
print("###### Running RKHUNTER ######")
print()
os.system("rkhunter --update")
os.system("rkhunter --check")

print()
print("###### SCRIPT HAS BEEN COMPLETE ######")
print()