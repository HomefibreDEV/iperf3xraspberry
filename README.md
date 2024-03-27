## Anmerkung: ##
    git clone need to be tested!
    additional iperf3 arguments need to be tested!
    for raspberry pi os lite (32-bit)
    Display is white until driver is installed.
    USB-Drive is working with USB 3 blue marked USB ports in our testbed.
   
known issue with display in installation process. If display didn't show comand line, repeat:

        cd /home/pi/LCD-show/
        sudo ./MHS35-show

## Beschschreibung: ##
  Dieses Projekt bietet die Möglichkeit, mithilfe von zwei Raspberry Pi 4B die Übertragungsgeschwindigkeit zwischen zwei Punkten in einem LAN zu messen.
  Dafür läuft auf einem der beiden Raspberry sein iPerf3-Server und am anderen ein Pythonskript welches einen iPerf3-Speedtest startet und das Ergebnis auf einen USB-Stick oder lokal am Pi speichert.

## Benötigte Komponenten: ##

    • 2x Raspberry Pi 4 Model B
    • 2x Micro SD-Karte
    • 2x USB-C 15.3W Powersupply
    • 1x Raspberry Pi 4 Touch Screen (https://amzn.eu/d/aauua0w)

## Vorbereitung Raspberry Pi ##

1) Bauen Sie das Raspberry in das Gehäuse mit Display laut Anleitung ein

       https://amzn.eu/d/aauua0w
   
3) Installieren Sie auf der Micro SD-Karte Raspberry Pi OS Lite (32-Bit) mit Raspberry Pi Imager
   
        https://www.raspberrypi.com/software/
   
4) Updates durchführen und Git installieren
   
        sudo apt update -y && sudo apt-get upgrade -y && sudo apt install git -y

## Installation Client auf dem Raspberry Pi: ##    
Der Client startet einen Test, ob eine Verbindung besteht und ob ein USB Speichermedium angeschossen ist und speichert entsprechend entweder lokal oder auf dem Speichermedium.

1) Update durchführen, Git herunterladen
   
        sudo apt update -y && sudo apt-get upgrade -y && sudo apt install git -y

2) Display Treiber installieren

        git clone https://github.com/goodtft/LCD-show.git
        chmod -R 755 LCD-show
        cd /home/pi/LCD-show/
        sudo ./MHS35-show

3) Autologin einstellen:
  
        sudo raspi-config

   System options / Boot / Auto Login / Console Autologin

4) Die folgenden beiden Zeilen aus /etc/rc.local löschen:
       
       sleep 7
       fbcp &
      
5) client.sh laden und ausführen.
       
        git clone https://github.com/HomefibreDEV/iperf3xraspberry.git
        cd ./iperf3xraspberry 
        sudo chmod +x client.sh
        sudo ./client.sh

## Installation Server auf dem 2. Raspberry Pi, falls vorhanden: ##
Der Server benötigt kein Display. Er wird einmalig angeschlossen und wartet auf einen Client, der einen Test durchführen möchte.
    
1) Server.sh laden und ausführen.
   
          git clone https://github.com/HomefibreDEV/iperf3xraspberry.git
          cd ./iperf3xraspberry
          sudo chmod +x server.sh
          sudo ./server.sh

## Einstellungen: ##

    Client: IP 10.10.10.112/24
    Server: IP 10.10.10.111/24

    Iperf3: Iperf3 -t 30
    Ergebnisse: result-###.txt
    
    ### -> Lfd. Nummer




