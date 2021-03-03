import flask
app = flask.Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    return 'Home'

@app.route('/newgame', methods=['GET'])
def new_game():
    return 'New game'

@app.route('/game/<gameview_id>', methods=['GET', 'POST'])
def game(gameview_id):
    if flask.request.method == 'POST':
        return 'POST to game'
    else:
        return flask.render_template('game.html')

@app.route('/test/<side>', methods=['GET', 'POST'])
def test(side):
    if flask.request.method == 'POST':
        return 'POST to game'
    else:
        return flask.render_template('game.html', side=side)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)