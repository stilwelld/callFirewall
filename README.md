# callFirewall
Raspberry Pi application to monitor/block calls on a telephone line.

### Components

callFirewall.py

Main application using a USB modem to access callier-id informatiaon and to drop in-progress calls.

ttsd.py

Daemon program that listens for call announcements. Announcements are played using gtts.

nodeapp

A web gui to allow you to view and manage call data.
