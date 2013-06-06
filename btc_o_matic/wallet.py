# -*- coding: utf-8 -*-

import bitcoinrpc

class Wallet(object):
    """
    It's a wallet. It holds some kind of money.
    """
    def __init__(self, currency):
        self.currency = currency

class BTCWallet(Wallet):
    """
    This wallet holds your bitcoins
    """

    def __init__(self, address):
        super(BTCWallet, self).__init__(currency = 'btc')
        self.conn = bitcoinrpc.connect_to_local()

    def get_temp_wallet_address(self):
        return str(self.conn.getnewaddress())

    def get_balance_on_address(self, address):
        return self.conn.getreceivedbyaddress(address)

    def is_available(self):
        availability = True
    
        if self.conn:
            if self.conn.getconnectioncount() < 5:
               availability = False
        return availability

    def is_address_valid(self, address):
        av = self.conn.validateaddress(address)
        return av.isvalid

    def get_balance(self):
        return self.conn.getbalance()

    def transfer_amount(self, address, amount):
        self.conn.sendtoaddress(address, amount)
        pass

class EuroWallet(Wallet):
    """
    This wallet holds your hardware coins also named Euros
    """
 
    def __init__(self):
        super(EuroWallet, self).__init__(currency='euro')
        self.money = 23.02 
        pass

    def get_balance(self):
        return self.money

    def deposit(self, amount):
        self.money += amount

    def withdraw(self, amount):
        if self.money < amount:
           raise NotEnoughtBalanceError()
        self.money -= amount

class NotEnoughtBalanceError(Exception):
    def __init__(self):
        pass

