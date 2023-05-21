#!/bin/bash

# Update and Upgrade
echo "###### Updating Software and Operating System ######"
apt-get update -y && apt-get upgrade -y

# Install Fail2Ban
echo
echo "###### Installing Fail2Ban ###### "
echo
apt-get install -y fail2ban

# Configure Fail2Ban
echo "###### Configuring Fail2Ban ######"
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.backup
wget -O /etc/fail2ban/jail.conf https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/jail.local
systemctl restart fail2ban

# Install UFW
echo
echo "###### Installing UFW ######"
echo
apt-get install -y ufw
ufw enable

# Configure UFW
echo
echo "###### Configuring UFW ######"
echo
read -p "Enter Ports (123/tcp,124/udp,125,100:200): " ports
ufw allow $ports
ufw deny proto tcp flags FIN,SYN,RST,PSH,ACK,URG NONE FIN,SYN SYN,RST FIN,RST FIN,ACK FIN ACK,URG URG ACK,FIN FIN ACK,PSH PSH ALL ALL NONE FIN,PSH,URG SYN,FIN,PSH,URG SYN,RST,ACK,FIN,URG
ufw deny proto icmp
ufw route allow proto tcp synproxy all
ufw limit proto tcp from any to any port 22

# Install SSHD
echo
echo "###### Installing SSHD ######"
echo
apt-get install -y openssh-server

# Configure SSHD
echo "###### Configuring SSHD ######"
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
wget -O /etc/ssh/sshd_config https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/sshd_config
systemctl restart sshd
systemctl restart ssh

# Configure IPTables
echo
echo "###### Configuring IPTables ######"
echo
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
iptables -A INPUT -p tcp ! --syn -m conntrack --ctstate NEW -j DROP
iptables -A INPUT -p tcp -m conntrack --ctstate NEW -m tcpmss ! --mss 536:65535 -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags FIN,SYN,RST,PSH,ACK,URG NONE -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags FIN,SYN FIN,SYN -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags FIN,RST FIN,RST -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags FIN,ACK FIN -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ACK,URG URG -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ACK,FIN FIN -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ACK,PSH PSH -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ALL ALL -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ALL NONE -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ALL FIN,PSH,URG -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ALL SYN,FIN,PSH,URG -j DROP
iptables -A INPUT -t mangle -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP
iptables -A INPUT -s 224.0.0.0/3 -j DROP
iptables -A INPUT -s 169.254.0.0/16 -j DROP
iptables -A INPUT -s 172.16.0.0/12 -j DROP
iptables -A INPUT -s 192.0.2.0/24 -j DROP
iptables -A INPUT -s 192.168.0.0/16 -j DROP
iptables -A INPUT -s 10.0.0.0/8 -j DROP
iptables -A INPUT -s 0.0.0.0/8 -j DROP
iptables -A INPUT -s 240.0.0.0/5 -j DROP
iptables -A INPUT -s 127.0.0.0/8 ! -i lo -j DROP
iptables -A INPUT -p icmp -j DROP
iptables -A INPUT -f -j DROP
iptables -A INPUT -p tcp -m connlimit --connlimit-above 111 -j REJECT --reject-with tcp-reset
iptables -A INPUT -p tcp --tcp-flags RST RST -m limit --limit 2/s --limit-burst 2 -j ACCEPT
iptables -A INPUT -p tcp --tcp-flags RST RST -j DROP
iptables -A INPUT -p tcp -m conntrack --ctstate NEW -m limit --limit 60/s --limit-burst 20 -j ACCEPT
iptables -A INPUT -p tcp -m conntrack --ctstate NEW -j DROP

# Install PortSentry
echo
echo "###### Installing PortSentry ######"
echo
apt install -y portsentry

# Configure PortSentry
echo
echo "###### Configuring PortSentry ######"
echo
cp /etc/portsentry/portsentry.conf /etc/portsentry/portsentry.conf.backup
wget -O /etc/portsentry/portsentry.conf https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/portsentry.conf
systemctl restart portsentry

# Install rkhunter
echo
echo "###### Installing RKHUNTER ######"
echo
apt-get install -y rkhunter

# Run rkhunter
echo
echo "###### Running RKHUNTER ######"
echo
rkhunter --update
rkhunter --check

echo
echo "###### SCRIPT HAS BEEN COMPLETE ######"
echo
