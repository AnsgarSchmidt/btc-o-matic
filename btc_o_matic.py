#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
btc-o-matic

Usage:
  btc_o_matic.py
  btc_o_matic.py (-h | --help)
  btc_o_matic.py --version

Options:
  -h, --help    Show this screen.
  --version     Show version.
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

import PIL
import pygame
import docopt
import qrcode
from pygame.locals import QUIT, \
                          DOUBLEBUF, \
                          FULLSCREEN, \
                          KEYDOWN, \
                          K_ESCAPE, \
                          MOUSEBUTTONDOWN

import btc_o_matic.wallet as Wallet


class MainClass(object):
    """
    Main class which holds this and that and does this and that.
    """
    def __init__(self, testnet=False):
        """
        Initialize main class with this and that.
        """
        pygame.init()
        self._fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((800, 600), DOUBLEBUF)
        pygame.display.set_caption('btc-o-matic')

        self._testnet = testnet
        self._last_update = 0
        self._rate = None       # 1 EUR is x BTC

        #TODO: read wallet ids from config file
        self._btcwallet = Wallet.BTCWallet('o-matic')
        self._eurowallet = Wallet.EuroWallet()

        self._running = True

    def loop(self):
        """
        Queries for user interaction and serves cool things.
        """
        col_black = pygame.Color(0, 0, 0)
        col_white = pygame.Color(255, 255, 255)

        font = pygame.font.Font('freesansbold.ttf', 22)

        while self._running:
            # first handle events
            self.eventhandler()

            # react to them and do awesome stuff

            # get the latest btc exchange rate every 10 minutes
            if self._last_update < time.time() - 600:
                self.update_rate()
                self._last_update = time.time()

            # painting a black background
            self.surface.fill(col_black)

            # add stuff to the display

            #TODO: stuff

            # display the current time
            time_surface = font.render(time.strftime('%H:%M:%S'), False, col_white)
            time_rect = time_surface.get_rect()
            time_rect.midtop = (self.surface.get_width() / 2, 10)
            self.surface.blit(time_surface, time_rect)

            # display the wallets
            wallet1_surface = font.render('Euro:  %d' % self._eurowallet.money,
                                              False, col_white)
            wallet1_rect = wallet1_surface.get_rect()
            wallet1_rect.bottomleft = (0, self.surface.get_height())
            self.surface.blit(wallet1_surface, wallet1_rect)

            wallet2_surface = font.render('BTC: %d' % self._btcwallet.money,
                                             False, col_white)
            wallet2_rect = wallet2_surface.get_rect()
            wallet2_rect.bottomleft = (0, wallet1_rect.top - 2)
            self.surface.blit(wallet2_surface, wallet2_rect)

            wallet3_surface = font.render('Wallets', False, col_white)
            wallet3_rect = wallet3_surface.get_rect()
            wallet3_rect.bottomleft = (0, wallet2_rect.top - 2)
            self.surface.blit(wallet3_surface, wallet3_rect)

            # draw current bitcoin rate
            rate1_surface = font.render('###.#####', False, col_white)
            rate1_rect = rate1_surface.get_rect()
            rate1_rect.bottomright = (self.surface.get_width(),
                                      self.surface.get_height())
            self.surface.blit(rate1_surface, rate1_rect)

            rate2_surface = font.render('Current rate:', False, col_white)
            rate2_rect = rate2_surface.get_rect()
            rate2_rect.bottomright = (self.surface.get_width(),
                                      rate1_rect.top -2)
            self.surface.blit(rate2_surface, rate2_rect)


            # updating the screen and finally drawing it
            pygame.display.update()
            pygame.display.flip()
            self._fps_clock.tick(30)

    def eventhandler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
            elif event.type == MOUSEBUTTONDOWN:
                pass

    def update_rate(self):
        """
        Updates the exchange rate to the current value from bitcoincharts.com
        """
        self._rate = 1

if __name__ == '__main__':
    ARGS = docopt.docopt(__doc__, version='btc-o-matic v%s' % __version__)
    APP = MainClass(testnet=True)
    sys.exit(APP.loop())
