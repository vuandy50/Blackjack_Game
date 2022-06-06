#!/usr/bin/env python3
# Andy Vu
# CPSC 386-04
# 2022-03-28
# avu53@csu.fullerton.edu
# @vuandy50
#
# Lab 07-00
#
# This program runs a Blackjack game.
#

"""Below this point is the main code. Everything above is header."""

from blackjack import game


def main_run():
    """This function will run the BlackJack Game"""
    start_game = game.BlackJack()
    start_game.run()


if __name__ == "__main__":
    main_run()
