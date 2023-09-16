import flask
import flask_socketio

import os
import flask_sqlalchemy
from flask_migrate import Migrate
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from uuid import UUID

from models import db, Game, Guest, Player
import game_exceptions
from game_move_results import AttackResult, GameHasEnded
import random

app = flask.Flask(__name__)
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://chessterisk:chessterisk@db:5432/chessterisk'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # TODO: randomize

db.init_app(app)
migrate = Migrate(app, db)
socketio = flask_socketio.SocketIO(app)

@app.route('/home', methods=['GET'])
def home():
    if not 'guest_id' in flask.session:
        new_guest = Guest()
        db.session.add(new_guest)
        db.session.commit()
        flask.session['guest_id'] = new_guest.id
        print("NEW GUEST ID {}".format(flask.session['guest_id']))
    return flask.render_template('home.html', last_updated=dir_last_updated('static'))

@app.route('/newgame/invite', methods=['GET'])
def newgame_invite():
    if not 'guest_id' in flask.session:
        new_guest = Guest()
        db.session.add(new_guest)
        db.session.commit()
        flask.session['guest_id'] = new_guest.id
        # print("NEW GUEST ID (invite) {}".format(flask.session['guest_id']))
    print('------- GUEST {}: /newgame/invite'.format(
        flask.session['guest_id']
    ))
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
        # print("NEW GUEST ID {} (for existing guest)".format(flask.session['guest_id']))
        new_game.player_a.guest=guest
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
    print('------- GUEST {}: /game/{}'.format(
        flask.session['guest_id'],
        game_id
    ))
    try:
        game=Game.query.filter_by(id=game_id).one()
    except NoResultFound:
        return flask.redirect(flask.url_for('home')) # TODO: warning alert in home
    # except MultipleResultsFound:
    #     pass # TODO
    try: # we first check if the guest is already in this game
        player=game.get_player(guest_id=flask.session['guest_id'])
        return flask.render_template('game.html', color='red' if player.is_red else 'blue', is_inviter=player.is_inviter, game_id=game_id, winner=game.winner_color_string, last_updated=dir_last_updated('static'))
    except game_exceptions.NoSuchPlayerInGame:
        if game.is_full():
            return flask.render_template('game.html', is_viewer='True', color=random.choice(['red', 'blue']), is_inviter=False, game_id=game_id, winner=game.winner_color_string, last_updated=dir_last_updated('static'))
        else: # the guest registers as player if they make a move
            return flask.render_template('game.html', color='blue' if game.player_a.is_red else 'red', is_inviter=False, game_id=game_id, winner=game.winner_color_string, last_updated=dir_last_updated('static'))
        # try: # if it isn't, we try to make it into a player
        #     new_guest=Guest.query.filter_by(id=flask.session['guest_id']).one()
        #     player=game.add_player(guest=new_guest)
        #     db.session.add(player)
        #     db.session.commit()
        #     return flask.render_template('game.html', color='red' if player.is_red else 'blue', is_inviter=player.is_inviter, game_id=game_id, winner=game.winner_color_string)
        # except game_exceptions.GameIsFull:
        #     return flask.redirect(flask.url_for('home')) # TODO: warning alert in home; in the future a possible spectator mode

@socketio.on('join game')
def handle_join_game(received_json): # TODO: flask.session can be used for checks!
    flask_socketio.join_room(received_json['game_id'])
    # print('someone joined game '+received_json['game_id'])

@socketio.on('make move')
def handle_make_move(received_json): # TODO: flask.session can be used for checks!
    print('------- GUEST {}: /game/{} (make move)'.format(
        flask.session['guest_id'],
        received_json['game_id']
    ))
    game=Game.query.filter_by(id=received_json['game_id']).one() # TODO: missing exception handling (including valid uuid)
    try: # we first check if the guest is already in this game
        player=game.get_player(guest_id=flask.session['guest_id'])
        # print('-----------AFTER GET PLAYER')
    except game_exceptions.NoSuchPlayerInGame:
        if not game.player_b:
            # register as player
            print('-----------NO PLAYER B ' + str(flask.session['guest_id']))
            player=Player()
            # print('---------------------------a')
            # print(flask.session['guest_id'])
            player.guest=Guest.query.filter_by(id=flask.session['guest_id']).one()
            # print('---------------------------b')
            player.is_red=not(game.player_a.is_red)
            # print('---------------------------c')
            game.player_b=player
            # print('player b is red: '+game.player_b.isred)
            db.session.add(game)
            db.session.commit()
        else:
            # set viewer mode
            # print('-----------SET VIEWER MODE')
            print('-----------------------EMIT VIEWER MODE' + str(flask.session['guest_id']))
            flask_socketio.emit('viewer mode')
            return
    finally:
        print('-----------------------FINALLY' + str(flask.session['guest_id']))
        # print('-----------FINALLY')
        move_result=game.move(received_json['coords_from'], received_json['coords_to'])
        # print('-----------AFTER GAME MOVER')
        data_to_send={
            'position': game.position_string,
            'color_of_turn': game.color_string,
            'last_move': game.last_move_coords
        }
        if move_result.__class__==AttackResult:
            data_to_send['attack_result']=move_result.message()
        if move_result.__class__==GameHasEnded:
            data_to_send['winner_color']=move_result.message()
        # print('-----------BEFORE COMMIT')
        db.session.add(game)
        db.session.commit()
        # print('-----------AFTER COMMIT')
        flask_socketio.emit('move made', data_to_send, room=received_json['game_id'])


@app.route('/game/<game_id>/position', methods=['GET'])
def game_position(game_id):
    game=Game.query.filter_by(id=game_id).one() # TODO: exception handling
    data_to_send={
        'position': game.position_string,
        'color_of_turn': game.color_string
    }
    if game.last_move_coords:
        data_to_send['last_move']=game.last_move_coords
    json_to_send=flask.jsonify(data_to_send)
    return json_to_send

# @app.route('/test/<side>', methods=['GET', 'POST'])
# def test(side):
#     if flask.request.method == 'POST':
#         return 'POST to game'
#     else:
#         if not (side in ['red', 'blue']):
#             return flask.redirect(flask.url_for('home'))
#         return flask.render_template('game.html', side=side)

@app.errorhandler(404)
def page_not_found(e):
    return flask.redirect(flask.url_for('home'))

def is_valid_uuid(uuid_to_test, version=4): # TODO: move to better place, utils.py or sth
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

if __name__ == '__main__':
    # game_manager=server_utils.GameManager()
    app.run(threaded=True, port=5000, debug=True)
