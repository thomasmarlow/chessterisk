# import manager_exceptions
# import server_utils
import db_utils
from models import db, Game
import flask
import flask_sqlalchemy
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://chessterisk:chessterisk@localhost:5432/chessterisk'
db.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # TODO: randomize

@app.route('/home', methods=['GET'])
def home():
    if not 'guest_id' in flask.session:
        flask.session['guest_id'] = db_utils.get_new_guest_id()
    return flask.render_template('home.html')

@app.route('/newgame/invite', methods=['GET'])
def newgame_invite():
    if not 'guest_id' in flask.session:
        flask.session['guest_id'] = db_utils.get_new_guest_id()
    new_game_id=db_utils.get_new_game_id()
    return flask.redirect(flask.url_for('game', game_id=new_game_id))

# @app.route('/newgame/automatch', methods=['GET'])
# def newgame_automatch():
#     return 'New game'

@app.route('/game/<game_id>', methods=['GET', 'POST'])
def game(game_id):
    if flask.request.method == 'POST':
        return 'POST to game'
    else:
        if not 'guest_id' in flask.session:
            return flask.redirect(flask.url_for('home'))
        try:
            game=Game.query.filter_by(id=game_id).one()
        except NoResultFound:
            pass
        except MultipleResultsFound:
            pass
        
        

        # try:
        #     game=game_manager.get_game(gameview_id)
        # except manager_exceptions.NonExistantGameView:
        #     return flask.redirect(flask.url_for('home')) # TODO: 404
        # side=game.get_side_name(gameview_id)
        # invite_link=flask.url_for('game', gameview_id=game.get_invited_id()) if game.is_inviter(gameview_id) else ''
        # return flask.render_template('game.html', side=side, invite_link=invite_link)

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

if __name__ == '__main__':
    # game_manager=server_utils.GameManager()
    app.run(threaded=False, port=5000, debug=True)