#!/usr/bin/python3

# -----------------------------------------------
# -------- homefibre - iPerf x Raspberry --------
# -------------- by Stefan Marbler --------------
# ------------- and Alexadner Maier -------------
# -----------------------------------------------

# import Modules
import os 
from os import path
import time
from datetime import datetime

# define Classes
#
# ----------------------------------------------------------------
# | Class: Search                                                |
# | Functions:                                                   |
# |  - __init__(self,server_ip):                                 |
# |    Beschreibung                                              |
# |                                                              |
# |  - ping_server(self):                                        |
# |    ping den iPerf-Server                                     |
# |                                                              |
# |  - check_iperf_status(self):                                 |
# |    testet ob iPerf am Server laeuft                          |
# |                                                              |
# |  - find_usb(self):                                           |
# |    sucht nach einen angeschlossenen USB-Stick am Pi          |
# |                                                              |
# ----------------------------------------------------------------
class Search:
    def __init__(self, server_ip, server_port):
        if server_ip != '':
            self._server_ip = server_ip
        if server_port != '':
            self._server_port = server_port

    def ping_server(self):
        resp_ping = os.system('ping -c 1 ' + self._server_ip + '>/dev/null 2>&1')

        if resp_ping == 0:
            return 1  # Host reachable
        else:
            return -1  # Host unreachable

    def check_iperf_status(self):
        resp_status = os.system('nc -zvw1 ' + self._server_ip + ' ' + self._server_port + '>/dev/null 2>&1')

        if resp_status == 0:
            return 1  # service up
        else:
            return -1  # service down

    def find_usb(self):
        usb_name = 'NO_DEVICE'
        resp_usb = os.popen('ls -l /dev/disk/by-uuid/').readlines()
        if len(resp_usb) > 3:
            devli = str(resp_usb[(len(resp_usb) - 1)]).split()
            for item in devli:
                if '../../sd' in item:
                    if item != '':
                        tmpli = str(item).split('/')
                        usb_name = tmpli[-1]
                    break   
        return usb_name

    def mount_usb(self, device):
        if device != '':
            if path.exists('/mnt/usb') is False:
                os.system('mkdir /mnt/usb && chown -R pi:pi /mnt/usb')

            os.system('mount /dev/' + device + ' /mnt/usb -o uid=pi,gid=pi' + '>/dev/null 2>&1')
        else:
            print('ERROR: No devise parsed! [Search(self, server_ip, server_port).mount_usb(self, device)')

    def unmount_usb(self):
        os.system('umount /mnt/usb' + '>/dev/null 2>&1')


# ----------------------------------------------------------------
# | Class: Speedtest                                             |
# | Functions:                                                   |
# |  - __init__(self,server_ip):                                 |
# |    Beschreibung                                              |
# |                                                              |
# |  - start_test(self):                                         |
# |    startet den iPerf-Test                                    |
# |                                                              |
# |  - get_result(self):                                         |
# |    returned das Ergebnis des Tests                           |
# |                                                              |
# ----------------------------------------------------------------
class Speedtest:
    def __init__(self, server_ip, args):
        self._result = None
        
        if server_ip:
            self._server_ip = server_ip
                
        if args:
            self._args = " ".join(args.split())
        else:
            self._args = ""


    def start_test(self):
        self._result = os.popen('iperf3 -c ' + self._server_ip + ' ' + self._args).readlines()

    def get_result(self):
        return self._result


# ----------------------------------------------------------------
# | Class: FileIO                                                |
# | Functions:                                                   |
# |  - __init__(self,server_ip):                                 |
# |    Beschreibung                                              |
# |                                                              |
# |  - write_to_file(self):                                      |
# |    schreibt das Ergebnis des Tests in ein txt-File am        |
# |    USB-Stick                                                 |
# |                                                              |
# ----------------------------------------------------------------
class FileIO:
    def __init__(self, path, result, num):
        if path != '' and result != '':
            self._path = path
            self._result = result
            self._header_text = '-----------------------------------------------\n-------- homefibre - iPerf x Raspberry --------\n-------------- by Stefan Marbler --------------\n-----------------------------------------------\n\n'
            self._testnr = num
            self._test_info = 'Testnr.: ' + str(self._testnr) + '\n\n'

    def write_to_file(self):
        if path.exists(self._path):
            self.__clear_file()

        self.__write(self._header_text)
        self.__write(self._test_info)

        for line in self._result:
            output = line
            self.__write(output)

    def __write(self, line):
        if line != '':
            f = None
            try:
                f = open(self._path, 'a')
                f.write(line)
            except:
                print('ERROR: Writing failed! [FileIO(self, path, result).__write(self, line)]')
            finally:
                if f:
                    f.close()
        else:
            print('ERROR: No line parsed! [FileIO(self, path, result).__write(self, line)]')

    def __clear_file(self):
        f = None
        try:
            f = open(self._path, 'r+')
            f.truncate(0)
        except:
            print('ERROR: Could not clear file! [FileIO(self, path, result).__clear_file(self)]')
        finally:
            if f:
                f.close()


# ----------------------------------------------------------------
# | Class: GetTestNum                                            |
# | Functions:                                                   |
# |  - __init__(self):                                           |
# |    Beschreibung                                              |
# |                                                              |
# |  - start(self):                                              |
# |    startet den iPerf-Test und managed alle Function-Calls    |
# |                                                              |
# ----------------------------------------------------------------
class GetTestNum:
    def __init__(self):
        self._configpath = '/opt/lan-speedtest/config.txt'
        self._testnumber = 1

    def __write_num(self, num):
        if num != '':
            f = None
            try:
                f = open(self._configpath, 'w')
                f.write(str(num))
            except :
                print('ERROR: Writing failed! [GetTestNum(self).__write_num(self, num)]')
            finally:
                if f:
                    f.close()
        else:
            print('ERROR: No number parsed! [GetTestNum(self).__write_num(self)]')

    def __read_num(self):
        if path.exists(self._configpath):
            f = None
            try:
                f = open(self._configpath, "r")
                self._testnumber =f.read()
            except:
                print('ERROR: Reading failed! [GetTestNum(self).__read_num(self)]')
            finally:
                if f:
                    f.close()
        else:
            self.__write_num('1')

    def getNum(self):
        self.__read_num()
        output = self._testnumber

        if len(str(self._testnumber)) <= 3 and int(self._testnumber) < 999:  
            while len(str(output)) < 3:
                output = '0' + str(output)
            new = int(self._testnumber) + 1
        else:
            new = 1

        self.__write_num(new)
        return str(output)

    def stepBack(self):
        new = int(self._testnumber) - 1
        self.__write_num(new)


# ----------------------------------------------------------------
# | Class: Controller                                            |
# | Functions:                                                   |
# |  - __init__(self):                                           |
# |    Beschreibung                                              |
# |                                                              |
# |  - start(self):                                              |
# |    startet den iPerf-Test und managed alle Function-Calls    |
# |                                                              |
# ----------------------------------------------------------------
class Controller:
    def __init__(self, server_ip, server_port, args, filename, testnr):
        if server_ip != '' and server_port != '' and filename != '':
            self._output_path_usb = '/mnt/usb/' + filename
            self._output_path = '/opt/lan-speedtest/results/' + filename
            self._server_ip = server_ip
            self._server_port = server_port
            self._args = args

            self.search = Search(self._server_ip, self._server_port)
            self.speedtest = Speedtest(self._server_ip, self._args)
            self.testnr = testnr

    def start(self):
        print('\n -----------------------------------------------\n',
            '-------- homefibre - iPerf x Raspberry --------\n',
            '-------------- by Stefan Marbler --------------\n',
			'------------ and Alexadner Maier --------------\n',
            '-----------------------------------------------')
        if self.search.ping_server() is 1:
            print('STATUS: Server found!')
            if self.search.check_iperf_status() is 1:
                print('STATUS: Service up!\nSTATUS: Searching USB storage media!')
                self._usb_device = self.search.find_usb()
                if self._usb_device != 'NO_DEVICE':
                    print('STATUS: USB storage media found!\nSTATUS: Mounting USB storage media!')
                    self.search.mount_usb(str(self._usb_device))
                    print('STATUS: USB storage media mounted!\nSTATUS: Speedtest running...')
                    self.speedtest.start_test()
                    print('STATUS: Speedtest finished!\nSTATUS: Writing results to USB storage media!')
                    FileIO(self._output_path_usb, self.speedtest.get_result(), self.testnr).write_to_file()
                    print('STATUS: Results written to USB storage media!\nSTATUS: Unmounting USB storage media!')
                    self.search.unmount_usb()
                    print('STATUS: USB storage media unmounted!')
                else:
                    print('STATUS: No USB storage media found!\nSTATUS: Saving results locally!\nSTATUS: Speedtest running...')
                    self.speedtest.start_test()
                    print('STATUS: Speedtest finished!\nSTATUS: Writing results to "/opt/lan-speedtest"!')
                    FileIO(self._output_path, self.speedtest.get_result(), self.testnr).write_to_file()
                    print('STATUS: Results written to "/opt/lan-speedtest"!')
                print('-----> Finsihed! Device can now be powered off! <-----')
            else: 
                GetTestNum().stepBack()
                print('ERROR: Service is down! [Controller(self, server_ip, server_port, filename).start(self)]')
        else: 
            GetTestNum().stepBack()
            print('ERROR: Server is down! [Controller(self, server_ip, server_port, filename).start(self)]')


# ------------------------------ main ------------------------------
# variables
iperf_server_ip = '10.10.10.111'  # set your iPerf server's IP  10.10.10.111
iperf_server_port = '5201'  # set your iPerf server's Port

iperf_args = '-t 30' # set additional parameters for iPerf

testnr = GetTestNum().getNum()
filename = 'result-' + str(testnr) + '.txt'  # set filename

Controller(iperf_server_ip, iperf_server_port, iperf_args, filename, testnr).start()
