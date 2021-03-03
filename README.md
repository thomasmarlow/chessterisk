# chessterisk
A chess-like online board game, with certain events being determined by chance.

### For now

![So sad](https://media.giphy.com/media/pSWD6t2AH4gdtNqE80/giphy.gif)

### TODOs
- [ ] Automize board creation
	- [ ] Initial placeholders (empty disabled squares)
	- [ ] Identify square `button`s with `id="board-square-i-j"`
	- [ ] Design protocol for creation through async API
	- [ ] Keep track of square logic through 2D matrix
- [ ] Flask server
	- [ ] `GET /home`: "new game" button
	- [ ] `GET /newgame`: generate ID pair, redirect to game
	- [ ] `GET /game/{id}`: game view
	- [ ] `POST /game/{id}`: game API
	- [ ] Adapt existing domain to Flask interface
- [ ] Add turn tracker to front (?)
- [ ] Organize `*.py` into packages/modules
- [ ] Change `btn-warning`s to `btn-secondary`s; warnings can be left for movable enemy pieces
