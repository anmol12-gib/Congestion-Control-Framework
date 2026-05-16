#!/usr/bin/python

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.link import TCLink

def create_realistic_topology():
    net = Mininet_wifi()
    info("*** Adding Controller\n")
    c0 = net.addController('c0')
    info("*** Adding 6G IoT Nodes\n")
    iot1 = net.addStation('iot1', ip='10.0.0.1/8')
    iot2 = net.addStation('iot2', ip='10.0.0.2/8')
    info("*** Adding Edge Server\n")
    edge = net.addHost('edge', ip='10.0.0.3/8')
    info("*** Adding 6G gNodeB\n")
    bs1 = net.addAccessPoint('bs1', ssid='6G-Net', mode='g', channel='1')
    info("*** Configuring Wireless Environment\n")
    net.configureWifiNodes()
    info("*** Creating Wireless Links\n")
    net.addLink(iot1, bs1)
    net.addLink(iot2, bs1)
    info("*** Creating Wired Backhaul\n")
    net.addLink(bs1, edge, cls=TCLink, bw=2, delay='20ms')
    info("*** Starting Network\n")
    net.build()
    c0.start()
    bs1.start([c0])
    info("*** Opening Lab Command Line\n")
    CLI(net)
    info("*** Stopping Network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_realistic_topology()