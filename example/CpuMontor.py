#!/usr/bin/python2.4
#_*_ coding: utf-8 _*_

'''
Last Modify: 2014/05/09
Version: 1.2
Description: Monitor Disk usage
Author: Victor
QQ:1409175531
'''

from sys import argv,exit
from decimal import Decimal
from optparse import OptionParser
from netsnmp import snmpwalk

parser = OptionParser('%prog -C -H -d -w -c ')

parser.add_option('-H', '--HostAddr', action='store', dest='hostaddress', help='Specify HostAddress')
parser.add_option('-C', '--community', action='store', dest='community', help='Specify host community')
parser.add_option('-d', '--device', action='store', dest='device', help='Specify a device')
parser.add_option('-w', '--warning', action='store', dest='warning', help='set the warning value')
parser.add_option('-c', '--critical', action='store', dest='critical', help='set the critical value')

(options, argvs) = parser.parse_args(argv)

desc_list = ['hrStorageDescr', 'hrStorageSize', 'hrStorageUsed', 'hrStorageAllocationUnits']

#���λ�ȡdesc_list��Ӧ�ķ���ֵ�����ֱ�����б�
try:
    for mibdsc in desc_list:
        r1 = list(snmpwalk(mibdsc,Version=2,Community=options.community,DestHost=options.hostaddress))
        if mibdsc == 'hrStorageDescr':
            dev = r1
        elif mibdsc == 'hrStorageSize':
            size = r1
        elif mibdsc == 'hrStorageUsed':
            used = r1
        elif mibdsc == 'hrStorageAllocationUnits':
            units = r1
except TypeError:
    parser.print_help()
    exit(3)
    
size_list = {}
used_list = {}
per_list = {}
print ('a');
for devname in dev:
    l = dev.index(devname) #���λ�ȡ��Ԫ�����б��λ��
    dev_size = int(size[l]) * int(units[l]) / 1024 / 1024 #������������λתΪM
    dev_used = int(used[l]) * int(units[l]) / 1024 / 1024
    used_percent = round(float(dev_used) / float(dev_size),2) * 100

    size_list[devname] = dev_size
    used_list[devname] = dev_used
    per_list[devname] = used_percent

if float(options.warning) > float(options.critical):
    print "-w <��ֵ> ������ڻ�С�� -c <��ֵ>"
    exit(3)
try:
    if float(per_list[options.device]) < float(options.warning):
        print 'OK - "%s" ʹ����:%s%% | ������:%s MB,��ʹ��:%s MB (w:%s%%, c:%s%%)' % (options.device, per_list[options.device], size_list[options.device], used_list[options.device], options.warning, options.critical)
        exit(0)
    elif float(options.critical) > float(per_list[options.device]) >= float(options.warning):
        print 'Warning - "%s" ʹ����:%s%% | ������:%s MB , ��ʹ��:%s MB (w:%s%%, c:%s%%)' % (options.device, per_list[options.device], size_list[options.device], used_list[options.device], options.warning, options.critical)
        exit(1)
    elif float(per_list[options.device]) >= float(options.critical):
        print 'Critical - "%s" ʹ����:%s%% | ������:%s MB , ��ʹ��:%s MB (w:%s%%, c:%s%%)' % (options.device, per_list[options.device], size_list[options.device], used_list[options.device], options.warning, options.critical)
        exit(2)
except KeyError:
    print '����Ӧ��ָ�����ļ�ϵͳ������'
    exit(3)