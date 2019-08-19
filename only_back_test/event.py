class Event:
    """
    Event类的基类
    """
    pass


class MarketEvent(Event):
    """
    将新的市场数据注册为Event, 由Strategy对象处理
    """

    def __init__(self):
        """
        Initialises the MarketEvent.
        """
        self.type = 'MARKET'


class SignalEvent(Event):
    """
    将Strategy类产生的Single注册为Event, 由Portfolio对象处理
    """

    def __init__(self, symbol, datetime, signal_type):
        """
        Initialises the SignalEvent.

        Parameters:
        symbol - The ticker symbol, e.g. 'GOOG'.
        datetime - The timestamp at which the signal was generated.
        signal_type - 'LONG' or 'SHORT'.
        """

        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type


class OrderEvent(Event):
    """
    将Portfolio产生的Single注册为Event, 由 执行系统(execution system) 处理
    The order contains a symbol (e.g. GOOG), a type (market or limit), quantity and a direction.
    """

    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initialises the order type, setting whether it is
        a Market order ('MKT') or Limit order ('LMT'), has
        a quantity (integral) and its direction ('BUY' or
        'SELL').

        Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market or Limit.
        quantity - Non-negative integer for quantity.
        direction - 'BUY' or 'SELL' for long or short.
        """

        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        打印到屏幕或日志
        """
        print("Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" % (self.symbol, self.order_type, self.quantity, self.direction))


class FillEvent(Event):
    """
    计算下单需要的数据, 包括 数量, 价格, 交易费用等
    将 订单 产生的Single注册为Event, 由 下单系统 处理
    """

    def __init__(self, timeindex, symbol, exchange, quantity,
                 direction, fill_cost, commission=None):
        """
        Initialises the FillEvent object. Sets the symbol, exchange,
        quantity, direction, cost of fill and an optional
        commission.

        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.

        Parameters:
        timeindex - The bar-resolution when the order was filled.  下单时间
        symbol - The instrument which was filled.  证券代码
        exchange - The exchange where the order was filled.  交易所
        quantity - The filled quantity.  数量
        direction - The direction of fill ('BUY' or 'SELL') 买卖方向
        fill_cost - The holdings value in dollars. 成本
        commission - An optional commission sent from IB.  手续费
        """

        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculate commission
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission

    def calculate_ib_commission(self):
        """
        当未传入手续费时, 自动计算出一个手续费, 根据各个交易所情况不同, 有不同的默认值
        招商证券:
            手续费: 0.06%, 最低5块
            印花税: 0.1%
        """
        min_service_change = 5
        service_change_percent = 0.0006
        stamp_tax_percent = 0.001

        service_change = max(min_service_change, service_change_percent * self.fill_cost)
        stamp_tax = stamp_tax_percent * self.fill_cost
        full_cost = service_change + stamp_tax

        return full_cost
