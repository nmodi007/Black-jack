
import unittest
from card import Card
from player import Status


class Hand():

    def __init__(self, cards=None) -> None:
        if cards is None:
            self.cards = []
        else:
            self.cards = list(cards)
    
    # def __iter__(self):
    #     return (c for c in self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def __setitem__(self, position, value):
        self.cards[position] = value

    def __repr__(self) -> str:
        return ' '.join(card.rank for card in self.cards)
        
class HandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.five = Card('hearts', '5')
        self.nine = Card('clubs', '9')

        self.cards = [self.five, self.nine]
        
        return super().setUp()

    def test_hand_init(self):
        hand = Hand(self.cards)
        self.assertEqual(hand.cards[0], self.five)
        self.assertEqual(hand.cards[1], self.nine)
        self.assertIsInstance(hand.cards, list)

    def test_pass_empty_cards(self):
        hand = Hand([])
        self.assertEqual(hand.cards, [])
        
    def test_pass_nothing(self):
        hand = Hand()
        self.assertEqual(hand.cards, [])

    def test_in_operator(self):
        hand = Hand(self.cards)
        self.assertTrue(self.five in hand)

    def test_card_in_hand(self):
        hand = Hand(self.cards)
        for card in hand:
            print(card.value)

if __name__ == '__main__':
    unittest.main()