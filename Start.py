import time
import urllib2
import sys
import socket
import threading

from exchange.Exchange import Exchange
from exchange.yunbiEX import yunbiEX

from exchange.chbtcEX import chbtcEX

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

from Time import Time
from Log import Log

exchange = Exchange(RebotConfig.access_key, RebotConfig.secret_key);
exchange.delegate(chbtcEX());

#print exchange.getServerTimestamp();
#print exchange.getUser();
print exchange.getK('btccny', 2, 60, 1504598400000);
#print exchange.getOrder('btscny');
#print exchange.doOrder('btscny', 'buy', 0.1, 100);
#print exchange.getOrder('btscny');
#print exchange.doOrderCancel(2017090420479642, 'btscny');
#print exchange.getOrder('btscny');
