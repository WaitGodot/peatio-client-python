import MySQLdb
import sys
import time

# db
db = MySQLdb.connect("localhost", "randy", "randy521");
cursor=None
if db:
    cursor = db.cursor();
else:
    print "can not connect the mysql!!";
    sys.exit(1);

# create database bot;
cursor.execute("drop database bot;")
cursor.execute("create database bot default charset utf8 collate utf8_general_ci;")
cursor.execute("use bot;")

# build market tables; 
# unix time like 2017-06-06 19:52:00
cursor.execute('''create table markets (
	id INT NOT NULL AUTO_INCREMENT,
	market varchar(11) NOT NULL,
	openTime timestamp NOT NULL,
	PRIMARY KEY (id)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;''');

markets = [ ["QTUM", "2017-05-24 08:00:00"] ];
for k, cfg in enumerate(markets):
    print cfg[0], cfg[1];
    cursor.execute('''INSERT INTO markets
    	(market, openTime) VALUES ("{0}", {1}) '''.format(cfg[0], time.mktime(time.strptime(cfg[1], '%Y-%m-%d %H:%M:%S'))));

# commit and close
db.commit();
cursor.close();
db.close();