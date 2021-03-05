# TODO: this ideally requires a polymorphic solution, but well...

class MovedToEmptySquare:
    pass

class AttackResult:
    def __init__(self, succeeded, score_attacker, score_defender):
        self.succeeded=succeeded
        self.score_attacker=score_attacker
        self.score_defender=score_defender
