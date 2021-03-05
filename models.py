import flask_sqlalchemy
import random
import game_exceptions
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = flask_sqlalchemy.SQLAlchemy()

class Game(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # originally db.Column(db.Integer, primary_key=True)
    player_a_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    player_b_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)

    player_a = db.relationship('Player', foreign_keys=[player_a_id])
    player_b = db.relationship('Player', foreign_keys=[player_b_id])

    def get_player(self, guest_id):
        if self.player_a and self.player_a.guest and self.player_a.guest.id == guest_id: return self.player_a
        if self.player_b and self.player_b.guest and self.player_b.guest.id == guest_id: return self.player_b
        raise game_exceptions.NoSuchPlayerInGame()

    def add_player(self, guest): # TODO: refactor duplicate code
        if not self.player_a:
            new_player=Player()
            new_player.guest=guest
            self.player_a=new_player
            if self.player_b:
                self.player_a.is_red=not(self.player_b.is_red)
            else:
                self.player_a.set_random_color()
            return new_player
        if not self.player_b:
            new_player=Player()
            new_player.guest=guest
            self.player_b=new_player
            if self.player_a:
                self.player_b.is_red=not(self.player_a.is_red)
            else:
                self.player_b.set_random_color()
            return new_player
        raise game_exceptions.GameIsFull()


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=True)
    is_red = db.Column(db.Boolean, nullable=False)
    is_inviter = db.Column(db.Boolean, nullable=True)

    guest = db.relationship('Guest')

    def __init__(self, is_inviter=False, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.is_inviter=is_inviter

    def set_random_color(self):
        random.seed()
        self.is_red=random.choice([True, False])


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)


