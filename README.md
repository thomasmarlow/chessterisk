# chessterisk
A chess-like online board game, with certain events being determined by chance.

### Looks, as of now:

![Getting somewhere](https://media.giphy.com/media/E6KQ6vrBH6G9Ziwgvs/giphy.gif)

### TODOs:
- [x] Automize board creation
	- [x] Initial placeholders (empty disabled squares)
	- [x] Identify square `button`s with `id="board-square-i-j"`
	- [x] Design protocol for creation through async API
	- [x] ~Keep track of square logic through 2D matrix~ No need to
- [ ] Flask server
	- [ ] `GET /home`: "new game" button
	- [ ] `GET /newgame`: generate ID per side, redirect to game
	- [ ] `GET /game/{id}`: game view
	- [ ] `POST /game/{id}`: game API
	- [ ] Adapt existing domain to Flask interface
- [ ] Add turn tracker to front (define how)
- [ ] Organize `*.py` into packages/modules
- [x] Change `btn-warning`s to `btn-secondary`s; warnings can be left for movable enemy pieces

### Useful information:
* https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
