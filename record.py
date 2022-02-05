#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import unittest
from blackjack_utility import best_total
from card import Card
from player import Status


class Record:

    def __init__(self, player_hand, dealer_hand, result):
        """
        Parameters
        ----------
        player_hand : list
            player hand.
        dealer_hand : list
            dealer hand.
        result : Status
            the result for the player. 
            win, lose, push.

        Returns
        -------
        None.
        """
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.result = result

    def __repr__(self):
        hand = ' '.join(card.rank for card in self.player_hand)
        s1 = f"player hand: {hand} {best_total(self.player_hand)}"
        
        dealer_hand = ' '.join(card.rank for card in self.dealer_hand)
        s2 = f"dealer hand: {dealer_hand} {best_total(self.dealer_hand)}"

        s3 = '-------------------'
        return '\n'.join([s1, s2, self.result.name, s3]) + '\n'

class RecordTests(unittest.TestCase):

    def setUp(self):
        self.nine = Card(rank='9', suit='hearts')
        self.jack = Card(rank='J', suit='clubs')

        self.player_hand = [self.nine, self.jack]

        self.eight = Card(rank='8', suit='hearts')
        self.queen = Card(rank='Q', suit='clubs')

        self.dealer_hand = [self.eight, self.queen]

        self.status = Status.Win

        self.record = Record(self.player_hand, self.dealer_hand, self.status)

    def test_record_str(self):
        print(self.record)

if __name__ == '__main__':
    unittest.main()
