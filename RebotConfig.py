# bot config.
# yunbi user config
import time;
class RebotConfig():
    # access key
    access_key = "3fc30d76-816a9502-5cbb933f-fd3f8";
    # secret key
    secret_key = "c587548c-0c1bf226-a45d8913-1de46";

    # mysql config
    mysql_address = "localhost";
    mysql_user = "randy";
    mysql_password = "randy521";
    mysql_database = "bot";
    #data
    data_need_load = False;
    # user
    user_asset_ratio = 6;
    user_asset_least = 250;
    user_initamount = 2400;
    user_least_vol = 0.00001;
    # exchange
    exchange = 'huobi';#'chbtc';
    base_currency = 'usdt';
    # rebot
    rebot_period = 120; # min
    rebot_buy_least_angle = 5;
    rebot_trade_sure_times = 1;
    rebot_do_per_period = 120;
    rebot_release = True;
    rebot_is_test = False;
    rebot_test_k_count = 1000;
    rebot_test_begin = time.time() - rebot_test_k_count * 2 / (24 * 60 / rebot_period) * 24*60*60; #1502006400;

    rebot_loss_ratio = -7;
    rebot_profit_ratio = -10;
    rebot_trade_markets = []#[{'id':'etcusdt'}, {'id':'btcusdt'}, {'id':'bchusdt'},{'id':'ethusdt'},{'id':'ltcusdt'},{'id':'eosusdt'},{'id':'xrpusdt'},{'id':'omgusdt'},{'id':'dashusdt'},{'id':'zecusdt'},{'id':'htusdt'}];#[{'id':'603688'}];#[{'id':'603998'}, {'id':'603997'}]; #[{'id':'btccny'}, {'id':'ltccny'}, {'id':'ethcny'}, {'id':'etccny'}, {'id':'btscny'}]#[{'id':'luncny'}];
    # rebot_trade_markets = [{'id':'ltcusdt'}];
    # file
    path = ''
    log = 'log.txt';
