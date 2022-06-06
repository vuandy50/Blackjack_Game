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

"""Below this point is my BlackJackGame class. Everything above is header."""
from os import system, name
import time
import pickle
from .cards import Deck
from .player import BlackJackPlayer, ComputerDealer


def to_file(pickle_file, players):
    """Write the list players to the file pickle_file."""
    with open(pickle_file, "wb") as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


def from_file(pickle_file):
    """Reads pickle_file, decode it, and return it as players."""
    with open(pickle_file, "rb") as file_handle:
        players = pickle.load(file_handle)
    return players


def clear():
    """clears terminal"""
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def print_hand(hand):
    """Prints out Player's Hand"""
    num = len(hand)
    for i in range(num):
        print("Card {}: {}".format(i + 1, hand[i]))


def print_dealer(hand):
    """Prints out Dealer's Hand"""
    num = len(hand)
    for i in range(num):
        if i == 1:
            print("Card {}: ?".format(i + 1))
        else:
            print("Card {}: {}".format(i + 1, hand[i]))


def read_players():
    """Reads file and add it to player_l"""
    player_l = from_file("players.pckl")
    return player_l


def print_error():
    """Prints out Error Message"""
    clear()
    print()
    print("Your input is not valid. Please Try again...")
    print("------------------------------------------")


def table_view(game):
    """Table view of all players and dealer"""
    print("****BLACKJACK TABLE*****")
    print("------------------------")
    for i in range(len(game.players)):
        print("Regular Hand")
        print("{}){}".format(i + 1, game.players[i].get_n()))
        if i == len(game.players) - 1:
            print_dealer(game.players[i].get_hand())
        else:
            print_hand(game.players[i].get_hand())
            if game.players[i].check_split():
                print()
                print("Split Hand")
                print("{}){}".format(i + 1, game.players[i].get_n()))
                print_hand(game.players[i].get_split())
            print()
    print()


def final_table_view(game):
    """Shows cards of All Players"""
    print("****BLACKJACK TABLE*****")
    print("------------------------")
    for i in range(len(game.players)):
        print("    Regular Hand")
        print("{}){}".format(i + 1, game.players[i].get_n()), end="")
        value = game.deck.hand_value(game.players[i].get_hand())
        if value <= 21:
            print(" ---> {}".format(value))
        else:
            print(" ---> BUSTED")
        print_hand(game.players[i].get_hand())

        if i != game.n_o_p - 1:
            print("State: {}".format(game.players[i].get_state_one()))
            print_score(game, game.players[i].get_state_one(), i)
            if game.players[i].check_split():
                print()
                print("    Split Hand")
                print("{}){}".format(i + 1, game.players[i].get_n()), end="")
                value_split = game.deck.hand_value(game.players[i].get_split())
                if value_split <= 21:
                    print(" ---> {}".format(value_split))
                else:
                    print(" ---> BUSTED")
                print_hand(game.players[i].get_split())
                print("State: {}".format(game.players[i].get_state_two()))
                print_score_split(game, game.players[i].get_state_two(), i)
                print_insurance(game, i)
                print("Current Money: {}".format(game.players[i].get_money()))
            else:
                print_insurance(game, i)
                print("Current Money: {}".format(game.players[i].get_money()))
        print()


def print_score(game, string, index):
    """Prints out the score"""
    if string == "Winner":
        print(" + ${}".format(game.players[index].get_bet()))
    elif string == "Loser":
        print("- ${}".format(game.players[index].get_bet()))
    elif string == "Push":
        print("+ $0")


def print_score_split(game, string, index):
    """Prints out the split score"""
    if string == "Winner":
        print(" +${}".format(game.players[index].get_split_bet()))
    elif string == "Loser":
        print(" -${}".format(game.players[index].get_split_bet()))
    elif string == "Push":
        print(" +$0")


def print_insurance(game, index):
    """Prints out insurance score"""
    d_index = game.n_o_p - 1
    dealer = game.players[d_index]
    if game.players[index].is_there_insurance:
        if dealer.insurance_wins():
            insure = game.players[index].get_insurance()
            print("Insurance: +${}".format(insure))
            game.players[index].winner_insurance()
        else:
            insure = game.players[index].get_insurance()
            print("Insurance: -${}".format(insure))
            game.players[index].loser_insurance()


class BlackJack:
    """This is my BlackJack class"""

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.player_l = read_players()
        while True:
            try:
                self.n_o_p = int(input("How many player(1-4): "))
                if self.n_o_p in (1, 2, 3, 4):
                    break
                clear()
                print("Your input is not valid. Please Try again...")
            except ValueError:
                clear()
                print("Your input is not valid. Please Try again...")

        for i in range(self.n_o_p):
            self.form_players(i)
        self.players.append(ComputerDealer(self))
        self.n_o_p = self.n_o_p + 1

        index = 0
        clear()
        while index != self.n_o_p - 1:
            current_player = self.players[index]
            money = current_player.get_money()
            while True:
                try:
                    n_name = current_player.get_n()
                    print("{}'s current funds: ${}".format(n_name, money))
                    amount = int(input("How much do you want to bet: "))
                    if amount > money:
                        clear()
                        print("Invalid: Cannot bet more than you have.")
                    elif amount <= 0:
                        clear()
                        print("Invalid: Cannot bet 0 or less")
                    else:
                        current_player.betting(amount)
                        break
                except ValueError:
                    print_error()
            index = index + 1
        clear()

        self.deck.shuffle()
        print("Shuffling Deck...")
        time.sleep(2.5)
        self.deck.cut_deck()
        print("Cutting Deck...")
        time.sleep(2)
        for i in range(2):
            for j in range(self.n_o_p):
                player = self.players[j]
                player.add_to_hand(self.deck.deal())
                print("Dealing Card {} to {}".format(i + 1, player.get_n()))
                time.sleep(1.5)

    def write_players(self):
        """Saves players into pickle file"""
        player_list = []
        for i in range(len(self.player_l)):
            title = self.player_l[i][0]
            email = self.player_l[i][1]
            money = self.player_l[i][2]
            player_list.append([title, email, money])

        for i in range(len(self.players) - 1):
            title = self.players[i].get_n()
            email = self.players[i].get_email()
            money = self.players[i].get_money()
            if money > 0:
                player_list.append([title, email, money])
        to_file("players.pckl", player_list)

    def find_player(self, title, email):
        """Finds player in pickle file if exists"""
        for i in range(len(self.player_l)):
            n_name = self.player_l[i][0]
            e_email = self.player_l[i][1]
            m_money = self.player_l[i][2]
            if title == n_name and email == e_email:
                old_player = BlackJackPlayer(title, email)
                old_player.set_money(m_money)
                self.players.append(old_player)
                del self.player_l[i]
                return True
        return False

    def form_players(self, i):
        """Asks if a new or returning player"""
        flag = False
        while True:
            try:
                clear()
                print("Person {}".format(i + 1))
                print("Are you a new or a returning player?")
                print("1) New Player")
                print("2) Returning Player")
                selection = int(input("Choose an option: "))
                if selection == 1:
                    clear()
                    _n = input("Person {} -> Enter your name: ".format(i + 1))
                    _e = input("Person {} -> Enter your email: ".format(i + 1))
                    self.players.append(BlackJackPlayer(_n, _e))
                    flag = True
                elif selection == 2:
                    _n = input("Person {} -> Enter your name: ".format(i + 1))
                    _e = input("Person {} -> Enter your email: ".format(i + 1))
                    if self.find_player(_n, _e):
                        flag = True
                if flag:
                    break
                clear()
                print_error()
            except ValueError:
                clear()
                print_error()

    def new_game(self):
        """Starts a new game"""
        for i in range(len(self.players) - 1):
            self.players[i].reset()
        self.players[self.n_o_p - 1].reset_hand()

        index = 0
        clear()
        while index != self.n_o_p - 1:
            current_player = self.players[index]
            money = current_player.get_money()
            while True:
                try:
                    n_name = current_player.get_n()
                    print("{}'s current funds: ${}".format(n_name, money))
                    amount = int(input("How much do you want to bet: "))
                    if amount > money:
                        clear()
                        print("Invalid: Cannot bet more than you have.")
                    elif amount <= 0:
                        clear()
                        print("Invalid: Cannot bet 0 or less")
                    else:
                        current_player.betting(amount)
                        break
                except ValueError:
                    print_error()
            index = index + 1
        clear()

        self.deck.shuffle()
        print("Shuffling Deck...")
        time.sleep(2.5)
        self.deck.cut_deck()
        print("Cutting Deck...")
        time.sleep(2)
        for i in range(2):
            for j in range(self.n_o_p):
                player = self.players[j]
                player.add_to_hand(self.deck.deal())
                print("Dealing Card {} to {}".format(i + 1, player.get_n()))
                time.sleep(1.5)

    def check_funds(self):
        """Donates $10000 to players who have $0"""
        for i in range(len(self.players) - 1):
            if self.players[i].get_money() <= 0:
                self.players[i].set_money(10000)

    def run(self):
        """This run the BlackJack Game"""
        index = 0
        while True:
            try:
                if index == self.n_o_p - 1:
                    self.cpu_phase(index)
                    clear()
                    self.check_for_winner()
                    final_table_view(self)
                    while True:
                        print("{}, ".format(self.players[0].get_n()), end="")
                        y_n = input("Do you want to play again?(Y/N): ")
                        if y_n in ("Y", "y", "N", "n"):
                            break
                    if y_n in ("Y", "y"):
                        self.check_funds()
                        self.new_game()
                        index = 0
                    elif y_n in ("N", "n"):
                        print("Thanks for playing!")
                        self.check_funds()
                        self.write_players()
                        break
                else:
                    clear()
                    self.before_turn(index)
                    clear()
                    while True:
                        clear()
                        during = self.during_turn(index)
                        if during == 1:
                            self.players[index].add_to_hand(self.deck.deal())
                        elif during in (-2, -1, 2):
                            break
                    if self.players[index].check_split():
                        self.split_phase(index)
                    index = index + 1
            except ValueError:
                print_error()

    def before_turn(self, index):
        """Player can double down / split/ insurance"""
        player_n = self.players[index].get_n()
        player_hand = self.players[index].get_hand()
        value = self.deck.hand_value(player_hand)

        flag = True
        flags = [False, False, False]
        butt = [True, True, True]
        while flag:
            try:
                bet = self.players[index].get_bet()
                value = self.deck.hand_value(player_hand)
                table_view(self)
                print("Your turn {}!".format(player_n))
                print_hand(player_hand)
                print("Value: {}".format(value))
                print("Bet: ${}".format(bet))
                print("SELECT YOUR MOVE:")
                if value < 21:
                    if butt[0]:
                        flags[0] = self.double_down_check(index)
                    if butt[1]:
                        flags[1] = self.split_check(index)
                        if flags[1]:
                            butt[2] = False
                    if butt[2]:
                        flags[2] = self.insurance_check(index)
                else:
                    print("You reached 21! Press 4 to continue")
                print("4) Continue")
                move = int(input("Choose an option: "))
                flag, butt = self.check_before_move(index, move, flags, butt)
                clear()
            except ValueError:
                print_error()

    def before_turn_split(self, index):
        """Split card first then insurance"""
        player = self.players[index]
        player_n = self.players[index].get_n()
        player_hand = self.players[index].get_split()
        value = self.deck.hand_value(player_hand)

        flag = True
        flags = [False, False, False]
        butt = [False, False, True]
        while flag:
            try:
                bet = self.players[index].get_split_bet()
                table_view(self)
                print("Split turn {}!".format(player_n))
                print_hand(player_hand)
                print("Value: {}".format(value))
                print("Bet: ${}".format(bet))
                print("SELECT YOUR MOVE:")
                if value < 21:
                    if player.check_split():
                        if butt[2]:
                            flags[2] = self.insurance_check(index)
                else:
                    print("You reached 21! Press 4 to continue")
                print("4) Continue")
                move = int(input("Choose an option: "))
                flag, butt = self.check_before_move(index, move, flags, butt)
                clear()
            except ValueError:
                print_error()

    def double_down_check(self, index):
        """Checks if the player can double down"""
        player = self.players[index]
        if player.check_split():
            if player.can_double_split():
                print("1) Double Down")
                return True
        elif player.can_double():
            print("1) Double Down")
            return True
        else:
            print("*) Not enough funds to double down")
        return False

    def split_check(self, index):
        """Checks if the player can split"""
        player = self.players[index]
        if player.if_split():
            if player.can_double():
                print("2) Split")
                return True
            print("*) Not enough funds to split")
        return False

    def insurance_check(self, index):
        """Checks if Player can bet insurance"""
        dealer_card = self.players[self.n_o_p - 1].get_hand()
        player = self.players[index]

        if dealer_card[0].rank in ("Ace", "10", "Jack", "Queen", "King"):
            if player.is_there_money():
                print("3) Insurance")
                return True
            print("*) Not enough funds for insurance")
        return False

    def check_before_move(self, index, move, flags, button):
        """Performs double down / split / insurance based on player's move"""
        flag = True
        if move == 4:
            flag = False
        elif move == 1 and flags[0]:
            self.players[index].double()
            button[0] = False
        elif move == 2 and flags[1]:
            button[1] = False
            card_one = self.deck.deal()
            card_two = self.deck.deal()
            self.players[index].deal_split(card_one, card_two)
            self.players[index].betting_split()
        elif move == 3 and flags[2]:
            button[2] = False
            self.insurance_phase(index)
        print_error()
        return flag, button.copy()

    def during_turn(self, index):
        """Prompts player to hit or stand"""
        player_n = self.players[index].get_n()
        player_hand = self.players[index].get_hand()
        value = self.deck.hand_value(player_hand)
        bet = self.players[index].get_bet()
        while True:
            try:
                table_view(self)
                print("{}'s Turn".format(player_n))
                print_hand(player_hand)
                print("Value: {}".format(value))
                print("Bet: ${}".format(bet))
                if value < 21:
                    print("SELECT YOUR MOVE:")
                    print("1) Hit")
                    print("2) Stand")
                    move = int(input("Choose an option: "))
                    if move in (1, 2):
                        break
                    print_error()
                elif value == 21:
                    move = -1
                    print("You reached 21!")
                    break
                elif value > 21:
                    move = -2
                    print("You reached Busted!")
                    break
                clear()
            except ValueError:
                print_error()
        return move

    def during_turn_split(self, index):
        """Hit or Stand for split hand"""
        player_n = self.players[index].get_n()
        player_hand = self.players[index].get_split()
        value = self.deck.hand_value(player_hand)
        bet = self.players[index].get_split_bet()
        while True:
            try:
                table_view(self)
                print("{}'s Split Turn".format(player_n))
                print_hand(player_hand)
                print("Value: {}".format(value))
                print("Bet: ${}".format(bet))
                if value < 21:
                    print("SELECT YOUR MOVE:")
                    print("1) Hit")
                    print("2) Stand")
                    move = int(input("Choose an option: "))
                    if move in (1, 2):
                        break
                    print_error()
                elif value == 21:
                    move = -1
                    break
                elif value > 21:
                    move = -2
                    break
                clear()
            except ValueError:
                print_error()
        return move

    def split_phase(self, index):
        """Player's moves if they split"""
        clear()
        self.before_turn_split(index)
        clear()
        while True:
            clear()
            during = self.during_turn_split(index)
            if during == 1:
                self.players[index].add_to_split(self.deck.deal())
            elif during == 2:
                break
            elif during == -1:
                print("You reached 21!")
                break
            elif during == -2:
                break
            else:
                print_error()

    def cpu_phase(self, index):
        """Computer's Turn"""
        while True:
            clear()
            player_n = self.players[index].get_n()
            player_hand = self.players[index].get_hand()
            value = self.deck.hand_value(player_hand)

            table_view(self)
            if value < 21:
                print("{}'s Turn".format(player_n))
                print_hand(player_hand)
                print("Value: {}".format(value))
                print("SELECT YOUR MOVE:")
                print("1) Hit")
                print("2) Stand")
                print("Choose an option:", end="")
                if value >= 17 and self.check_busted():
                    self.players[index].slowprint(" 2")
                    break
                self.players[index].slowprint(" 1")
                self.players[index].add_to_hand(self.deck.deal())
            else:
                break

    def check_busted(self):
        """Checks all player if they bust"""
        dealer_card = self.players[self.n_o_p - 1].get_hand()
        value = self.deck.hand_value(dealer_card)
        for i in range(len(self.players)):
            if self.deck.hand_value(self.players[i].get_hand()) > 21:
                return True
            if self.deck.hand_value(self.players[i].get_hand()) <= value:
                return True
        return False

    def check_for_winner(self):
        """Check all player if they Win/Lose/Push"""
        index = 0
        d_index = self.n_o_p - 1
        dealer = self.players[d_index]
        while True:
            player = self.players[index]
            player_hand = player.get_hand()
            if dealer.check_players_hand(player_hand) == 1:
                player.set_state_one("Winner")
                player.winner()
            elif dealer.check_players_hand(player_hand) == 2:
                player.set_state_one("Push")
            else:
                player.set_state_one("Loser")
                player.loser()
            index = index + 1
            if index == d_index:
                self.check_for_split_winners()
                break

    def check_for_split_winners(self):
        """Checks all splits if they win/Lose/Push"""
        index = 0
        d_index = self.n_o_p - 1
        dealer = self.players[d_index]
        while True:
            player = self.players[index]
            player_hand = player.get_split()
            if player.check_split():
                if dealer.check_players_hand(player_hand) == 1:
                    player.set_state_two("Winner")
                    player.winner_split()
                elif dealer.check_players_hand(player_hand) == 2:
                    player.set_state_two("Push")
                else:
                    player.set_state_two("Loser")
                    player.loser_split()
            index = index + 1
            if index == d_index:
                break

    def insurance_phase(self, index):
        """If player chooses to have insurance"""
        clear()
        player = self.players[index]
        money = player.get_money() - player.get_bet() - player.get_split_bet()
        while True:
            try:
                print("{}'s current funds: ${}".format(player.get_n(), money))
                amount = int(input("How much do you want to bet: "))
                if amount > money:
                    clear()
                    print("Invalid: Cannot bet more than you have.")
                elif amount <= 0:
                    clear()
                    print("Invalid: Cannot bet 0 or less")
                else:
                    player.betting_insurance(amount)
                    break
            except ValueError:
                print_error()
        clear()
