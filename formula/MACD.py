from formula.Formula import EMA

# MACD
class DATA():
    def __init__(self):
        self.diff = 0;
        self.dea = 0;
        self.macd = 0;

    def Set(self, diff, dea):
        self.diff = diff;
        self.dea = dea;
        self.macd = 2 * (self.diff - self.dea);
    def __str__(self):
        return 'diff={0},dea={1},macd={2}'.format(self.diff, self.dea, self.macd);

class MACD():
    def __init__(self):
        self.data = [];

    def Input(self, KS):
        arr = []
        for idx, value in enumerate(KS):
            arr.append(value.c);
        ema12s = EMA(arr, 12);
        ema26s = EMA(arr, 26);
        diffs = [];
        for idx, value in enumerate(ema12s):
            diffs.append(ema12s[idx] - ema26s[idx]);
        deas = EMA(diffs, 9);
        for idx, value in enumerate(ema12s):
            d = DATA();
            d.Set(diffs[idx], deas[idx]);
            self.data.append(d);

    def __str__(self):
        str = '';
        for k, v in enumerate(self.data):
            str = str + v.__str__() + '\n';
        return str;
