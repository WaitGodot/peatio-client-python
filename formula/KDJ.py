'''
以KDJ(9,3,3) 为例:
RSV(9)=（今日收盘价－9日内最低价）÷（9日内最高价－9日内最低价）×100
K(3日)=（当日RSV值+2×前一日K值）÷3
D(3日)=（当日K值+2×前一日D值）÷3
J=3K－2D （这里应该是3k而不是3d）
如果无前一日的K、D值，K、D初始值取50。
'''

class KDJ():
   def __init__(self, N1 = 9, N2 = 3, N3 = 3):
       self.N1 = N1;
       self.N2 = N2;
       self.N3 = N3;
       self.hightArr = [];

    def Input(self, klines):
        rsv = 