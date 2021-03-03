# chessterisk
A chess-like online board game, with RNG-based initial position and capturing efficacy.

### Looks, as of now:

![Getting somewhere](https://media.giphy.com/media/kucRgSSmSObdhqeh0N/giphy.gif)

### Testing routes:
- `/test/blue`: Test as blue
- `/test/red`: Test as red

### TODOs:
- [ ] Flask server
	- [ ] `GET /home`: "new game" button
	- [ ] `GET /newgame`: generate ID per side, redirect to game
	- [ ] `GET /game/{id}`: game view
	- [ ] `POST /game/{id}`: game API
	- [ ] Adapt existing domain to Flask interface
- [ ] Add turn tracker to front (define how)
- [ ] Organize `*.py` into packages/modules

### Useful information:
* https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
* https://flask.palletsprojects.com/en/1.1.x/quickstart/
