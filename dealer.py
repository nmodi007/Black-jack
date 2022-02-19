#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from card import Card
from hand import Hand
from record import Record
from tray import Tray
from collections import deque
from player import Decision, Player, Status
from random import randint
from blackjack_utility import any_ace_in_hand, best_total, hand_busted, hard_total, is_natural_blackjack, hand_values
import unittest

bet = 10


class Dealer:

    def __init__(self):
        self._hand = Hand()
        self.status = Status.Still_playing
        self.bank = [0]  # dealer balance

    def deal(self, players, tray):
        '''
        The dealer will deal the cards to the number of players and 
        to the dealer himself. the number of players must be at least one 
        and not more than 8.

        Parameters
        ----------
        players : iterable of player objects.

        tray : tray to deal cards from.

        Returns
        -------
        None.

        '''
        if len(players) < 1 or len(players) > 8:
            raise ValueError("Must have between 1 to 8 players.")

        if not len(tray):
            raise ValueError("Tray must not be empty")

        # +1 for dealer. 2 per player.
        num_cards_to_deal = (len(players) + 1) * 2
        line = deque(players + [self])

        for player in players:
            player.hands.appendleft(Hand())

        for filp in range(num_cards_to_deal):
            # # get a card from the tray and give it to the first
            # # person in line.
            if isinstance(line[0], Player):
                line[0].hands[0].cards.extend(tray.deal())
            else:
                line[0]._hand.cards.extend(tray.deal())
            line.rotate(-1)  # next person in line.

    def play(self, players, tray):
        players_queue = deque(players)
        while players_queue:
            player = players_queue.popleft()
            while player.hands:
                hand = player.hands.popleft()

                if len(hand) == 1:
                    # should happen after split.
                    hand.cards.extend(tray.deal())

                player_has_natural_balckjack = is_natural_blackjack(hand)
                dealer_has_natural_balckjack = is_natural_blackjack(self._hand)

                if player_has_natural_balckjack and dealer_has_natural_balckjack:
                    new_balance = player.balance[-1]
                    player.balance.append(new_balance)
                    player.records.append(
                        Record(hand, self._hand, Status.Push, new_balance))
                    self.bank.append(self.bank[-1])
                    continue
                if player_has_natural_balckjack and not dealer_has_natural_balckjack:
                    new_balance = player.balance[-1] + bet * 1.5
                    player.balance.append(new_balance)
                    player.records.append(
                        Record(hand, self._hand, Status.Win, new_balance))
                    self.bank.append(self.bank[-1] - bet * 1.5)
                    continue
                if not player_has_natural_balckjack and dealer_has_natural_balckjack:
                    new_balance = player.balance[-1] - bet
                    player.balance.append(new_balance)
                    player.records.append(
                        Record(hand, self._hand, Status.Lose, new_balance))
                    self.bank.append(self.bank[-1] + bet)
                    continue

                # dealer and the player don't have a black jack
                while True:
                    player_decision = player.decide3(hand, self._hand[1])

                    if player_decision == Decision.Hit:
                        hand.cards.extend(tray.deal())
                        if hand_busted(hand):
                            new_balance = player.balance[-1] - bet
                            player.balance.append(new_balance)
                            player.records.append(
                                Record(hand, self._hand, Status.Busted, new_balance))
                            self.bank.append(self.bank[-1] + bet)
                            break
                        else:  # we have an ace
                            continue  # make decision again.
                    elif player_decision == Decision.Stay:
                        player.staying_hands.append(hand)
                        break
                    elif player_decision == Decision.Double:
                        hand.cards.extend(tray.deal())
                        if hand_busted(hand):
                            new_balance = player.balance[-1] - bet
                            player.balance.append(new_balance)
                            player.records.append(
                                Record(hand, self._hand, Status.Busted, new_balance))
                            self.bank.append(self.bank[-1] + bet)
                            break
                    else:  # split
                        left_hand = Hand([hand[0], tray.deal()[0]])
                        right_hand = Hand([hand[1]])
                        player.hands.appendleft(right_hand)
                        player.hands.appendleft(left_hand)
                        break

        # Dealer makes his decision.
        while True:
            dealer_decision = self._decide()
            if dealer_decision == 'hit':
                self._hand.cards.extend(tray.deal())
                if hand_busted(self._hand):
                    self.status = Status.Busted
                    break
                else:
                    continue
            else:  # stay
                break

        # If dealer busted, players who stayed, win.
        if self.status == Status.Busted:
            for player in (p for p in players if p.staying_hands):
                while player.staying_hands:
                    hand = player.staying_hands.popleft()
                    new_balance = player.balance[-1] + bet
                    player.balance.append(new_balance)
                    player.records.append(
                        Record(hand, self._hand, Status.Win, new_balance))
                    self.bank.append(self.bank[-1] - bet)

        else:
            dealer_score = best_total(self._hand)
            for player in (p for p in players if p.staying_hands):
                while player.staying_hands:
                    hand = player.staying_hands.popleft()
                    player_score = best_total(hand)
                    if player_score > dealer_score:
                        new_balance = player.balance[-1] + bet
                        player.balance.append(new_balance)
                        player.records.append(
                            Record(hand, self._hand, Status.Win, new_balance))
                        self.bank.append(self.bank[-1] - bet)
                    elif player_score < dealer_score:
                        new_balance = player.balance[-1] - bet
                        player.balance.append(new_balance)
                        player.records.append(
                            Record(hand, self._hand, Status.Lose, new_balance))
                        self.bank.append(self.bank[-1] + bet)
                    else:
                        new_balance = player.balance[-1]
                        player.balance.append(new_balance)
                        player.records.append(
                            Record(hand, self._hand, Status.Push, new_balance))
                        self.bank.append(self.bank[-1])

        for player in players:
            if player.hands or player.staying_hands:
                raise Exception(
                    'players hands and stayings hands must be empty when play is over.')

        self._hand = Hand()
        self.status = Status.Still_playing

    def _decide(self):
        if any_ace_in_hand(self._hand):
            if best_total(self._hand) >= 17 and best_total(self._hand) <= 21:
                return 'stay'
            else:
                return 'hit'
        else:
            if hard_total(self._hand) <= 16:
                return 'hit'
            else:
                return 'stay'

    def __repr__(self):
        return 'dealer hand:\n\t' + '\n'.join(card for card in self._hand)


def main():
    pass


class DealerTests(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer()
        self.tray = Tray()
        self.players = [Player() for i in range(3)]
        self.cards = [Card('clubs', '7'),  # p1
                      Card('clubs', 'A'),  # p2
                      Card('clubs', '6'),  # p3
                      Card('clubs', '5'),  # D
                      Card('clubs', '5'),  # p1
                      Card('clubs', '8'),  # p2
                      Card('clubs', '5'),  # p3
                      Card('clubs', '10')]  # D

        # D(5, 10) --> hits Dealer is showing a 10.
        # p1(7, 5) --> hits
        # p2(A, 8) --> stays
        # p3(6, 5) --> double

        self.tray._cards.extend(reversed(self.cards))
        self.dealer.deal(self.players, self.tray)

    def test_deal(self):

        self.assertEqual(self.players[0].hands[0].cards[0], self.cards[0])
        self.assertEqual(self.players[0].hands[0].cards[1], self.cards[4])

        self.assertEqual(self.players[1].hands[0].cards[0], self.cards[1])
        self.assertEqual(self.players[1].hands[0].cards[1], self.cards[5])

        self.assertEqual(self.players[2].hands[0].cards[0], self.cards[2])
        self.assertEqual(self.players[2].hands[0].cards[1], self.cards[6])

        self.assertEqual(self.dealer._hand[0], self.cards[3])
        self.assertEqual(self.dealer._hand[1], self.cards[7])

    def test_play(self):
        self.dealer.play(self.players, self.tray)

    # def test_play(self):
    #     self.dealer.play(self.players, self.tray)
if __name__ == '__main__':
    unittest.main()
    # main()
