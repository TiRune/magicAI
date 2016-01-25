from cardzone import CardZone

class Hand(CardZone):
    def __init__(self):
        super(self.__class__, self).__init__()
        pass

    @property
    def __name__(self):
        return 'Hand'