# callFirewall
Raspberry Pi application to monitor/block calls on a telephone line.

## Parts list

* Raspberry pi 3 or 4.
* USB modem https://www.amazon.com/dp/B00XW5QYWS?psc=1&ref=ppx_yo2_dt_b_product_details
* SD card, minimum 32gb
* power supply, be sure to use at least a 2.5 amp given you have to power the modem
* USB speaker or attached AMP

## Components

* callFirewall.py

Main application using a USB modem to access callier-id informatiaon and to drop in-progress calls.

* ttsd.py

Daemon program that listens for call announcements. Announcements are played using gtts.

* nodeapp

A nodejs web gui to allow you to view and manage call data.

## setup

Boot your Raspberry Pi using the Raspberry Pi OS Lite image.
Configure your network and enable SSH.

Clone the software and install needed packages.
```sh
$ git clone git@github.com:stilwelld/callFirewall.git
$ sudo apt-get update
$ sudo apt-get install socat
$ sudo apt-get install python3-pymysql
$ sudo apt-get install python3-requests
$ sudo apt-get install python3-bs4
$ sudo apt-get install mariadb-server
$ sudo apt-get install mpg321
$ pip3 install gtts

$ sudo touch /var/log/cidmon.log
$ sudo chown pi /var/log/cidmon.log

$ sudo mysql_secure_installation
```

Just follow the prompts to set a password for the root user and to secure your MySQL installation.

For a more secure installation, you should answer “Y” to all prompts when asked to answer “Y” or “N“.

These prompts will remove features that allows someone to gain access to the server easier.

## Setup the DB
Where it says 'password' change this to whatever password you want to use.
```sh
# mysql -u root -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 60
Server version: 10.3.31-MariaDB-0+deb10u1 Raspbian 10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> CREATE DATABSE callid;
MariaDB [(none)]> use callid
Database changed
MariaDB [callid]> CREATE USER 'pi'@'localhost' IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.004 sec)

MariaDB [callid]> GRANT ALL PRIVILEGES on callid.* TO 'pi'@'localhost';
Query OK, 0 rows affected (0.005 sec)

MariaDB [callid]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.004 sec)

MariaDB [callid]>
```

Create the database tables:
```sh
$ mysql -p callid < mysql_setup.sql
Enter password:
```
## copy the config sample and update the MySQL password
```sh
$ cp cfg-sample.json ~/.cfg.json
$ vi ~/.cfg.json
$ vi nodeapp/database.js
```

## setup nodejs

Install the nodejs and npm packages, then use npm to install the dependencies.
```sh
sudo apt-get install nodejs npm
cd callFirewall/nodeapp
npm install
```

## Testing

Use the socat command to start up a tty device to simulate the modem.

```sh
$ socat -d -d pty,raw,echo=0 pty,raw,echo=0

2021/10/25 08:16:18 socat[6502] N PTY is /dev/pts/2
2021/10/25 08:16:18 socat[6502] N PTY is /dev/pts/3
2021/10/25 08:16:18 socat[6502] N starting data transfer loop with FDs [5,5] and [7,7]
```
In another window start up the callFirewall in test mode by passing in the second pts device
```sh 
$ ./callFirewall.py /dev/pts/3
```
Open another window to simulate calls, use the sendCallid.sh script passing in the first pts device
```sh
$ ./sendCallid.sh /dev/pts/2 2029983262 spam caller
```
* This call should be flagged as a spam caller and added to the block table.

In another window start up the website
```sh
$ ./nodeapp/bin/www
```
Open a web brower and go to http://raspberrypi:3000 or whatever hostname you used to setup your pi.
If your server does not support local name resolution can you use the IP address of the Pi.

You should see the main page with the caller statistics. From here you you view the call log, block list and contacts.

<p align="center">
<img src="https://raw.githubusercontent.com/stilwelld/callFirewall/master/images/stats.png"
  alt="statistics page">
</p>

Call logs

<p align="center">
<img src="https://raw.githubusercontent.com/stilwelld/callFirewall/master/images/call_log.png"
  alt="call logs page">
</p>

Blocked callers

<p align="center">
<img src="https://raw.githubusercontent.com/stilwelld/callFirewall/master/images/blocked.png"
  alt="blocked callers page">
</p>

Contacts

<p align="center">
<img src="https://raw.githubusercontent.com/stilwelld/callFirewall/master/images/contacts.png"
  alt="contas page">
</p>
