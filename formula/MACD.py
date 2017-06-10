from formula.Formula import EMA

# MACD
class DATA():
    def __init__(self, diff, dea):
        self.Set(diff, diff, dea)

    def Set(self, diff, dea):
        self.diff = diff;
        self.dea = dea;
        self.macd = 2 * (self.diff - self.dea);

    def __str__(self):
        return 'diff={0},dea={1},macd={2}'.format(self.diff, self.dea, self.macd);

class MACD():
    def __init__(self, short=12, long=26, diff=9):
        self.EMAShort = [];
        self.EMALong = [];
        self.EMADEA = [];
        self.DIFFS = [];
        self.short = short;
        self.diff = diff;
        self.long = long;

    def Input(self, klines):
        prices = klines.prices;
        EMA(klines.prices, self.EMAShort, self.short);
        EMA(klines.prices, self.EMALong, self.long);
         
        ld = len(self.DIFFS);
        lr = len(self.EMAShort) - ld;
        for idx in range(ld, dr - 1):
            DIFFS.append(self.EMAShort[idx] - self.EMALong[idx]);
        EMA(self.DIFFS, self.EMADEA, self.diff);
    
    def Get(index):
        return DATA(self.DIFFS[index], self.EMADEA[index])

    def __str__(self):
        str = '';
        l = len(self.EMAShort);
        for k in range(0, l):
            str = str + self.Get(indx).__str__() + '\n';
        return str;
