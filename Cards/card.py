from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import os
from random import randint

class Card(object):
    def __init__(self, name = None):
        self.name = None
        self.color = None
        self.type = None
        self.subtype = None
        self.cmc = None
        self.rules_text = None
        self.toughness = None
        self.power = None
        self.uniqueID = randint(0,1000000000)
        self.tapped = None
        self.summoning_sickness = None
        self.attacking = None
        self.damage = 0

        if name:
            self.load_by_name(name)

    @property
    def untapped(self):
        if self.tapped:
            return False
        else:
            return True

    def __repr__(self):
        return self.name

    def load_from_dict(self, input_dict):
        self.name = input_dict.get('name',None)
        self.color = input_dict.get('color', [])
        self.type = input_dict.get('type', [])
        self.subtypes = input_dict.get('subtypes', [])
        self.cmc = input_dict.get('cmc', '')
        self.rules_text = input_dict.get('rules_text','')
        self.power = input_dict.get('power',None)
        self.toughness = input_dict.get('toughness',None)

    def load_by_name(self, name):
        yaml_file = 'Cards/' + name + '.yaml'
        yaml_file_location = os.path.abspath(yaml_file)
        if os.path.exists(yaml_file_location):
            stream = file(yaml_file_location,'r')
        else:
            raise ValueError("card {} not found in database. Should be at location {}".format(name, yaml_file_location))

        card_dict = load(stream, Loader)
        self.load_from_dict(card_dict)