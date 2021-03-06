import flask
import flask_socketio

import flask_sqlalchemy
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from uuid import UUID

from models import db, Game, Guest, Player
import game_exceptions

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://chessterisk:chessterisk@localhost:5432/chessterisk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # TODO: randomize

db.init_app(app)
socketio = flask_socketio.SocketIO(app)

@app.route('/home', methods=['GET'])
def home():
    if not 'guest_id' in flask.session:
        new_guest = Guest()
        db.session.add(new_guest)
        db.session.commit()
        flask.session['guest_id'] = new_guest.id
        print("NEW GUEST ID {}".format(flask.session['guest_id']))
    return flask.render_template('home.html')

@app.route('/newgame/invite', methods=['GET'])
def newgame_invite():
    if not 'guest_id' in flask.session:
        new_guest = Guest()
        db.session.add(new_guest)
        db.session.commit()
        flask.session['guest_id'] = new_guest.id
        print("NEW GUEST ID {}".format(flask.session['guest_id']))
    new_game=Game()
    new_game.player_a=Player(is_inviter=True)
    new_game.player_a.set_random_color()
    try:
        new_game.player_a.guest=Guest.query.filter_by(id=flask.session['guest_id']).one()
    except NoResultFound:
        guest = Guest()
        db.session.add(guest)
        db.session.commit()
        flask.session['guest_id'] = guest.id
        print("NEW GUEST ID {} (for existing guest)".format(flask.session['guest_id']))
    except MultipleResultsFound:
        pass # TODO
    db.session.add(new_game)
    db.session.commit()
    return flask.redirect(flask.url_for('game', game_id=new_game.id))

# @app.route('/newgame/automatch', methods=['GET'])
# def newgame_automatch():
#     return 'New game'

@app.route('/game/<game_id>', methods=['GET'])
def game(game_id): # TODO: delegation went on vacation, huh?
    if not is_valid_uuid(game_id):
        return flask.redirect(flask.url_for('home')) # TODO: warning alert in home
    if not 'guest_id' in flask.session: # TODO: abstract guest creation into separate function
        new_guest = Guest()
        db.session.add(new_guest)
        db.session.commit()
        flask.session['guest_id'] = new_guest.id
        print("NEW GUEST ID {}".format(flask.session['guest_id']))
    try:
        game=Game.query.filter_by(id=game_id).one()
    except NoResultFound:
        return flask.redirect(flask.url_for('home')) # TODO: warning alert in home
    # except MultipleResultsFound:
    #     pass # TODO
    try: # we first check if the guest is already in this game
        player=game.get_player(guest_id=flask.session['guest_id'])
        return flask.render_template('game.html', color='red' if player.is_red else 'blue', is_inviter=player.is_inviter)
    except game_exceptions.NoSuchPlayerInGame:
        try: # if it isn't, we try to make it into a player
            new_guest=Guest.query.filter_by(id=flask.session['guest_id']).one()
            player=game.add_player(guest=new_guest)
            db.session.add(player)
            db.session.commit()
            return flask.render_template('game.html', color='red' if player.is_red else 'blue', is_inviter=player.is_inviter)
        except game_exceptions.GameIsFull:
            return flask.redirect(flask.url_for('home')) # TODO: warning alert in home; in the future a possible spectator mode

@socketio.on('join game')
def handle_join_game(received_json): # TODO: flask.session can be used for checks!
    flask_socketio.join_room(json['game_id'])

@socketio.on('make move')
def handle_make_move(received_json): # TODO: flask.session can be used for checks!
    game=Game.query.filter_by(id=received_json['game_id']).one() # TODO: missing exception handling (including valid uuid)
    move_result=game.move(received_json['coords_from'], received_json['coords_to'])
    data_to_send={'position': game.position_string, 'color_of_turn': game.color_string}
    if move_result.triggers_alert_display():
        data_to_send['alert']=move_result.message()
    json_to_send=flask.jsonify(data_to_send)
    db.session.add(game)
    db.session.commit()
    flask_socketio.emit('move made', json_to_send, room=game.id)

@app.route('/game/<game_id>/position', methods=['GET'])
def game_position(game_id):
    game=Game.query.filter_by(id=game_id).one() # TODO: exception handling
    data_to_send={'position': game.position_string, 'color_of_turn': game.color_string}
    json_to_send=flask.jsonify(data_to_send)
    return json_to_send

@app.route('/test/<side>', methods=['GET', 'POST'])
def test(side):
    if flask.request.method == 'POST':
        return 'POST to game'
    else:
        if not (side in ['red', 'blue']):
            return flask.redirect(flask.url_for('home'))
        return flask.render_template('game.html', side=side)

@app.errorhandler(404)
def page_not_found(e):
    return flask.redirect(flask.url_for('home'))

def is_valid_uuid(uuid_to_test, version=4): # TODO: move to better place, utils.py or sth
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

if __name__ == '__main__':
    # game_manager=server_utils.GameManager()
    app.run(threaded=True, port=5000, debug=True)