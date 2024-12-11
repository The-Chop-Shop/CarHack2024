#!/bin/bash

# Disable wlan0 from NetworkManager control (stop managing)
sudo nmcli dev set wlan0 managed no

# Enable IP forwarding if not already enabled
if [ "$(sysctl -n net.ipv4.ip_forward)" -eq 0 ]; then
    sudo sysctl -w net.ipv4.ip_forward=1
fi

# Check if NAT rule is present; add it if it's missing
if ! sudo iptables -t nat -C POSTROUTING -s 192.168.2.0/24 -o eth0 -j MASQUERADE 2>/dev/null; then
    sudo iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -o eth0 -j MASQUERADE
fi

# Start hostapd (AP)
sudo systemctl start hostapd

# Start dnsmasq (DHCP/DNS)
sudo systemctl start dnsmasq

# Set the static IP for wlan0
sudo ip addr add 192.168.2.1/24 dev wlan0

echo "Access Point Started"
