#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from time import sleep
import unittest

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()

    def __repr__(self):
        return f'Card({self.suit}, {self.rank})'

    def __str__(self):
        return f'{self.rank} of {self.suit}'

    def _get_value(self):
        value = 0
        if self.rank in '23456789':
            value = int(self.rank)
        elif self.rank in "J Q K 10".split():
            value = 10
        else:
            value = 11
        return value

    def __eq__(self, __o: object) -> bool:
        return self.value == __o.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

class CardTests(unittest.TestCase):

    def setUp(self) -> None:
        self.five = Card("heart", '5')
        self.five_clubs = Card('clubs', '5')
        self.nine = Card("clubs", '9')

        self.king = Card('spades', 'K')
        self.ace = Card('diamonds', 'A')
        self.pile = [self.king, self.five, self.ace, self.nine]
        self.hand = [self.ace, self.five]
        self.hand2 = [self.five, self.ace]

        return super().setUp()
    
    def test_equal(self):
        self.assertEqual(self.five, self.five_clubs)

    def test_lessthan(self):
        self.assertTrue(self.five < self.nine)
        self.assertTrue(self.king < self.ace)
        self.assertTrue(self.nine < self.king)
        self.assertFalse(self.five < self.five_clubs)

    def test_can_sort_list_of_cards(self):
        self.assertEqual([self.five, self.nine, self.king, self.ace],
                            sorted(self.pile))

    def test_player_total_key_for_lookup(self):
        self.assertEqual(''.join(card.rank for card in sorted(self.hand, reverse=True)), 'A5')
        self.assertEqual(''.join(card.rank for card in sorted(self.hand2, reverse=True)), 'A5')


if __name__ == '__main__':
    unittest.main()