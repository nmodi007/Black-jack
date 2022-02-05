#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The tray class is a simulation of the Black Jack's dealer's tray.
decks: number of decks in the tray.
"""

import sys
from card import Card
from random import shuffle, randint


class Tray:
    '''
    When you get a new tray, it comes with the deck cut.
    '''
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self, decks=1):
        self._num_of_decks = decks
        self._cards = [Card(suit, rank)
                       for i in range(decks)
                       for suit in self.suits
                       for rank in self.ranks]
        shuffle(self._cards)
        self._cut_part = []
        self._cut_the_deck()

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value


    def get_num_of_decks(self):
        return self._num_of_decks

    def __repr__(self):
        # return '\n'.join(f'{c.rank} of {c.suit}' for c in self._cards)
        return '\n'.join(f'{c}' for c in self._cards)

    def deal(self, cards=1):
        '''
        Deal from the tray. Will remove cards from the right side of the deck.
        will pop cards from the deck.

        Parameters
        ----------
        cards : int
            Number of cards to deal (to remove from the deck).

        Returns
        -------
        None.

        '''
        if not isinstance(cards, int):
            raise TypeError("Number of cadrds should be int.")

        if cards < 1:
            raise ValueError("Number of cards should be 1 or more.")

        cards_to_return = []

        for _ in range(cards):
            try:
                cards_to_return.append(self._cards.pop())
            except IndexError:
                try:
                    cards_to_return.append(self._cut_part.pop())
                except IndexError as e:
                    print(e, file=sys.stderr)
                    raise 
        return cards_to_return

    def _cut_the_deck(self):
        lower = round(len(self._cards) * 0.20)  # 20% of the deck
        upper = round(len(self._cards) * 0.35)  # 35% of the deck
        pos = randint(lower, upper)  # position where to cut.

        self._cut_part = self._cards[:pos]
        del self._cards[:pos]


def main():
    t = Tray(2)
    print(f'number of decks: {t.get_num_of_decks()}')

    shuffle(t)
    print(t)
    print('-------')

    print('\nlast 3 cards:')
    for c in t[-3:]:
        print(c)

    cards = t.deal(3)
    print('\n3 delt cards:')
    for c in cards:
        print(c)

    print('\nlast 3 cards after dealing:')
    for c in t[-3:]:
        print(c)

    print('----')
    the_whole_deck = t.deal(101)
    print(len(the_whole_deck))

if __name__ == '__main__':
    main()
