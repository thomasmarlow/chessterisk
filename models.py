import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_a_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    player_a = db.relationship('player')
    player_b_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    player_b = db.relationship('player')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
