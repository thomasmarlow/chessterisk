import manager_exceptions
import server_utils
import flask

app = flask.Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    return flask.render_template('home.html')

@app.route('/newgame/invite', methods=['GET'])
def newgame_invite():
    gameview_id_inviter, gameview_id_invited = game_manager.get_new_gameview_id_pair()
    return flask.redirect(flask.url_for('game', gameview_id=gameview_id_inviter))

# @app.route('/newgame/automatch', methods=['GET'])
# def newgame_automatch():
#     return 'New game'

@app.route('/game/<gameview_id>', methods=['GET', 'POST'])
def game(gameview_id):
    if flask.request.method == 'POST':
        return 'POST to game'
    else:
        try:
            game=game_manager.get_game(gameview_id)
        except manager_exceptions.NonExistantGameView:
            return flask.redirect(flask.url_for('home')) # TODO: 404
        side=game.get_side_name(gameview_id)
        invite_link=flask.url_for('game', gameview_id=game.get_invited_id()) if game.is_inviter(gameview_id) else ''
        return flask.render_template('game.html', side=side, invite_link=invite_link)

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
    # your processing here
    return flask.redirect(flask.url_for('home'))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    game_manager=server_utils.GameManager()
    app.run(threaded=False, port=5000, debug=True)