#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate playing many rounds of Blackjack at a casino.

Usage: python3 black_jack_sim.py <rounds> <num_players>

"""
import sys
from glob import glob
from itertools import count
import os
from dealer import Dealer
from player import Player, Status
from tray import Tray
from matplotlib import pyplot as plt

def main(rounds, num_players):
    """
    rounds: the number of rounds to simulate.
    num_players: the number of players at the table.
    """
    tray = Tray(decks=6)
    dealer = Dealer()
    players = [Player() for i in range(num_players)]

    for round in range(rounds):
        dealer.deal(players, tray)
        dealer.play(players, tray)
        if not len(tray):
            tray = Tray(decks=6)

    # find all the player[0-9] files and delete them.
    for file in glob('player[0-9]'):
        os.remove(file)
    
    # delete the stats file.
    stats_file = 'stats'
    if os.path.isfile(f'./{stats_file}'):
        os.remove(f'./{stats_file}')

    total_wins_of_all_players = 0
    total_losses_of_all_players = 0
    total_pushes_of_all_players = 0

    for player in players:    
        wins, losses, pushes, balance = calculate_stats(player)
        print_stats_to_file(wins, losses, pushes, balance, stats_file )
        total_wins_of_all_players += wins
        total_losses_of_all_players += losses
        total_pushes_of_all_players += pushes
        
    plot_players_balance(players)

    dealer_wins = total_losses_of_all_players
    dealer_losses = total_wins_of_all_players
    dealer_pushes = total_pushes_of_all_players
    print_stats_to_file(dealer_wins,
                        dealer_losses,
                        dealer_pushes,
                        dealer.bank[-1],
                        stats_file)

    plot_dealer_stats(dealer_wins, dealer_losses, dealer_pushes)
    
    # print_records_of_players_to_file(players)
   
def plot_players_balance(players):
    plt.style.use('seaborn-whitegrid')
    fig1, ax1 = plt.subplots()
    for player in players:
        ax1.plot(player.balance)
    plt.savefig('players_balance.png')
    # plt.show()


def plot_dealer_stats(dealer_wins, dealer_losses, dealer_pushes):   
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'dealer wins', 'dealer loses', 'dealer pushes'
    sizes = [dealer_wins, dealer_losses, dealer_pushes]
    explode = (0.1, 0, 0)  # only "explode" the winning slice

    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig2.suptitle('Dealer stats')
    plt.savefig('dealer_stats.png')
    # plt.show()
    
def print_records_of_players_to_file(players):
    for num, player in enumerate(players):
            file_name = 'player' + str(num)
            with open(file_name, mode='wt', encoding='utf-8') as file:
                for record in player.records:
                    file.write(format(record))


def calculate_stats(player):
    wins = 0
    losses = 0
    pushes = 0
    for record in player.records:
        if record.result == Status.Win:
            wins += 1
        elif record.result == Status.Push:
            pushes += 1
        else:
            losses += 1

    return wins, losses, pushes, player.balance[-1]

def print_stats_to_file(wins, losses, pushes, balance, file_name):
    total_hands = wins + losses + pushes
    with open(file_name, mode='a', encoding='utf-8') as file:
            file.write(f'wins: {wins} winning %: {wins/total_hands:.2%}\n')
            file.write(f'losses: {losses} losing %: {losses/total_hands:.2%}\n')
            file.write(f'pushes: {pushes} push %: {pushes/total_hands:.2%}\n')
            file.write(f'--------------------------\n')
            file.write(f'total hands: {total_hands}\n')
            file.write(f'final balance: {balance}\n\n')


if __name__ == '__main__':
    # _, num_rounds, num_players = sys.argv
    # try:
    #     rounds = int(num_rounds)
    # except ValueError as e:
    #     print(f'Number of rounds must be an integer. {str(e)}')
    #     raise

    # try:
    #     number_of_players = int(num_players)
    # except ValueError as e:
    #     print(f'Number of players must be an integer.', file=sys.stderr)
    #     # raise

    import  argparse
    parser = argparse.ArgumentParser(description="Blackjack simulation")
    parser.add_argument('rounds', type=int, help='number of rounds to simulate', )
    parser.add_argument('players', type=int, help='number of players at the table.')
    args = parser.parse_args()
    main(args.rounds, args.players)
