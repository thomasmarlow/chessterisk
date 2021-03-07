# chessterisk*
*"A chess-like RNG-based online board game."*

Currently running on https://chessterisk.herokuapp.com/

#### Looks, as of now:

![Getting somewhere](https://media.giphy.com/media/jgH1X6U5U7EiQJtAHu/giphy.gif)

## TODOs:

##### Next up
- [ ] Track last move for each game
- [ ] 10k row cap: set max. amount of simultaneously persisted games, players and guests (include creation_time in tables and wipe db periodically?)
- [ ] Add frontend gradient for turn tracking
- [ ] Add draw recognition
- [ ] Add draw proposal feature
- [ ] Add rematch feature
- [ ] Add sounds for moves, attacks (captures and blocks) and ending.
- [ ] Add metadata and favicon
- [ ] Check and fix/refactor all TODOs
- [ ] Add automatch feature
- [ ] Organise `*.py`s into module/package structure
- [ ] Add error handling for `request` related issues
- [ ] Enhance board sizing
- [ ] Add `/rules` and `/about`

##### Down the road
- [ ] Think about timer implementation
- [ ] Try PyMODM integration
- [ ] Switch to vanilla js or React

## Useful information:
* https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
* https://flask.palletsprojects.com/en/1.1.x/quickstart/
* https://medium.com/analytics-vidhya/heroku-deploy-your-flask-app-with-a-database-online-d19274a7a749
* https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
* https://stackoverflow.com/questions/20460339/flask-sqlalchemy-constructor
* https://docs.sqlalchemy.org/en/13/orm/cascades.html#unitofwork-cascades
* https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
* https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/
* https://stackoverflow.com/questions/61852364/unable-to-update-database-using-flask-sqlalchemy-and-flask-socket-io
