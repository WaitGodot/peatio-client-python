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

KLines.extend(db.Get('qtum', 'k', ));
KMACD.extend(db.Get('qtum', 'macd'));
# 
while True:
    time.sleep(3);


d = client.get(get_api_path('k'), params={'market': 'qtumcny', 'limit' : '10000', 'period' : '30', 'timestamp' : '1495584000'});
KS = [];
for k, v in enumerate(d):
    KS.append(K(v));
macd.Input(KS);

print KS[1];
db.add("qtum", "k", KS);
db.add("qtum", "macd", macd.data);


db.close();