#!/usr/bin/env python3
# Andy Vu
# CPSC 386-04
# 2022-03-01
# avu53@csu.fullerton.edu
# @vuandy50
#
# Lab 07-00
#
# This program runs a Blackjack game.
#

"""Below is my Player classes. Everything above is header."""
import sys
import time
from .cards import Deck


class Player:
    """Player has a name and hand"""

    def __init__(self, name, email):
        """Initializes Player"""
        self.name = name
        self.hand = []
        self.split_hand = []
        self.state_one = ""
        self.state_two = ""
        self.email = email
        self.money = 10000

    def get_n(self):
        """Returns Player's Name"""
        return self.name

    def get_hand(self):
        """Returns Player's Hand"""
        return self.hand

    def add_to_hand(self, card):
        """Adds to Player's Hand"""
        self.hand.append(card)

    def reset_hand(self):
        """Clears Player's Hand"""
        self.hand.clear()

    def add_to_split(self, card):
        """Adds to Player's Split Hand"""
        self.split_hand.append(card)

    def get_split(self):
        """Returns Player's Split Hand"""
        return self.split_hand

    def reset_split(self):
        """Clears Player's Split Hand"""
        self.split_hand.clear()

    def if_split(self):
        """When the player have the same rank"""
        card_one = self.hand[0].rank
        card_two = self.hand[1].rank
        if card_one == card_two:
            return True
        return False

    def check_split(self):
        """Checks if there is a split hand"""
        return len(self.split_hand) != 0

    def deal_split(self, c_one, c_two):
        """Deals the split hand"""
        card_two = self.hand[1]
        self.hand.pop()
        self.add_to_split(card_two)
        self.add_to_hand(c_one)
        self.add_to_split(c_two)

    def get_state_one(self):
        """Win/Lose/Push State of hand"""
        return self.state_one

    def set_state_one(self, string):
        """Set Win/Lose/Push State of hand"""
        self.state_one = string

    def get_state_two(self):
        """Win/Lose/Push State of split hand"""
        return self.state_two

    def set_state_two(self, string):
        """Set Win/Lose/Push State of split hand"""
        self.state_two = string

    def get_money(self):
        """Return total money"""
        return self.money

    def set_money(self, money):
        """Sets money"""
        self.money = money

    def get_email(self):
        """Return total email"""
        return self.email


class BlackJackPlayer(Player):
    """Blackjack Player"""

    def __init__(self, name, email):
        """Initalizes BlackjackPlayer"""
        super().__init__(name, email)
        self.bet = 0
        self.bet_split = 0
        self.bet_insurance = 0

    def betting_split(self):
        """Set split hand bet"""
        self.bet_split = self.bet

    def get_split_bet(self):
        """Returns the split bet"""
        return self.bet_split

    def betting(self, bet):
        """Inital Bet"""
        self.bet = bet

    def get_bet(self):
        """Returns inital bet"""
        return self.bet

    def double(self):
        """Doubles inital bet"""
        self.bet = self.bet * 2

    def hypothetical_money(self):
        """Calculates all bets if lose"""
        return self.money - self.bet - self.bet_split - self.bet_insurance

    def can_double(self):
        """Is there enough money to double"""
        return self.money >= self.bet * 2

    def can_double_split(self):
        """Is there enough money to split"""
        return self.money >= self.bet + self.bet_split

    def is_there_money(self):
        """Is there enough money"""
        return self.hypothetical_money() > 0

    def reset(self):
        """Resets Bet"""
        self.bet = 0
        self.bet_split = 0
        self.bet_insurance = 0
        self.reset_split()
        self.reset_hand()

    def winner(self):
        """When the player wins"""
        self.money = self.money + self.bet

    def loser(self):
        """When the player loses"""
        self.money = self.money - self.bet

    def winner_split(self):
        """When the player wins with split"""
        self.money = self.money + self.bet_split

    def loser_split(self):
        """When the player loses with split"""
        self.money = self.money - self.bet_split

    def winner_insurance(self):
        """When the player wins with insurance"""
        self.money = self.money + self.bet_insurance

    def loser_insurance(self):
        """When the player loses with insurance"""
        self.money = self.money - self.bet_insurance

    def push(self):
        """When the player ties"""
        self.reset()

    def betting_insurance(self, insurance):
        """Set insurance bet"""
        self.bet_insurance = insurance

    def get_insurance(self):
        """Return insurance bet"""
        return self.bet_insurance

    def is_there_insurance(self):
        """Checks if player bet insurance"""
        return self.bet_insurance > 0


class ComputerDealer(Player):
    """Computer Dealer Player"""

    def __init__(self, game):
        """Initializes Computer Dealer"""
        super().__init__("Dealer", "")
        self._game = game
        self.deck = Deck()

    def check_players_hand(self, hand):
        """Checks if player's hand vs dealer's hand"""
        dealer_hand = self.deck.hand_value(self.hand)
        player_hand = self.deck.hand_value(hand)
        checker = 1
        if player_hand > 21:
            checker = 0
        elif player_hand < dealer_hand <= 21:
            checker = 0
        elif dealer_hand == 21 and len(self.get_hand()) == 2:
            if player_hand == 21 and len(hand) == 2:
                checker = 1
            checker = 0
        elif dealer_hand == player_hand:
            checker = 2
        return checker

    def insurance_wins(self):
        """Insurance wins when dealer has 21 without hitting"""
        dealer_hand = self.deck.hand_value(self.hand)
        return dealer_hand == 21 and len(self.get_hand()) == 2

    @staticmethod
    def slowprint(string):
        """Slow prints CPU actions"""
        for cha in string + "\n":
            sys.stdout.write(cha)
            sys.stdout.flush()
            time.sleep(2)
