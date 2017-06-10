# rule
from lib.client import Client, get_api_path
from formula.K import K
from formula.MACD import MACD
from BotConfig import BotConfig

class Rule():
    def __init__(self, market, period):
    	self.market = market;
        self.period = period;
        self.KLines = K();
        self.MACD = MACD();
        self.client = Client(access_key=BotConfig.access_key, secret_key=BotConfig.secret_key)

    def Run():
        d = client.get(get_api_path('k'), params={'market': '{0}'.format(self.market), 'period' : '{0}'.format()});
        self.KLines.Input(d);
        self.MACD.Input(self.KLines);
