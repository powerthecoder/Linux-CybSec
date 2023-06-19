# update and upgrade
# install unattended-upgrades
# configure unattended-upgrades
# install fail2ban
# configure fail2ban (->restart)
# install ufw
# enable and configure ufw (ask user for ports)
# configure ufw to protect against portscans and botattacks *
# install sshd
# configure sshd (->restart) (no keys)
# configure IPTables for PortScanning and BotAttacks
# install portsentry
# configure portsentry
# install sshguard
# configure sshguard
# * install OpenVAS https://www.geeksforgeeks.org/installing-openvas-on-kali-linux/#
# install and run chrootkit

# Developer: powerthecoder
# GitHub: https://github.com/powerthecoder/Linux-CybSec

import os
import time

def InstallAll():
    print("### STARTING SCRIPT ###")
    time.sleep(3)
    # Update and Upgrade system
    print("\n"*5)
    print("### STARTING UPDATES ###")
    os.system("apt-get update -y && apt-get upgrade -y")

    # Install unattended-upgrades and configure
    print("\n"*5)
    print("### STARTING UNATTENDED UPGRADES ###")
    os.system("apt-get install unattended-upgrades -y")
    print("\n"*5)
    unattended_upgrades_reboot = input("Do you want Unattended Upgrades to automaticaly reboot your system? (default = no): ")
    os.system("cp /etc/apt/apt.conf.d/50unattended-upgrades /etc/apt/apt.conf.d/50unattended-upgrades.backup")
    if (unattended_upgrades_reboot.lower() == "y" or unattended_upgrades_reboot.lower() == "yes"):
        #/etc/apt/apt.conf.d/50unattended-upgrades
        os.system("wget -O /etc/apt/apt.conf.d/50unattended-upgrades https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/unattended_upgrades_reboot_yes")
        os.system("systemctl stop unattended-upgrades.service")
        os.system("systemctl start unattended-upgrades.service")
        os.system("systemctl restart unattended-upgrades.service")
    else:
        os.system("wget -O /etc/apt/apt.conf.d/50unattended-upgrades https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/unattended_upgrades_reboot_no")
        os.system("systemctl stop unattended-upgrades.service")
        os.system("systemctl start unattended-upgrades.service")
        os.system("systemctl restart unattended-upgrades.service")

    
    print("\n"*5)
    print("### STARTING FAIL2BAN ###")
    # Install Fail2Ban and configure
    os.system("apt-get install fail2ban -y") #/etc/fail2ban/jail.local
    os.system("cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.backup")
    os.system("wget -O /etc/fail2ban/jail.local https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/fail2ban_jail.local")
    os.system("systemctl stop fail2ban")
    os.system("systemctl start fail2ban")
    os.system("systemctl restart fail2ban")

    print("\n"*5)
    print("### STARTING UFW ###")
    # Install ufw and configure
    os.system("apt-get install ufw -y")
    print("\n"*5)
    ufw_ports = input("Enter ports you want opened (123,456,789): ")
    ufw_port_list = ufw_ports.split(",")
    for port in ufw_port_list:
        os.system(f"ufw allow {port}")
        time.sleep(1)
    os.system("systemctl stop ufw")
    os.system("systemctl start ufw")
    os.system("systemctl restart ufw")

    print("\n"*5)
    print("### STARTING SSHD ###")
    # Install sshd and configure
    os.system("apt-get install openssh-server -y")
    os.system("cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup")
    os.system("wget -O /etc/ssh/sshd_config https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/sshd_config")
    os.system("systemctl restart ssh")

    print("\n"*5)
    print("### STARTING IPTABLES ###")
    # Setup IPTables
    os.system("""
/sbin/iptables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP
/sbin/iptables -t mangle -A PREROUTING -p tcp -m conntrack --ctstate NEW -m tcpmss ! --mss 536:65535 -j DROP
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
/sbin/iptables -t mangle -A PREROUTING -s 224.0.0.0/3 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 169.254.0.0/16 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 172.16.0.0/12 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 192.0.2.0/24 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 192.168.0.0/16 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 10.0.0.0/8 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 0.0.0.0/8 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 240.0.0.0/5 -j DROP
/sbin/iptables -t mangle -A PREROUTING -s 127.0.0.0/8 ! -i lo -j DROP
/sbin/iptables -t mangle -A PREROUTING -p icmp -j DROP
/sbin/iptables -t mangle -A PREROUTING -f -j DROP
/sbin/iptables -A INPUT -p tcp -m connlimit --connlimit-above 111 -j REJECT --reject-with tcp-reset
/sbin/iptables -A INPUT -p tcp --tcp-flags RST RST -m limit --limit 2/s --limit-burst 2 -j ACCEPT
/sbin/iptables -A INPUT -p tcp --tcp-flags RST RST -j DROP
/sbin/iptables -A INPUT -p tcp -m conntrack --ctstate NEW -m limit --limit 60/s --limit-burst 20 -j ACCEPT
/sbin/iptables -A INPUT -p tcp -m conntrack --ctstate NEW -j DROP
#/sbin/iptables -t raw -D PREROUTING -p tcp -m tcp --syn -j CT --notrack
#/sbin/iptables -D INPUT -p tcp -m tcp -m conntrack --ctstate INVALID,UNTRACKED -j SYNPROXY --sack-perm --timestamp --wscale 7 --mss 1460
#/sbin/iptables -D INPUT -m conntrack --ctstate INVALID -j DROP
/sbin/iptables -A INPUT -p tcp --dport ssh -m conntrack --ctstate NEW -m recent --set
/sbin/iptables -A INPUT -p tcp --dport ssh -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 10 -j DROP
/sbin/iptables -N port-scanning
/sbin/iptables -A port-scanning -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s --limit-burst 2 -j RETURN
/sbin/iptables -A port-scanning -j DROP
""")
    
    print("\n"*5)
    print("### STARTING PORTSENTRY ###")
    # Install portsentry and configure
    os.system("apt-get install portsentry -y")
    os.system("cp /etc/portsentry/portsentry.conf /etc/portsentry/portsentry.conf.backup")
    os.system("wget -O /etc/portsentry/portsentry.conf https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/portsentry.conf")
    os.system("systemctl stop portsentry")
    os.system("systemctl start portsentry")
    os.system("systemctl restart portsentry")

    print("\n"*5)
    print("### STARTING SSHGUARD ###")
    # Install sshguard and configure
    os.system("apt-get install sshguard -y")
    os.system("cp /etc/sshguard/sshguard.conf /etc/sshguard/sshguard.conf.backup")
    os.system("wget -O /etc/sshguard/sshguard.conf https://raw.githubusercontent.com/powerthecoder/Linux-CybSec/main/Config%20Files/sshguard.conf")
    os.system("systemctl stop sshguard")
    os.system("systemctl start sshguard")
    os.system("systemctl restart sshguard")

    print("\n"*5)
    print("### STARTING UPDATES ###")
    os.system("apt-get update -y && apt-get upgrade -y")

    print("\n"*5)
    print("### STARTING RKHUNTER ###")
    # Install rkhunter and run
    os.system("apt-get install -y rkhunter")
    os.system("rkhunter --update")
    os.system("rkhunter --check")

    time.sleep(5)
    x = 0
    while (x != 1):
        print("\n"*5)
        print("### ATTENTION USER, SERVER WILL NOT LET YOU LOG IN UNLESS YOU DO THE FOLLOWING ###")
        # Creating a new user
        print("\n"*3)
        print("!!! The Following prompt will ask you to create a new user, please make sure to log in with this user")
        print("The server will no longer allow you to log in with the username 'root' !!!")
        print()
        print()
        yes_or_no = input("Please type 'understand' if you understand the prompt: ")
        if (yes_or_no == "understand"):
            time.sleep(2)
            username = input("Please enter new username: ")
            os.system(f"useradd {username}")
            os.system(f"usermod -aG sudo {username}")
            print("\n"*5)
            print(f"### NEW USER {username} HAS BEEN CREATED ###")
            print("When you log out please make sure to log in with this new user")
            print()
            print()
            print()
            print(f"# ATTENTION # Please make sure to type this command `passwd {username}`")
            x = 1
        else:
            os.system("clear")
            pass




if __name__ == "__main__":
    InstallAll()
