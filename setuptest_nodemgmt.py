import nodemgmt as n
ser = n.initcmd('/dev/ttyUSB0',20)
#ser = n.initcmd('/dev/ttyUSB1',12)


node0 = n.node('test','0013a20041033e85',log='logfile.log')
c6 = n.node('C6','0013a20040e495a7',log='logfile.log')
