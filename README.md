Beschschreibung:
  Dieses Projekt bietet die Möglichkeit, mithilfe von zwei Raspberry Pi 4B die Übertragungsgeschwindigkeit zwischen zwei Punkten in einem LAN zu messen.
  Dafür läuft auf einem der beiden Raspberry sein iPerf3-Server und am anderen ein Pythonskript welches einen iPerf3-Speedtest startet und das Ergebnis auf einen USB-Stick oder lokal am Pi speichert.

Benötigte Komponenten:
  • 2x Raspberry Pi 4 Model B
  • 2x SD-Karte
  • 2x USB-C 15.3W Powersupply
  • 1x Raspberry Pi 4 Touch Screen

Installation Server / Client:

  Server:
    Der Server benötigt kein Display. Er wird einmalig angeschlossen und wartet auf einen Client, der einen Test durchführen möchte.
    
    1) Server.sh laden und ausführen.
          git clone https://github.com/HomefibreDEV/iperf3xraspberry.git
          sudo chmod +x server.sh
          sudo ./server.sh

  Client:
    Der Client startet einen Test, ob eine Verbindung besteht und ob ein USB Speichermedium angeschossen ist und speichert entsprechend entweder lokal oder auf dem Speichermedium.
    
    1) Display Treiber installieren:
        sudo apt update -y && sudo apt-get upgrade -y && sudo apt install git -y
        git clone https://github.com/goodtft/LCD-show.git
        chmod -R 755 LCD-show
        cd /home/pi/LCD-show/
        sudo ./MHS35-show

    2) Autologin einstellen:
      sudo raspi-config
      System options / Boot / Auto Login / Console Autologin

    3) Die folgenden beiden Zeilen aus /etc/rc.local löschen:
      sleep 7
      fbcp &
      
    4) client.sh laden und ausführen.
      git clone https://github.com/HomefibreDEV/iperf3xraspberry.git
      sudo chmod +x client.sh
      sudo ./client.sh

## git clone need To be Tested! ##

Einstellungen:

Client: IP 10.10.10.112/24
Server: IP 10.10.10.111/24

Iperf3: Iperf3 -t 30
Ergebnisse: result-###.txt

### -> Lfd. Nummer

## additional Iperf3 arguments should be tested ##


