# bot config.
# yunbi user config
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

    # user
    user_asset_ratio = 4;
    user_asset_least = 200;
    user_initamount = 785;
    # exchange
    exchange = 'chbtc';
    # rebot
    rebot_period = 240; # min
    rebot_buy_least_angle = 5;
    rebot_trade_sure_times = 1;
    rebot_do_per_period = 5;
    rebot_release = False;
    rebot_is_test = True;
    rebot_test_k_count = 200;
    rebot_test_begin = 1502006400000;

    rebot_loss_ratio = -10;
    rebot_profit_ratio = -20;
    rebot_yunbi_markets = [{'id':'ltccny'}];#[{'id':'btccny'}, {'id':'ltccny'}, {'id':'ethcny'}, {'id':'etccny'}, {'id':'btscny'}]#[{'id':'luncny'}];
    # file
    path = 'C:\\Users\\randy\\';
    log = 'log.txt';
