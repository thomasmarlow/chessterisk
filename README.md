# chessterisk*
*"A chess-like online board game, with RNG-based initial position and capturing efficacy."*

Currently running on https://chessterisk.herokuapp.com/

#### Looks, as of now:

![Getting somewhere](https://media.giphy.com/media/kucRgSSmSObdhqeh0N/giphy.gif)

## TODOs:

##### Backend
- [x] Integration with PostgresDB
- [x] Game invites with Flask-SQLAlchemy
- [ ] Automatch with Flask-SQLAlchemy
- [ ] Organise `*.py`s into module/package structure
- [ ] 10k row cap: set max. amount of simultaneously persisted games, players and guests (include creation_time in tables?)

##### Front+back
- [ ] Integration with SocketIO for players to be able to listen to their oponents' moves; gunicorn settings?

##### Frontend
- [ ] Add error views instead of redirecting to `/home`
- [ ] Add turn tracker to front (define how will it look)
- [ ] Enhance board sizing (`vmin`?)
- [ ] Replace king symbol for https://fontawesome.com/icons/crown?style=solid

##### Additional
- [ ] Search about timer implementation for games

## Useful information:
* https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
* https://flask.palletsprojects.com/en/1.1.x/quickstart/
* https://medium.com/analytics-vidhya/heroku-deploy-your-flask-app-with-a-database-online-d19274a7a749
* https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
* https://stackoverflow.com/questions/20460339/flask-sqlalchemy-constructor
* https://docs.sqlalchemy.org/en/13/orm/cascades.html#unitofwork-cascades
* https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
* https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/
