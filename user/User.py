# user
#
#
from user.Order import Order
class User():
    def __init__(self):
        self.amount = 0; # 持有现金
        self.positions = []; # 持仓
        self.undone = []; # 未完成订单

