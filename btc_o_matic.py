#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
btc-o-matic

Usage:
  btc_o_matic.py [--testnet] [-v | --verbose]
  btc_o_matic.py (-h | --help)
  btc_o_matic.py --version

Options:
  --testnet      Use the testnet instead of the real bitcoin network.
  -v, --verbose  Print the amount of money and bitcoins in the btc-o-matic.
  -h, --help     Show this screen.
  --version      Show version.
"""

__author__ = "Ricardo (XeN) Band, Ansgar (ansi) Schmidt"
__copyright__ = "Copyright 2013, c-base e.V."
__credits__ = ["Ricardo Band", "Ansgar Schmidt"]
__license__ = "GPLv3+"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "btc-o-matic@xengi.de"
__status__ = "Development"

import os
import sys
import time
import json
import urllib
import threading

#import PIL
import pygame
import docopt
#import qrcode
#import jsonrpclib
from pygame.locals import QUIT, \
                          DOUBLEBUF, \
                          FULLSCREEN, \
                          KEYDOWN, \
                          K_ESCAPE, \
                          MOUSEBUTTONDOWN

import btc_o_matic.wallet as Wallet

pygame.init()
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
FONT = pygame.font.Font('freesansbold.ttf', 28)

class ChartDownloader(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.url = 'http://api.bitcoincharts.com/v1/markets.json'

    def run(self):
        """
        Updates the exchange rate to the current value from bitcoincharts.com
        """
        while True:
            # if the mashine is idling we update the rates
            if self.parent.state == 'idle':
                self.parent.state = 'update'
                #opener = urllib.FancyURLopener({})
                #f = opener.open(self.url)
                #charts = json.loads(f.read())
                #markets = [market for market in charts
                #           if market[u'currency'] == u'EUR'
                #           and market[u'volume'] > 10]
                #ask_numerator = sum(market[u'ask'] * market[u'volume'] for market in markets)
                #bid_numerator = sum(market[u'bid'] * market[u'volume'] for market in markets)
                #divisor = sum(market[u'volume'] for market in markets)
                #self.parent._ask = (ask_numerator / divisor) if divisor != 0 else None
                #self.parent._bid = (bid_numerator / divisor) if divisor != 0 else None
                self.parent._ask = 23.421337 + time.time() / 1000000
                self.parent._bid = 42.231337 + time.time() / 1000000
                self.parent._last_update = time.time()

                # reset to idle state and wait for the next update
                self.parent.state = 'idle'
                time.sleep(900)
            else:
                # there is a transaction going on atm so we wait a little bit
                # more before we update the rates
                time.sleep(60)


class BTCOMatic(object):
    """
    Main class which holds this and that and does this and that.
    """
    def __init__(self, testnet=False, verbose=False):
        """
        Initialize main class with this and that.
        """
        self._fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((800, 600), DOUBLEBUF)
        pygame.display.set_caption('btc-o-matic')

        self._testnet = testnet
        self._verbose = verbose
        self._last_update = 0
        self._bid = 0
        self._ask = 0

        #TODO: read wallet ids from config file
        self._btcwallet = Wallet.BTCWallet('o-matic')
        self._eurowallet = Wallet.EuroWallet()
        self._chartdl = ChartDownloader(self)
        self._chartdl.setDaemon(True)

        self.state = 'idle'

    def loop(self):
        """
        Queries for user interaction and serves cool things.
        """

        self._chartdl.start()
        while self.state:
            # first handle events
            self.handle_events()

            # then update whats needed
            self.update()

            # now redraw everything
            self.render()

    def handle_events(self):
        """
        Get all events and react to them.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
            elif event.type == MOUSEBUTTONDOWN:
                pass

    def update(self):
        """
        Update all the things related to the events that just happened.
        """
        pass

    def render(self):
        """
        Render the scene to te screen.
        """
        # painting a black background
        self.surface.fill(BLACK)

        # display the current time
        time_surface = FONT.render(time.strftime('%H:%M:%S'), False, WHITE)
        time_rect = time_surface.get_rect()
        time_rect.midtop = (self.surface.get_width() / 2, 10)
        self.surface.blit(time_surface, time_rect)

        # display last update
        lupdate_surface = FONT.render(time.strftime('%H:%M:%S',
                                                    time.gmtime(self._last_update)),
                                      False, WHITE)
        lupdate_rect = lupdate_surface.get_rect()

        if self._verbose:
            # display the wallets
            wallet1_surface = FONT.render('Euro:  %f' % self._eurowallet.money,
                                          False, WHITE)
            wallet1_rect = wallet1_surface.get_rect()
            wallet1_rect.bottomleft = (0, self.surface.get_height())
            self.surface.blit(wallet1_surface, wallet1_rect)

            wallet2_surface = FONT.render('BTC: %f' % self._btcwallet.money,
                                      False, WHITE)
            wallet2_rect = wallet2_surface.get_rect()
            wallet2_rect.bottomleft = (0, wallet1_rect.top - 2)
            self.surface.blit(wallet2_surface, wallet2_rect)

            wallet3_surface = FONT.render('Wallets:', False, WHITE)
            wallet3_rect = wallet3_surface.get_rect()
            wallet3_rect.bottomleft = (0, wallet2_rect.top - 2)
            self.surface.blit(wallet3_surface, wallet3_rect)

        if self.state == 'update':
            # display update text
            update_surface = FONT.render('Updating..', False, WHITE)
            update_rect = update_surface.get_rect()
            update_rect.bottomright = (self.surface.get_width(),
                                       self.surface.get_height())
            self.surface.blit(update_surface, update_rect)
        else:
            # draw current bitcoin rate
            rate1_surface = FONT.render('Ask: %f' % self._ask, False, WHITE)
            rate1_rect = rate1_surface.get_rect()
            rate1_rect.bottomright = (self.surface.get_width(),
                                      self.surface.get_height())
            self.surface.blit(rate1_surface, rate1_rect)

            rate2_surface = FONT.render('Bid: %f' % self._bid, False, WHITE)
            rate2_rect = rate2_surface.get_rect()
            rate2_rect.bottomright = (self.surface.get_width(),
                                      rate1_rect.top - 2)
            self.surface.blit(rate2_surface, rate2_rect)

            rate3_surface = FONT.render('Current rates:', False, WHITE)
            rate3_rect = rate3_surface.get_rect()
            rate3_rect.bottomright = (self.surface.get_width(),
                                      rate2_rect.top - 2)
            self.surface.blit(rate3_surface, rate3_rect)

        #TODO: draw menu items

        # updating the screen and finally drawing it
        pygame.display.update()
        pygame.display.flip()
        self._fps_clock.tick(3)


if __name__ == '__main__':
    ARGS = docopt.docopt(__doc__, version='btc-o-matic v%s' % __version__)
    APP = BTCOMatic(testnet=ARGS['--testnet'], verbose=ARGS['--verbose'])
    sys.exit(APP.loop())
