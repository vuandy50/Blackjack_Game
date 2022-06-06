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

"""Below this point is my Die class. Everything above is header."""
from collections import namedtuple
from random import shuffle, randrange


Card = namedtuple("Card", ["rank", "suit"])


def print_card(card):
    """Prints out card nicely"""
    return "{} of {}".format(card.rank, card.suit)


Card.__str__ = print_card


class Deck:

    """This function initializes class Deck"""

    def __init__(self):
        self.ranks = (
            ["Ace"]
            + list(map(str, list(range(2, 11))))
            + "Jack Queen King".split()
        )
        self.suits = "Clubs Hearts Spades Diamonds".split()
        self.cards = []
        self.set_values()
        self.new_deck()

    def shuffle(self, num=1):
        """Shuffles the list of cards"""
        index = 0
        while index < num:
            shuffle(self.cards)
            index = index + 1

    def check_number_cards(self):
        """Checks if the deck has greater than 80 cards left"""
        return len(self.cards) > 80

    def new_deck(self):
        """Create a new deck"""
        self.cards = [
            Card(rank, suit)
            for rank in self.ranks
            for suit in self.suits
            for i in range(8)
        ]

    def set_values(self):
        """Sets the values of each card"""
        self.values = list(range(1, 11)) + [10, 10, 10]
        self.value_dict = dict(zip(self.ranks, self.values))
        self.value_dict.update({"Ace": [1, 11]})

    def __str__(self):
        """Prints out card nicely"""
        return "\n".join(
            ["{} {}".format(i, j) for i, j in enumerate(self.cards)]
        )

    def cut_deck(self):
        """Cuts the deck at the 60 - 80 card from the bottom"""
        index = randrange(60, 81)
        top_half = self.cards[:index]
        bottom_half = self.cards[index:]
        self.cards = bottom_half + top_half

    def deal(self):
        """Returns a card from the deck"""
        return self.cards.pop()

    def hand_value(self, hand):
        """Calculates the Max value of a hand"""
        total_value = 0
        num_cards = len(hand)
        for i in range(num_cards):
            if hand[i].rank == "Ace":
                card_one = self.value_dict[hand[i].rank][0]
                card_two = self.value_dict[hand[i].rank][1]
                if total_value + self.value_dict[hand[i].rank][1] > 21:
                    total_value = total_value + card_one
                else:
                    total_value = total_value + card_two
            else:
                total_value = total_value + self.value_dict[hand[i].rank]
        return total_value
