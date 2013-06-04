# -*- coding: utf-8 -*-

import bitcoinrpc


class Wallet(object):
    """
    It's a wallet. It holds some kind of money.
    """
    def __init__(self, currency):
        self.money = 0.0
        self.currency = currency


class BTCWallet(Wallet):
    """
    This wallet holds your bitcoins
    """
    def __init__(self, address):
        super(BTCWallet, self).__init__(currency='btc')
        pass


class EuroWallet(Wallet):
    """
    This wallet holds your hardware coins also named Euros
    """
    def __init__(self):
        super(EuroWallet, self).__init__(currency='euro')
        pass
