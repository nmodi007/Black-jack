#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from logging import exception
import unittest
from card import Card
from blackjack_utility import any_ace_in_hand, best_total, hand_busted, hand_values, hard_total, is_natural_blackjack, soft_total
from collections import defaultdict, deque

import enum

import pickle

class Status(enum.Enum):
    Win = 1
    Busted = 2 # when hand goes over 21.
    Lose = 3 # you stay and dealer gets higher score.
    Push = 4
    Still_playing = 5 # still in the game. If the player is staying and waiting for the dealer.

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
        I am sorting the hand if there is an ace...should I do deep copy so I don't change the order
        of hands for the rest of the program?
        """

        if hand_busted(hand):
            raise ValueError("Should not be deciding hit, stay, or split if the hand is busted.")

        if len(hand) >= 3:
           return self._hit_stay_or_double(hand, dealer_upcard)
        else:
            pair_of_cards = hand[0].value == hand[1].value    
            if pair_of_cards:
                should_split = splitting_chart[hand[0].rank + 's'][dealer_upcard.rank]
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
                player_total = ''.join(card.rank for card in sorted(hand, reverse=True))    
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
    #print(hit_stay_double_chart['A9']['9'])

class PlayerTests(unittest.TestCase):

    def setUp(self):
        """ Runs before each test."""
        self.player1 = Player()
        self.five = Card("heart", '5')
        self.six = Card("heart", '6')
        self.another_six = Card("heart", '6')
        self.nine = Card("clubs", '9')
        self.king = Card('spades', 'K')
        self.ace = Card('diamonds', 'A')
        self.eight = Card('hearts', '8')
        self.another_eight = Card('clubs', '8')

        self.ace_five = [self.ace, self.five]
        self.five_nine = [self.five, self.nine]
        self.five_six = [self.five, self.six]
        self.ace_nine = [self.ace, self.nine]
        self.ace_king = [self.ace, self.king]

        self.pair_eights = [self.eight, self.another_eight]
        self.pair_sixes = [self.six, self.another_six]

    def test_hand_value(self):
        self.assertEqual(self.player1.decide3(self.five_nine, self.nine) , Decision.Hit)
        self.assertEqual(self.player1.decide3(self.five_six, self.nine) , Decision.Double)

    def test_hand_value_with_ace(self):
        self.assertEqual(self.player1.decide3(self.ace_five, self.nine) , Decision.Hit)
        self.assertEqual(self.player1.decide3(self.ace_nine, self.nine) , Decision.Stay)
        
    def test_decide_with_blackjack_hand_throws_ValueException(self):
        with self.assertRaises(ValueError) as context:
            self.player1.decide3(self.ace_king, self.nine)
        self.assertTrue("Should not be deciding on a winning hand."
                         in str(context.exception))

    def test_should_split_eights(self):
        self.assertEqual(self.player1.decide3(self.pair_eights, self.nine) , Decision.Split)

    def test_should_hit_pair_of_sixes_dealer_nine(self):
        self.assertEqual(self.player1.decide3(self.pair_sixes, self.nine) , Decision.Hit)

        

if __name__ == '__main__':
    main()
    unittest.main()
    main()