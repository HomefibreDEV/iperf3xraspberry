## Anmerkung: ##

Diese Software wurde von unseren Praktikanten entwickelt. Unser Unternehmen bietet keinen zusätzlichen Support zu dieser Software. Sie dient zum basteln und ausprobieren und könnte in Zukunft durch weitere Projekte ergänzt oder erweitert werden.

Viel Spaß beim ausprobiere und testen.

Known issues and limitations:

    Small display is white until driver is installed!
    USB-Drive is working with USB 3 blue marked USB ports in our testbed!
    additional iperf3 arguments need to be tested!
    For raspberry pi os lite (32-bit) tested!
  
## Beschschreibung: ##
  Dieses Projekt bietet die Möglichkeit, mithilfe von zwei Raspberry Pi 4B die Übertragungsgeschwindigkeit zwischen zwei Punkten in einem LAN zu messen.
  Dafür läuft auf einem der beiden Raspberry ein iPerf3-Server und am anderen ein Pythonskript welches einen iPerf3-Speedtest startet und das Ergebnis auf einen USB-Stick oder lokal am Raspberry Pi speichert.
  Argumente für den Iperf Test können im speedtest.py definiert werden. In der aktuellen Version ist ein TCP Test mit maximaler Datenrate über 30 Sekunden definiert (-t 30).
  Es können alternativ mit einem Rapsberry und jeder anderen Art eines IPERF3 Server / Clients tests durchgeführt werden, z.B Raspberry als Client und Computer als Server, dazu muss nur die passende IP-Adresse konfiguriert werden. (Siehe Einstellungen!)

## Benötigte Komponenten: ##

    • 2x Raspberry Pi 4 Model B
    • 2x Micro SD-Karte
    • 2x USB-C 15.3W Powersupply
    • 1x Raspberry Pi 4 Touch Screen (https://amzn.eu/d/aauua0w)
    • Optional Micro HDMI Kabel & Tastatur um direkt am Raspberry PI zu arbeiten.

## Vorbereitung Raspberry Pi ##

1) Bauen Sie das Raspberry in das Gehäuse mit Display laut Anleitung ein

       https://amzn.eu/d/aauua0w
   
3) Installieren Sie auf der Micro SD-Karte Raspberry Pi OS Lite (32-Bit) mit Raspberry Pi Imager
   
        https://www.raspberrypi.com/software/
   
4) Nach dem Starten des Raspberry Updates durchführen und Git installieren
   
        sudo apt update -y && sudo apt-get upgrade -y && sudo apt install git -y

## Installation Client auf dem Raspberry Pi mit Display: ##    
Der Client startet einen Test, ob eine Verbindung besteht und ob ein USB Speichermedium angeschossen ist und speichert entsprechend entweder lokal oder auf dem Speichermedium.

   
1) Display Treiber installieren

        git clone https://github.com/goodtft/LCD-show.git
        chmod -R 755 LCD-show
        cd /home/pi/LCD-show/
        sudo ./MHS35-show

2) Autologin einstellen:
  
       sudo raspi-config

    Man findet die Entsprechende Einstellung unter:

       System options
       Boot / Auto Login
       Console Autologin
    Diese Option einfach mit Enter bestätigen.

4) client.sh laden und ausführen.
       
        git clone https://github.com/HomefibreDEV/iperf3xraspberry.git
        cd ./iperf3xraspberry 
        sudo chmod +x client.sh
        sudo ./client.sh
   Wärhend der Installation kann es sein, dass IPERF3 nach der Startoption frägt. Hier einfach mit Yes den Deamon Autostart bestätigen.

## Installation Server auf dem 2. Raspberry Pi, falls vorhanden: ##
Der Server benötigt kein Display. Er wird einmalig angeschlossen und wartet auf einen Client, der einen Test durchführen möchte.
    
1) Autologin einstellen:
  
        sudo raspi-config

   System options / Boot / Auto Login / Console Autologin

2) Server.sh laden und ausführen.
   
          git clone https://github.com/HomefibreDEV/iperf3xraspberry.git
          cd ./iperf3xraspberry
          sudo chmod +x server.sh
          sudo ./server.sh
   Wärhend der Installation kann es sein, dass IPERF3 nach der Startoption frägt. Hier einfach mit Yes den Deamon Autostart bestätigen.

## Option ohne 2. Raspberry Pi, z.B. Windows 11 Computer. ##

Für die Nutzung mit dem Raspberry PI Client muss der Computer die IP Adresse 10.10.10.111 bestizen mit Subnetz Maske 255.255.255.0.

Sie können IPERF3 aus dem Interent auf Ihren PC laden und mit der Console IPERF3 ausführen:
1) Laden Sie IPERF3 für Windows herunter
    
         https://iperf.fr/iperf-download.php

2) Entpacken Sie iperf3 auf den Desktop

    Öffnen Sie den Ordner
    Gehen Sie auf Datei > Windows Powershell öffnen
    
Tippen Sie den folgenden Befehl ein, um IPERF3 Server auf dem PC zu starten:

    .\iperf3.exe -s

mit Strg+c können Sie den IPerf3 Server abbrechen.
   

## Einstellungen: ##

    Client IP Adresse: 10.10.10.112/24
    Server IP Adresse: IP 10.10.10.111/24

    Iperf3: Iperf3 -c -t 30
    Ergebnisse: result-###.txt
    
    ### -> Lfd. Nummer




