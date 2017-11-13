# bot config.
# yunbi user config
import time;

DAY = {
    60 : 4,
    240 : 1,
    1680 : 0.14,
}

class RebotConfig():
    # access key
    access_key = "N1vXgZ0wSrTkLjgzG1oli4aD10DDRQW9gYxkHljW";
    # secret key
    secret_key = "Xgz0QqlvdAx9lBjpiVLlnFOs2IwaPS3lftuw4geS";

    # mysql config
    mysql_address = "localhost";
    mysql_user = "randy";
    mysql_password = "randy521";
    mysql_database = "bot";
    #data
    data_need_load = False;
    # user
    user_asset_ratio = 10;
    user_asset_least = 10000;
    user_initamount = 1000000;
    # exchange
    exchange = 'tushare';#'chbtc';
    # rebot
    rebot_period = 1680; # min
    rebot_buy_least_angle = 5;
    rebot_trade_sure_times = 1;
    rebot_do_per_period = 5;
    rebot_release = False;
    rebot_is_test = True;
    rebot_test_k_count = 100;
    rebot_test_begin = time.time() - rebot_test_k_count / DAY[rebot_period] *24*60*60; #1502006400;

    rebot_loss_ratio = -10;
    rebot_profit_ratio = -20;
    rebot_yunbi_markets = []#[{'id':'603688'}, {'id':'603998'}];#[{'id':'603998'}, {'id':'603997'}]; #[{'id':'btccny'}, {'id':'ltccny'}, {'id':'ethcny'}, {'id':'etccny'}, {'id':'btscny'}]#[{'id':'luncny'}];
    # file
    path = 'C:\\Users\\randy\\';
    log = 'log.txt';
