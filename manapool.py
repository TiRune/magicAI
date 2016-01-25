import re
import numpy as np
from errors import GameStateError

class ManaPool():
    def __init__(self, mana_string = None):
        self.mana = {'white':0, 'blue':0, 'black':0, 'red': 0, 'green': 0,
                'colorless': 0,'generic': 0}

        if mana_string:
            self.init_by_string(mana_string)

    def init_by_string(self, mana_string):
        mana_string = str.lower(mana_string)
        self.mana['white'] = mana_string.count('w')
        self.mana['blue'] = mana_string.count('u')
        self.mana['black'] = mana_string.count('b')
        self.mana['red'] = mana_string.count('r')
        self.mana['green'] = mana_string.count('g')
        self.mana['colorless'] = mana_string.count('o')
        self.mana['generic'] = np.sum(re.findall(r'\d+', mana_string))

    def empty_pool(self):
        self.mana['white'] = 0
        self.mana['blue'] = 0
        self.mana['black'] = 0
        self.mana['red'] = 0
        self.mana['green'] = 0
        self.mana['colorless'] = 0
        self.mana['generic'] = 0

    def __repr__(self):
        return '[W: ' + str(self.mana['white']) + \
               ' - U: ' + str(self.mana['blue']) + \
               ' - B: ' + str(self.mana['black']) + \
               ' - R: ' + str(self.mana['red']) + \
               ' - G: ' + str(self.mana['green']) + \
               ' - O: ' + str(self.mana['colorless']) + \
               ' - any: ' + str(self.mana['generic']) + \
               ']'

    def reduce_by(self, cost):
        if type(cost) == str:
            self -= ManaPool(cost)

    def add(self, value):
        if type(value) == str:
            self += ManaPool(value)
        else:
            pass

    def __add__(self, other):
        for key in self.mana:
            if key != 'generic':
                self.mana[key] += other.mana[key]


    def __sub__(self, other):
        for key in self.mana:
            if key != 'generic':
                self.mana[key] -= other.mana[key]

        # process generic, can be any order
        if other.mana['generic'] > 0:
            generic_to_deduct = other.mana['generic']
            for key in self.mana:
                mana = self.mana[key]
                if generic_to_deduct <= 0:
                    break
                if mana > 0:
                    if mana <= generic_to_deduct:
                        generic_to_deduct -= mana
                        self.mana[key] = 0
                    else:
                        self.mana[key] -= generic_to_deduct
                        generic_to_deduct = 0
            if generic_to_deduct > 0:
                raise GameStateError('Mana left to pay, cannot cast '
                                     'this spell')


        # make sure all mana values are positive
        for key in self.mana:
            if self.mana[key] < 0:
                raise GameStateError("Mana value below 0 found")