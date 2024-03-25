#!/bin/bash

echo '-----------------------------------------------'
echo '-------- homefibre - iPerf x Raspberry --------'
echo '-------------- by Stefan Marbler --------------'
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

#add iPerf to autostart
echo '#!/bin/sh -e' > /etc/rc.local
echo '# rc.local' >> /etc/rc.local
echo '# Print the IP address' >> /etc/rc.local
echo '_IP=$(hostname -I) || true' >> /etc/rc.local
echo 'if [ "$_IP" ]; then' >> /etc/rc.local
echo '  printf "My IP address is %s\n" "$_IP"' >> /etc/rc.local
echo 'fi' >> /etc/rc.local
echo '' >> /etc/rc.local
echo '/bin/sleep 7 && sudo iperf3 -s &' >> /etc/rc.local
echo 'exit 0' >> /etc/rc.local

#change hostname
echo 'changing hostname'
echo '127.0.0.1       iPerf-Server' > /etc/hosts
echo '::1             localhost ip6-localhost ip6-loopback' >> /etc/hosts
echo 'ff02::1         ip6-allnodes' >> /etc/hosts
echo 'ff02::2         ip6-allrouters' >> /etc/hosts
echo '' >> /etc/hosts
echo '127.0.1.1       iPerf-Server' >> /etc/hosts
echo 'iPerf-Server' > /etc/hostname

#network configuration
echo 'configure network'
echo "" >> /etc/dhcpcd.conf
echo '# custom static network config for iPerf client' >> /etc/dhcpcd.conf
echo 'interface eth0' >> /etc/dhcpcd.conf
echo 'static ip_address=10.10.10.111/24' >> /etc/dhcpcd.conf

#change motd
echo "`clear`" > /etc/motd
echo "" >> /etc/motd
echo "-----------------------------------------------" >> /etc/motd
echo "-------- homefibre - iPerf x Raspberry --------" >> /etc/motd
echo "-------------- by Stefan Marbler --------------" >> /etc/motd
echo "-----------------------------------------------" >> /etc/motd
echo "" >> /etc/motd

#user info
echo 'Configuration finished'
echo 'Press [ENTER] key to reboot your Pi now...'
read 

#reboot
reboot
