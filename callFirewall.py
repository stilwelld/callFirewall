#!/usr/bin/env python3

import serial
import time
import pymysql
import json
import time
import logging
import socket
from logging.handlers import RotatingFileHandler
from os import listdir
from array import array
import requests
import bs4
import sys

# Definition of functions and classes


class Caller:
    def __init__(self):
        self.clearBuffer()

    def clearBuffer(self):
        self.date = ''
        self.time = ''
        self.nmbr = ''
        self.name = ''
        self.threat = ''
        self.country = ''
        self.location = ''
        self.center = ''
        self.company = ''


def dbUpdate(sql_str):
    try:
        db = pymysql.connect(host=cfg['mysql']['host'], user=cfg['mysql']
                             ['user'], passwd=cfg['mysql']['passwd'], db=cfg['mysql']['db'])
        cursor = db.cursor()
        cursor.execute(sql_str)
        db.commit()
        db.close()

    except pymysql.Error as e:
        try:
            logString = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            print(logString)
            app_log.info(logString)
        except IndexError:
            logString = "MySQL Error: %s" % str(e)
            print(logString)
            app_log.info(logString)

    logString = '>> Data is stored into database!'
    print(logString)
    app_log.info(logString)


def dbRead(sql_str):
    result = []
    try:
        db = pymysql.connect(host=cfg['mysql']['host'], user=cfg['mysql']
                             ['user'], passwd=cfg['mysql']['passwd'], db=cfg['mysql']['db'])
        cursor = db.cursor()
        cursor.execute(sql_str)
        result = cursor.fetchall()
        db.close()

    except pymysql.Error as e:
        try:
            logString = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            print(logString)
            app_log.info(logString)
        except IndexError:
            logString = "MySQL Error: %s" % str(e)
            print(logString)
            app_log.info(logString)

    logString = '>> Data is read from database!'
    print(logString)
    app_log.info(logString)
    return result


def notify(MESSAGE):
    for entry in cfg['notify']:
        (UDP_IP, UDP_PORT) = entry.split(':')
        sock = socket.socket(socket.AF_INET,   # Internet
                             socket.SOCK_DGRAM)	       # UDP
        sock.sendto(MESSAGE, (UDP_IP, int(UDP_PORT)))


def threat(caller):
    # check the block list and allow list to see if nmbr or name match
    level = '5'
    result = []
    print("Checking threat level for %s, %s" % (caller.nmbr, caller.name) )
    sql_str = "SELECT nmbr,name from block where nmbr='%s' or name='%s' " % (caller.nmbr, caller.name)
    result = dbRead(sql_str)
    logString = ">> Block result: "+str(result)
    print(logString)
    app_log.info(logString)
    if (result):
        level = '9'

    sql_str = "SELECT nmbr,name from allow where nmbr='%s' or name='%s' " % (caller.nmbr, caller.name)
    result = dbRead(sql_str)
    logString = ">> Allow result: "+str(result)
    print(logString)
    app_log.info(logString)
    if (result):
        level = '0'

	# Unknown caller
    if (level == '5'):
        # check public website
        r = requests.get(cfg['lookup'] + caller.nmbr)
        if (r.status_code == 200):
            html = bs4.BeautifulSoup(r.text,features="lxml")
            result = html.title.text
            if ("Complaints" in result):
                level = '7'
                print(">> lookup match")
                app_log.info(">> lookup match")
                print(result)
                app_log.info(result)
                # add entry to block table
                # Just add the nmbr to the table
                print(">> caller blocked")
                app_log.info(">> caller blocked")
                sql_str = "INSERT INTO block (nmbr,name) values ('%s','')" % (caller.nmbr)
                dbUpdate(sql_str)
        loc_info = html.ul
        for li in loc_info.find_all("li"):
            #print(li.text)
            #app_log.info(li.text)
            if ("Country" in li.text):
                caller.country = li.text.split(':')[1]
            if ("Location" in li.text):
                caller.location = li.text.split(':')[1]
            if ("Rate" in li.text):
                caller.center = li.text.split(':')[1]
            if ("Company" in li.text):
                caller.company = li.text.split(':')[1]
    caller.threat = level

def monitor(line_number, serial_port_path):
    time.sleep(int(line_number)*2)
    try:
        ser = serial.Serial(serial_port_path, 9600, timeout=None)
    except:
        print("Unable to open serial port")
        app_log.info("Unable to open serial port")
    # initialize modem and set caller-id flag
    time.sleep(1)
    ser.write(str.encode("\r\nATZ\r\n"))
    time.sleep(1)
    ser.write(str.encode("\r\nAT\x2bVCID\x3d1\r\n"))
    time.sleep(1)

    caller = Caller()

    while True:
        if ser.isOpen() == False:
            ser.open()
        try:
            re = ser.readline().decode()
            if re.rstrip() != '':
                print(re)
                app_log.info(re)

            if re[:4] == 'DATE':
                caller.date = re[7:].rstrip()

            if re[:4] == 'TIME':
                caller.time = re[7:].rstrip()

            if re[:4] == 'NMBR':
                caller.nmbr = re[7:].rstrip()

            if re[:4] == 'NAME':
                caller.name = re[7:].rstrip()
                # set the threat level for this caller
                threat(caller)
                logString = ">> "+caller.nmbr+" "+caller.name+" Date:" + \
                    caller.date+" Time:"+caller.time + " Threat:"+caller.threat+ \
                    " Country:"+caller.country +" Location:"+caller.location+" Company:"+caller.company
                print(logString)
                app_log.info(logString)
                sql_str = "INSERT INTO call_log (phone_line, date,time,nmbr,name,threat_level) \
					values ('%s','%s','%s','%s','%s','%s' )" % \
                    (str(line_number), caller.date, caller.time,
                 caller.nmbr, caller.name, caller.threat)
                dbUpdate(sql_str)
                if (caller.threat == '9'):
                    print(">> HANGUP")
                    app_log.info(">> HANGUP")
                    ser.write(str.encode("\r\nATH1\r\n"))
                    time.sleep(1)
                    ser.write(str.encode("\r\nATH0\r\n"))
                elif (caller.threat == '7'):
                    notify(b"warning robo caller")
                elif (caller.threat == '5'):
                    notify(b"unknown caller calling from "+caller.location )
                else:
                    # send a message to the announce server
                    notify(b"call from "+caller.name)
                caller.clearBuffer()

        except Exception as e:
            print(repr(e))


# Setup Logging
LOG_FILE = '/var/log/cidmon.log'
log_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=5*1024*1024, backupCount=2)
handler.setFormatter(log_formatter)
handler.setLevel(logging.INFO)

app_log = logging.getLogger('callid')
app_log .setLevel(logging.INFO)
app_log .addHandler(handler)

# Load the config file
global cfg
with open("/home/pi/.cfg.json") as json_data_file:
    cfg = json.load(json_data_file)

if (len(sys.argv) > 1):
    print("Running in test mode using " + sys.argv[1])
    app_log.info("Running in test mode using "+sys.argv[1])
    monitor(0, sys.argv[1])
    quit()

line_number = 1
# find the usb modem and call monitor
for serialPort in sorted(listdir("/dev/serial/by-path/")):
    portPath = "/dev/serial/by-path/" + serialPort
    print(portPath)
    app_log.info(portPath)
    # Example:
    # /dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0
    monitor(line_number, portPath)
