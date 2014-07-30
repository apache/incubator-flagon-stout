#!/usr/bin/env bash

sudo iptables -I INPUT 5 -m state --state NEW -m tcp -p tcp --dport 8000 -j ACCEPT -m comment --comment "SimpleHTTPServer"
sudo iptables -I INPUT 5 -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT -m comment --comment "LoggingServer1"
sudo iptables -I INPUT 5 -m state --state NEW -m tcp -p tcp --dport 1337 -j ACCEPT -m comment --comment "LoggingServer2"
sudo /sbin/service iptables save
sudo /sbin/service iptables restart