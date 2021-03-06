# chessterisk*
*"A chess-like online board game, with RNG-based initial position and capturing efficacy."*

Limited testing version running on https://chessterisk.herokuapp.com/

#### Looks, as of now:

![Getting somewhere](https://media.giphy.com/media/jgH1X6U5U7EiQJtAHu/giphy.gif)

## TODOs:

##### Remaining until next release
- [x] Integration with SocketIO
- [ ] Fix game invite issue
- [ ] Add possible game endings to `game_move_results`
- [ ] Add frontend turn tracking + alert messages (block users from selecting pieces when it's not their turn)
- [ ] Replace king symbol for https://fontawesome.com/icons/crown?style=solid
- [ ] 10k row cap: set max. amount of simultaneously persisted games, players and guests (include creation_time in tables and wipe db periodically?)
- [ ] 2nd deployment (adding Postgres DB + probably tweaking gunicorn settings)

##### Next up
- [ ] Automatch feature
- [ ] Organise `*.py`s into module/package structure
- [ ] Add error views instead of redirecting to `/home`
- [ ] Enhance board sizing (`vmin`?)

##### Additional
- [ ] Search about timer implementation for games
- [ ] Try PyMODM integration?

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
