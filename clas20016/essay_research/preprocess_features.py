'''
Reads information of each mention and featurises it
'''

## import relevant libraries
import os
import nltk
import pandas as pd

from helper_functions import categorise_case, categorise_number
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

## find directory
dir_name = os.path.dirname(__file__)
relative_dir = 'data/'

## set variables
lines_per_book = [444, 433, 497, 847, 493, 331, 347, 586, 566, 574, 640, 453]
west_removed = ['1.171', '2.407', '3.131', '4.248', '10.569', '12.140']

## read in data
instances = pd.read_csv(f'{dir_name}{relative_dir}ship_instances.csv')

## set column types
instances['book'] = instances['book'].astype(int)
instances['line'] = instances['line'].astype(int)
instances['ship'] = instances['ship'].astype(str)
instances['epithet_gr'] = instances['epithet_gr'].astype(str)
instances['epithet_en'] = instances['epithet_en'].astype(str)
instances['number'] = instances['number'].astype(str)
instances['case'] = instances['case'].astype(str)
instances['clause'] = instances['clause'].astype(str)
instances['scansion'] = instances['scansion'].astype(str)

## dicts for new features
numbers = []
cases = []
appearances = []
num_lines = []
positions = []
differences = []
ratio = []
trigrams = []

## featurise
for index, row in instances.iterrows():

    numbers.append(categorise_number(row['number']))
    cases.append(categorise_case(row['case']))
    line_appearence = row['line']/lines_per_book[row['book']-1]
    appearances.append(line_appearence)

    ## find difference in epithet position
    phrase = row['clause'][:-1]
    words = phrase.replace(' | ', ' ').split(' ')
    if row['epithet_gr'] == 'none':
        difference = 0
    else:
        difference = words.index(row['epithet_gr']) - words.index(row['ship'])
    differences.append(difference)

    ## bi- and tri-grams
    if row['epithet_gr'] != 'none':
        clause = phrase.replace(' | ', ' ').replace(row['epithet_gr'], '')
    else:
        clause = phrase.replace(' | ', ' ')
    nltk_tokens = clause.split(' ')
    tri = list(nltk.trigrams(nltk_tokens))
    trigrams.append(tri)


    ## split clause into lines
    lines = row['clause'].split(' | ')
    num_lines.append(len(lines))

    for line in lines:
        if row['ship'] in line:
            words = line.split(' ')                
            filtered = [word for word in words if word!=row['epithet_gr']]

            ## find position of ship in the line
            if filtered[0] == row['ship']:
                pos = 0
            elif filtered[-1] == row['ship']:
                pos = 2
            else: 
                pos = 1
            positions.append(pos)
    
    ## find ratio of dactyls in a line
    feet = row['scansion'].split(' ')
    dactyl = 0
    for foot in feet:
        if foot == '-uu':
            dactyl += 1
    ratio.append(dactyl/6) # six feet per line

## encode all categorical variables
label = LabelEncoder()
onehot_encoder = OneHotEncoder(sparse=False)

ship_map = label.fit_transform(instances['ship'])
ship_map = ship_map.reshape(len(ship_map), 1)
ships = onehot_encoder.fit_transform(ship_map)

scan_map = label.fit_transform(instances['scansion'])
scan_map = scan_map.reshape(len(scan_map), 1)
scansion = onehot_encoder.fit_transform(scan_map)

## add features to dataframe
instances['ship'] = ships
instances['number'] = numbers
instances['case'] = cases
instances['scansion'] = scansion
instances['line'] = appearances
instances['num_lines'] = num_lines
instances['position'] = positions
instances['difference'] = differences
instances['ratio'] = ratio
instances['trigrams'] = trigrams

## take out instances west removed
instances_removed = instances
for index, row in instances_removed.iterrows():
    if f'{row["book"]}.{row["line"]}' in west_removed:
        instances_removed = instances_removed.drop(index)

## save data
instances_removed.to_csv(f'{dir_name}{relative_dir}ships_extended.csv')