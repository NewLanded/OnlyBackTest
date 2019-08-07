from abc import ABCMeta, abstractmethod


class Strategy:
    """Strategy is an abstract base class providing an interface for
    all subsequent (inherited) trading strategies.

    The goal of a (derived) Strategy object is to output a list of signals,
    which has the form of a time series indexed pandas DataFrame.

    In this instance only a single symbol/instrument is supported."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_signals(self):
        """
        An implementation is required to return the DataFrame of symbols
        containing the signals to go long, short or hold (1, -1 or 0).

        return: DataFrame

                    signal
        trade_date
        2016-01-04     0.0
        2016-01-05     0.0
        2016-01-06     0.0
        2016-01-07     0.0
        2016-01-08     0.0
        2016-01-11     1.0
        2016-01-12     1.0
        """
        raise NotImplementedError("Should implement generate_signals()!")


class Portfolio:
    """
    一个抽象类, 根据Strategy类发出的信号, 实现证券投资组合的功能(包括功能和现金管理)
    An abstract base class representing a portfolio of
    positions (including both instruments and cash), determined
    on the basis of a set of signals provided by a Strategy.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_positions(self):
        """
        在预测信号和可用现金的基础上, 决定证券投资组合的分配
        Provides the logic to determine how the portfolio
        positions are allocated on the basis of forecasting
        signals and available cash.
        """
        raise NotImplementedError("Should implement generate_positions()!")

    @abstractmethod
    def backtest_portfolio(self):
        """
        提供生成订单和净值曲线的逻辑, 并且依据 投资组合的分配 的情况, 处理持仓, 现金和区间收益

        Provides the logic to generate the trading orders
        and subsequent equity curve (i.e. growth of total equity),
        as a sum of holdings and cash, and the bar-period returns
        associated with this curve based on the 'positions' DataFrame.

        Produces a portfolio object that can be examined by
        other classes/functions.
        """
        raise NotImplementedError("Should implement backtest_portfolio()!")
