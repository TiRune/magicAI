
class GameStateError(Exception):
    def __init__(self, message):
        super(GameStateError, self).__init__(message)


class GameRuleViolation(Exception):
    def __init__(self, message):
        super(GameRuleViolation, self).__init__(message)