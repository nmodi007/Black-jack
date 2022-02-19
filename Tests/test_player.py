import unittest
from card import Card

from player import Decision, Player


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
        self.assertEqual(self.player1.decide3(
            self.five_nine, self.nine), Decision.Hit)
        self.assertEqual(self.player1.decide3(
            self.five_six, self.nine), Decision.Double)

    def test_hand_value_with_ace(self):
        self.assertEqual(self.player1.decide3(
            self.ace_five, self.nine), Decision.Hit)
        self.assertEqual(self.player1.decide3(
            self.ace_nine, self.nine), Decision.Stay)

    def test_decide_with_blackjack_hand_throws_ValueException(self):
        with self.assertRaises(ValueError) as context:
            self.player1.decide3(self.ace_king, self.nine)
        self.assertTrue("Should not be deciding on a winning hand."
                        in str(context.exception))

    def test_should_split_eights(self):
        self.assertEqual(self.player1.decide3(
            self.pair_eights, self.nine), Decision.Split)

    def test_should_hit_pair_of_sixes_dealer_nine(self):
        self.assertEqual(self.player1.decide3(
            self.pair_sixes, self.nine), Decision.Hit)


if __name__ == '__main__':
    unittest.main()
