import unittest

from card import Card
from player import Status
from record import Record


class RecordTests(unittest.TestCase):

    def setUp(self):
        self.nine = Card(rank='9', suit='hearts')
        self.jack = Card(rank='J', suit='clubs')

        self.player_hand = [self.nine, self.jack]

        self.eight = Card(rank='8', suit='hearts')
        self.queen = Card(rank='Q', suit='clubs')

        self.dealer_hand = [self.eight, self.queen]

        self.status = Status.Win

        self.record = Record(
            self.player_hand, self.dealer_hand, self.status, 125)

    def test_record_str(self):
        print(self.record)


if __name__ == '__main__':
    unittest.main()
