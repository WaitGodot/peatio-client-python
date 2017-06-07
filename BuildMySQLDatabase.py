import MySQLdb
import sys
import time
import math
from BotConfig import BotConfig;
# db
db = MySQLdb.connect(BotConfig.mysql_address, BotConfig.mysql_user, BotConfig.mysql_password);
cursor=None
if db:
    cursor = db.cursor();
else:
    print "can not connect the mysql!!";
    sys.exit(1);

# create database bot;
cursor.execute("drop database {0};".format(BotConfig.mysql_database))
cursor.execute("create database {0} default charset utf8 collate utf8_general_ci;".format(BotConfig.mysql_database))
cursor.execute("use {0};".format(BotConfig.mysql_database))

# build market tables; 
# unix time like 2017-06-06 19:52:00
cursor.execute('''create table markets (
	id INT NOT NULL AUTO_INCREMENT,
	market varchar(11) NOT NULL,
	openTime datetime NOT NULL,
	PRIMARY KEY (id)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;''');

markets = BotConfig.markets;
for k, cfg in enumerate(markets):
    name = cfg[0];
    # market info
    cursor.execute('INSERT INTO markets (market, openTime) VALUES ("{0}", "{1}")'.format(name, time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(cfg[1], '%Y-%m-%d %H:%M:%S'))));
    # market kline
    cursor.execute('''create table {0}_k (
        id INT NOT NULL AUTO_INCREMENT,
        time timestamp NOT NULL default CURRENT_TIMESTAMP,
        o FLOAT NOT NULL,
        h FLOAT NOT NULL,
        l FLOAT NOT NULL,
        c FLOAT NOT NULL,
        increase FLOAT NOT NULL,
        amplitude FLOAT NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(name));
    #market macd
    cursor.execute('''create table {0}_macd (
        id INT NOT NULL AUTO_INCREMENT,
        time timestamp NOT NULL default CURRENT_TIMESTAMP,
        diff FLOAT NOT NULL,
        dea FLOAT NOT NULL,
        macd FlOAT,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8'''.format(name));

# commit and close
db.commit();
cursor.close();
db.close();


