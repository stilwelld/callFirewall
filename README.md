# callFirewall
Raspberry Pi application to monitor/block calls on a telephone line.

## Components

callFirewall.py

Main application using a USB modem to access callier-id informatiaon and to drop in-progress calls.

ttsd.py

Daemon program that listens for call announcements. Announcements are played using gtts.

nodeapp

A web gui to allow you to view and manage call data.

## setup

sudo apt-get update
git clone git@github.com:stilwelld/callFirewall.git
sudo apt-get install socat
sudo apt-get install python3-pymysql
sudo apt-get install python3-requests
sudo apt-get install python3-bs4
sudo touch /var/log/cidmon.log
sudo chown pi /var/log/cidmon.log

sudo apt-get install mariadb-server
sudo mysql_secure_installation

## setup nodejs

sudo apt-get install nodejs npm
cd nodeapp
npm install

edit database.js to update the mysql password

## Setup the DB

root@robo:/home/pi/callFirewall# mysql -u root -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 60
Server version: 10.3.31-MariaDB-0+deb10u1 Raspbian 10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> use callid
Database changed
MariaDB [callid]> CREATE USER 'pi'@'localhost' IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.004 sec)

MariaDB [callid]> GRANT ALL PRIVILEGES on callid.* TO 'pi'@'localhost';
Query OK, 0 rows affected (0.005 sec)

MariaDB [callid]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.004 sec)

MariaDB [callid]>

mysql -p callid < mysql_setup.sql
Enter password:

### update the password stored in the cfg.json
cp cfg-sample.json ~/.cfg.json
vi ~/cfg.json
vi ~/nodeapp/database.js

## Testing

Use the socat command to start up a tty device to simulate the modem.

$ socat -d -d pty,raw,echo=0 pty,raw,echo=0

2021/10/25 08:16:18 socat[6502] N PTY is /dev/pts/2
2021/10/25 08:16:18 socat[6502] N PTY is /dev/pts/3
2021/10/25 08:16:18 socat[6502] N starting data transfer loop with FDs [5,5] and [7,7]

In another window start up the callFirewall passing in the second pts device

$ ./callFirewall.py /dev/pts/3

Open another window to simulate calls, use the sendCallid.sh script passing in the first pts device

$ ./sendCallid.sh /dev/pts/2 2029983262 spam caller

This call should be flagged as a spam caller and added to the block table.

In another window start up the website

$ ./nodeapp/bin/www

Open a web brower and go to http://raspberrypi:3000

