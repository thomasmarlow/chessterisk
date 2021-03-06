class MovedToEmptySquare:
    def triggers_alert_display(self):
        return False

class AttackResult:
    def __init__(self, succeeded, attacker_score, attacker_color, defender_score):
        self.succeeded=succeeded
        self.attacker_score=attacker_score
        self.attacker_color=attacker_color
        self.defender_score=defender_score

    def triggers_alert_display(self):
        return True

    def message(self):
        if self.succeeded:
            return f'{self.attacker_color.string} captures: {self.attacker_score} > {self.defender_score}'
        defender_color='blue' if self.attacker_color.string=='red' else 'red'
        return f'{defender_color} blocks: {self.attacker_score} > {self.defender_score}'