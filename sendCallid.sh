#!/bin/bash

tty=$1;shift
nmbr=$1;shift

date=`date +%m%d`
time=`date +%H%M`

exec > $tty
echo "RING" 
sleep 1
echo "DATE = $date" 
echo "TIME = $time" 
echo "NMBR = $nmbr" 
echo "NAME = $*" 
sleep 1 
echo "RING" 
sleep 1
echo "RING" 


