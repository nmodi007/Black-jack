#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import csv
from pprint import pprint as pp
import pickle


def read_csv_file(file_name):
    # opening the CSV file
    with open(file_name, mode='r') as file:
        # reading the CSV file
        csvFile_lines = list(csv.reader(file))

        dealer_upcard, *data = csvFile_lines
        dealer_upcard = dealer_upcard[1:]  # discard first element.

        chart = {}
        for line in data:
            players_hand, *decision = line
            chart[players_hand] = dict(zip(dealer_upcard, decision))
        
    return chart

def write_to_binary(file_name, variable):
    # create a binary pickle file
    with open(file_name, "wb") as file:
        pickle.dump(variable, file)


hit_stay_double_chart = read_csv_file('hit_stay_double.csv')
write_to_binary("hit_stay_or_double.pkl", hit_stay_double_chart)

splitting_chart = read_csv_file('splitting.csv')
write_to_binary("splitting_chart.pkl", splitting_chart)