# callFirewall
Raspberry Pi application to monitor/block calls on a telephone line.

### Components

callFirewall.py

Main application using a USB modem to access callier-id informatiaon and to drop in-progress calls.

ttsd.py

Daemon program that listens for call announcements. Announcements are played using gtts.

nodeapp

A web gui to allow you to view and manage call data.

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
