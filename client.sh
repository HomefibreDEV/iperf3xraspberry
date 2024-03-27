#!/bin/bash

echo '-----------------------------------------------'
echo '-------- homefibre - iPerf x Raspberry --------'
echo '-------------- by Stefan Marbler --------------'
echo '------------- and Alexadner Maier -------------'
echo '-----------------------------------------------'
echo ''
echo 'Starting with the configuration...'
echo 'This may take some minutes...'
echo ''

#update and install iPerf
echo 'updating Raspberry Pi'
sudo apt-get update && sudo apt-get upgrade -y
echo 'installing iPerf3'
sudo apt-get install iperf3 -y
echo 'installing nc'
sudo apt-get install netcat -y
#echo 'installing git'
#sudo apt-get install git -y

#make directories and download speedtest
echo 'downloading speedtest...'
echo '0' > config.txt
git clone https://github.com/HomefibreDEV/iperf3xraspberry.git /opt/lan-speedtest
cd /opt/lan-speedtest/speedtest
mkdir /opt/lan-speedtest/results
chmod +x /opt/lan-speedtest/speedtest/speedtest.py

#add iPerf to autostart
echo 'add speedtest to autostart...'
echo '' >> /home/pi/.bashrc
echo 'echo "starting speedtest in 10sec"' >> /home/pi/.bashrc
echo 'press [Ctrl]+[C] to cancel' >> /home/pi/.bashrc
echo '/bin/sleep 10' >> /home/pi/.bashrc
echo 'clear' >> /home/pi/.bashrc
echo 'cd /opt/lan-speedtest/speedtest' >> /home/pi/.bashrc
echo 'sudo python3 speedtest.py' >> /home/pi/.bashrc

#change hostname
echo 'changing hostname'
echo '127.0.0.1       iPerf-Client' > /etc/hosts
echo '::1             localhost ip6-localhost ip6-loopback' >> /etc/hosts
echo 'ff02::1         ip6-allnodes' >> /etc/hosts
echo 'ff02::2         ip6-allrouters' >> /etc/hosts
echo '' >> /etc/hosts
echo '127.0.1.1       iPerf-Client' >> /etc/hosts
echo 'iPerf-Client' > /etc/hostname

#network configuration
#echo 'configure network'
#echo "" >> /etc/dhcpcd.conf
#echo '# custom static network config for iPerf client' >> /etc/dhcpcd.conf
#echo 'interface eth0' >> /etc/dhcpcd.conf
#echo 'static ip_address=10.10.10.112/24' >> /etc/dhcpcd.conf

#change motd
echo "`clear`" > /etc/motd
echo "" >> /etc/motd
echo "-----------------------------------------------" >> /etc/motd
echo "-------- homefibre - iPerf x Raspberry --------" >> /etc/motd
echo "-------------- by Stefan Marbler --------------" >> /etc/motd
echo "------------- and Alexadner Maier -------------" >> /etc/motd
echo "-----------------------------------------------" >> /etc/motd
echo "" >> /etc/motd

#user info
echo 'Configuration finished'
read 
reboot
