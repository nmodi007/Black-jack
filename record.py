#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from blackjack_utility import best_total


class Record:

    def __init__(self, player_hand, dealer_hand, result, new_balance):
        """
        Parameters
        ----------
        player_hand : list
            player hand.
        dealer_hand : list
            dealer hand.
        result : Status
            the result for the player
            win, lose, push.

        Returns
        -------
        None.
        """
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.result = result
        self.new_balance = new_balance

    def __repr__(self):
        hand = ' '.join(card.rank for card in self.player_hand)
        s1 = f"player hand: {hand} {best_total(self.player_hand)}"

        dealer_hand = ' '.join(card.rank for card in self.dealer_hand)
        s2 = f"dealer hand: {dealer_hand} {best_total(self.dealer_hand)}"

        s3 = f'balance: {self.new_balance}'
        s4 = '-------------------'
        return '\n'.join([s1, s2, self.result.name, s3, s4]) + '\n'
