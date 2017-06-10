from lib.client import Client, get_api_path
from formula.K import K
from formula.MACD import MACD
from formula.Formula import EMA
from BotConfig import BotConfig
from data.Database import Database

import MySQLdb
import sys
import time;

# this is your access key and secret key
client = Client(access_key=BotConfig.access_key, secret_key=BotConfig.secret_key)
# first update data .db
db = Database();
KLines = K();
KMACD = MACD();
KLines.Add(db.Get('qtum', 'k', ));
KMACD.Add(db.Get('qtum', 'macd'));
# 
while False:
    time.sleep(3);
    d = client.get(get_api_path('k'), params={'market': 'qtumcny', 'period' : '1'});
    print d;

# last k.
lastK = None;
if len(KLines.data) > 0 :
    lastK = KLines.data[-1];
d = None;
if lastK:
    d = client.get(get_api_path('k'), params={'market': 'qtumcny', 'limit' : '1000', 'period' : '30', 'timestamp' : '{0}'.lastK.t});
else:
    d = client.get(get_api_path('k'), params={'market': 'qtumcny', 'limit' : '1000', 'period' : '30'});
KLines.Input(d);
KMACD.Input(KLines.data);

print KLines.data[1];
db.Add("qtum", "k", KLines.data);
db.Add("qtum", "macd", KMACD.data);


db.Close();