import time
import urllib2
import sys
import socket
import threading
import os
from exchange.Exchange import Exchange
from exchange.yunbiEX import yunbiEX

from formula.K import KLine
from formula.MACD import MACD
from formula.Formula import SMA
from formula.Formula import MA
from formula.Formula import EMA
from formula.Formula import HIGH
from formula.Formula import LOW
from RebotConfig import RebotConfig
from rule.Rule import Rule
from rule.MutliMovingAverage import MutliMovingAverage
from user.User import User
from Rebot import Rebot;
from exchange.yunbi.client import Client, get_api_path
from exchange.yunbiEX import yunbiEXLocal
from exchange.huobiEX import huobiEX
from Time import Time
from Log import Log

STATUS = "running";
stop = 'stop'

socket.setdefaulttimeout(6);
r = Rebot(RebotConfig.rebot_period);

OrderFile = '%s%s' %(RebotConfig.path, 'orders.txt'); 

def ClearOrderFile():
   if os.path.exists(OrderFile):
        os.remove(OrderFile);

def WriteOrder(content):
   f = open(OrderFile,'a');
   f.write('%s\n' % content)
   f.close();

def Exoprt():
    alltradetimes = 0;
    allwintimes = 0;
    alluncompeletetimes = 0;
    ClearOrderFile();

    for k,v in enumerate(r.markets):
        market = v['id'];
        ods = r.user.getOrderMarket(market);
        lenods = len(ods);
        if lenods > 0:
            buys = [];
            tradetimes = 0;
            wintimes = 0;
            uncompeletetimes = 0
            WriteOrder('market:%s' % market);
            key=0;
            for k,v in enumerate(ods):
                if v.type == 'buy':
                    tradetimes += 1;
                    alltradetimes += 1;
                    buys.append(v);
                if v.type == 'sell':
                    WriteOrder('\t%s' % v);
                    for bk, bv in enumerate(buys):
                        scale = 0;
                        if bv.averageprice > 0 :
                            scale = round((v.averageprice - bv.averageprice)/bv.averageprice * 100, 2);
                        if scale > 0:
                            wintimes += 1;
                            allwintimes += 1;
                        WriteOrder('\t\tscale:%s, %s' % (scale, bv.__str__()));
                        key = k;
                    buys = [];
            if len(buys) > 0:
                WriteOrder('\tcurrent buy order:')
                for k,v in enumerate(buys):
                    uncompeletetimes += 1;
                    alluncompeletetimes += 1;
                    WriteOrder('\t\t%s' % v.__str__());
            if tradetimes - uncompeletetimes > 0 :
                WriteOrder('\twinner: %f, win: %d, uncompelete %d, all %d\n' % (float(wintimes)/ float(tradetimes - uncompeletetimes) * 100, wintimes, uncompeletetimes, tradetimes));
            else:
                WriteOrder('\twinner: %f, win: %d, uncompelete %d, all %d\n' % (0, wintimes, uncompeletetimes, tradetimes));
    if alltradetimes <= 0:
        WriteOrder('none trade')
    if alltradetimes - alluncompeletetimes > 0:
        WriteOrder('all win: %f, win: %d, uncompelete %d, all %d\n' % (float(allwintimes)/ float(alltradetimes - alluncompeletetimes) * 100, allwintimes, alluncompeletetimes, alltradetimes));

    import csv
    f = open('%sscales.csv' % RebotConfig.path, 'wb');
    w = csv.writer(f);
    w.writerow(['scale']);
    for k in range(0, len(r.scales)):
        w.writerow([k, r.scales[k]]);
    f.close();


def Done():
    # Log.d('\nstart rebot %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Time.Time())));
    t = 0;
    while True:
        global STATUS;
        if STATUS == 'stop':
            break;
        t += 1;
        # print "rebot status %s, do %d, time : %s" % (STATUS, t, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Time.Time())));
        stop = r.run();
        # print '------------------------------------------------------------------------'
        if RebotConfig.rebot_is_test:
            if t > RebotConfig.rebot_test_k_count or stop == True:
                break;
        if t % 10 == 0:
            Exoprt();
       #  else:
       #     print 'sleep time', 6; #RebotConfig.rebot_period*60/RebotConfig.rebot_do_per_period;
       #     time.sleep(6);
            # time.sleep(RebotConfig.rebot_period*60/RebotConfig.rebot_do_per_period);
Done();
Exoprt();
'''
nr = threading.Thread(target=Done);
nr.start();

while True:
    try:
        STATUS = input('STATUS:');
        if STATUS == 'stop':
            break;
    except Exception:
        print ''
'''
