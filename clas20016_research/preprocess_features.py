'''
Reads information of each mention and featurises it
'''

## import relevant libraries
import os
import pandas as pd

## find directory
dir_name = os.path.dirname(__file__)

## read in data
instances = pd.read_csv(f'{dir_name}ship_instances.csv')