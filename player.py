#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import unittest
from card import Card
from blackjack_utility import any_ace_in_hand, best_total, hand_busted
from blackjack_utility import hard_total
from collections import deque

import enum

import pickle


class Status(enum.Enum):
    Win = 1
    Busted = 2  # when hand goes over 21.
    Lose = 3  # you stay and dealer gets higher score.
    Push = 4
    # still in the game. If the player is staying and waiting for the dealer.
    Still_playing = 5


class Decision(enum.Enum):
    Hit = 1
    Stay = 2
    Double = 3
    Split = 4


with open('hit_stay_or_double.pkl', 'rb') as file2:
    hit_stay_double_chart = pickle.load(file2)

with open('splitting_chart.pkl', 'rb') as file:
    splitting_chart = pickle.load(file)


class Player:

    def __init__(self):
        self.hands = deque([], maxlen=4)
        self.staying_hands = deque([], maxlen=4)
        self.records = []
        self.balance = [0]

    def decide3(self, hand, dealer_upcard):
        """
        I am sorting the hand if there is an ace...should I do deep copy
        so I don't change the order of hands for the rest of the program?
        """

        if hand_busted(hand):
            message = "Should not be deciding hit, stay, or split" \
                "if the hand is busted."
            raise ValueError(message)

        if len(hand) >= 3:
            return self._hit_stay_or_double(hand, dealer_upcard)
        else:
            pair_of_cards = hand[0].value == hand[1].value
            if pair_of_cards:
                should_split = splitting_chart[hand[0].rank +
                                               's'][dealer_upcard.rank]
                if should_split == 'Sp':
                    return Decision.Split
                else:
                    return self._hit_stay_or_double(hand, dealer_upcard)
            else:
                return self._hit_stay_or_double(hand, dealer_upcard)

    def _hit_stay_or_double(self, hand, dealer_upcard):
        if any_ace_in_hand(hand):
            if len(hand) >= 3:
                ranks = [str(n) for n in range(2, 10)]
                total = best_total(hand)
                if total == 21:
                    player_total = '21'
                else:
                    rank = ranks[total - 11 - 2]
                    player_total = 'A' + rank
            else:
                player_total = ''.join(
                    card.rank for card in sorted(hand, reverse=True))
        else:
            player_total = str(hard_total(hand))

        decision = hit_stay_double_chart[player_total][dealer_upcard.rank]

        if decision == 'H':
            return Decision.Hit
        elif decision == 'S':
            return Decision.Stay
        else:
            return Decision.Double


def main():
    print(hit_stay_double_chart.keys())
    # print(hit_stay_double_chart['A9']['9'])


if __name__ == '__main__':
    main()
    unittest.main()
    main()
