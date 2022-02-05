#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from card import Card
import unittest


def hard_total(hand):
    """
    Any hand contaning either no aces or an Ace valued as 1 is a hard total.
    Returns the score where ace counts as 1 point.
    Every ace will count as 1. (ace, ace, ace, 5 --> 8)
    """
    score = 0
    for card in hand:
        if card.rank == 'A':
            score += 1
        else:
            score += card.value
    return score


def soft_total(hand):
    """
    Returns the score where ace counts as 11 points.
    Only the first ace will count as 11. The rest of the aces count as 1.
    """
    if not any_ace_in_hand(hand):
        raise ValueError("To calculate soft total there must be at least one ace in hand.")

    score = 0
    firstAce = True
    for card in hand:
        if card.rank == 'A' and firstAce:
            score += 11
            firstAce = False
        else:
            if card.rank == 'A':
                score += 1
            else:
                score += card.value
    return score

def any_ace_in_hand(hand):
    return any(card.value == 11 for card in hand)

def hand_busted(hand):
    """
    if ace in hand:
        (15, 25) --> 15     No
        (25, 20) --> 20     No 
        (25, 35) --> 25     Yes
        (15, 20) --> 20     no
        (20, 15) --> 20     no
    else:
        hard_total > 21     Yes
    """

    if any_ace_in_hand(hand):
        return soft_total(hand) > 21 and hard_total(hand) > 21
    
    return hard_total(hand) > 21 


def best_total(hand):
    """
    Return the best possible score.
    Best possible total can be over 21 if it is a busted hand.
    if ace in hand:
        (15, 25) --> 15     soft total busted.  (ten, four, ace)
        (25, 20) --> 20     hard total busted.  (i don't know)
        (25, 35) --> 25     both busted.        (nine, eight, ace, seven)
        (15, 20) --> 20     neither busted. pick the best.
        (20, 15) --> 20     neither busted. pick the best.
    else:
        return hard_total
    """
    
    hard_score = hard_total(hand)

    if any_ace_in_hand(hand):
        if hand_busted(hand):
            return hard_score
        elif hard_score <= 21 and soft_total(hand) <= 21:
            return max(hard_score, soft_total(hand))
        else:
            return min(hard_score, soft_total(hand))
    
    return hard_score

def hand_values(hand):
    """
    Give a tuple of two scores. The first one is with Ace counted as 1 or
    if there is no ace in the hand. The second score is with Ace counted as 11.

    Parameters
    ----------
    hand : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return (hard_total(hand),
            soft_total(hand) if any_ace_in_hand(hand) else None) 


def is_natural_blackjack(hand):
    if len(hand) != 2:
        raise ValueError(
            "When checking for natural blackjack, "
            "hand must have only 2 cards.")
    if any_ace_in_hand(hand):
        return soft_total(hand) == 21
    return False


class utility_tests(unittest.TestCase):

    def setUp(self):
        self.five = Card('spades', '5')
        self.ten = Card('diamonds', '10')
        self.jack = Card('hearts', 'J')
        self.ace = Card('clubs', 'A')
        self.nine = Card('spades', '9')

        self.five_ten = [self.five, self.ten]
        self.five_ten_nine = [self.five, self.ten, self.nine]
        self.nine_ten = [self.nine, self.ten]

        self.jack_ace = [self.jack, self.ace]
        self.ace_jack = [self.ace, self.jack]

        self.five_ace = [self.five, self.ace]
        self.ace_five = [self.ace, self.five]

        self.five_ten_ace = [self.five, self.ten, self.ace]

        self.nine_ten_ace = [self.nine, self.ten, self.ace]

        self.three_aces_five = [self.ace, self.ace, self.ace, self.five]
        self.three_aces_nine = [self.ace, self.ace, self.ace, self.nine]

        self.ace_ten_nine_five = [self.ace, self.ten, self.nine, self.five]

    def test_any_ace_in_hand_without_aces(self):
        self.assertFalse(any_ace_in_hand(self.five_ten))

    def test_any_ace_in_hand_with_aces(self):
        self.assertTrue(any_ace_in_hand(self.five_ten_ace))
        self.assertTrue(any_ace_in_hand(self.ace_five))
        self.assertTrue(any_ace_in_hand(self.five_ace))
        self.assertTrue(any_ace_in_hand(self.nine_ten_ace))
        self.assertTrue(any_ace_in_hand(self.three_aces_five))
        self.assertTrue(any_ace_in_hand(self.three_aces_nine))
        self.assertTrue(any_ace_in_hand(self.ace_ten_nine_five))

    def test_hand_values_without_ace(self):
        self.assertEqual(hand_values(self.five_ten), (15, None))
        self.assertEqual(hand_values(self.five_ten_nine), (24, None))
        self.assertEqual(hand_values(self.nine_ten), (19, None))

    def test_hand_values_with_ace(self):
        self.assertEqual(hand_values(self.five_ten_ace), (16, 26))
        self.assertEqual(hand_values(self.ace_five), (6, 16))
        self.assertEqual(hand_values(self.five_ace), (6, 16))
        self.assertEqual(hand_values(self.nine_ten_ace), (20, 30))
        self.assertEqual(hand_values(self.three_aces_five), (8, 18))
        self.assertEqual(hand_values(self.three_aces_nine), (12, 22))
        self.assertEqual(hand_values(self.ace_ten_nine_five), (25, 35))

    def test_hand_values_with_ace_blackjack(self):
        self.assertEqual(hand_values(self.jack_ace), (11, 21))
        self.assertEqual(hand_values(self.ace_jack), (11, 21))

    def test_three_aces_hand_values(self):
        self.assertEqual(hand_values(self.three_aces_five), (8, 18))

    def test_is_natural_blackjack(self):
        self.assertTrue(is_natural_blackjack(self.jack_ace))

    def test_is_natural_blackjack_throws_ValueException(self):
        with self.assertRaises(ValueError) as context:
            is_natural_blackjack(self.five_ten_nine)
        self.assertTrue("When checking for natural blackjack, "
                        "hand must have only 2 cards."
                        in str(context.exception))

    def test_best_total_no_aces(self):
        self.assertEqual(best_total(self.five_ten), 15)
        self.assertEqual(best_total(self.five_ten_nine), 24)

    def test_best_total_with_aces(self):
        self.assertEqual(best_total(self.five_ten_ace), 16)     # (16, 26)
        self.assertEqual(best_total(self.ace_five), 16)         # (6, 16)
        self.assertEqual(best_total(self.nine_ten_ace), 20)     # (20, 30)
        self.assertEqual(best_total(self.three_aces_five), 18)  # (8, 18)
        self.assertEqual(best_total(self.three_aces_nine), 12)  # (12, 22)

    def test_best_total_both_bust(self):
        self.assertEqual(best_total(self.ace_ten_nine_five), 25)    # (25, 35)

    def test_hard_total(self):
        self.assertEqual(hard_total(self.five_ten_ace), 16)
        self.assertEqual(hard_total(self.ace_five), 6)
        self.assertEqual(hard_total(self.nine_ten_ace), 20)
        self.assertEqual(hard_total(self.three_aces_five), 8)
        self.assertEqual(hard_total(self.three_aces_nine), 12)
        self.assertEqual(hard_total(self.ace_ten_nine_five), 25)

    def test_soft_total(self):
        self.assertEqual(soft_total(self.five_ten_ace), 26)
        self.assertEqual(soft_total(self.ace_five), 16)
        self.assertEqual(soft_total(self.nine_ten_ace), 30)
        self.assertEqual(soft_total(self.three_aces_five), 18)
        self.assertEqual(soft_total(self.three_aces_nine), 22)
        self.assertEqual(soft_total(self.ace_ten_nine_five), 35)

if __name__ == '__main__':
    unittest.main()
