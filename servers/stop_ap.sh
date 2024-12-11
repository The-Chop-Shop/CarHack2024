#!/bin/bash

# Disable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=0

# Remove NAT rule
sudo iptables -t nat -D POSTROUTING -s 192.168.2.0/24 -o eth0 -j MASQUERADE
# Stop hostapd (AP)
sudo systemctl stop hostapd

# Stop dnsmasq (DHCP/DNS)
sudo systemctl stop dnsmasq

# Remove the static IP from wlan0
sudo ip addr del 192.168.2.1/24 dev wlan0

# Re-enable wlan0 for NetworkManager management
sudo nmcli dev set wlan0 managed yes

echo "Access Point Stopped"
