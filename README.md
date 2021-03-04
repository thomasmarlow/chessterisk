# chessterisk*
*"A chess-like online board game, with RNG-based initial position and capturing efficacy."*

Currently running on https://chessterisk.herokuapp.com/

### Looks, as of now:

![Getting somewhere](https://media.giphy.com/media/kucRgSSmSObdhqeh0N/giphy.gif)

### TODOs:
- [ ] Adapt existing domain to server interface (organize `*.py` into packages/modules?)
  - ...before implementing DB
  - ...only runnable on local server with `threaded=False`
- [ ] Integration with PostgresDB through SQLAlchemy
- [ ] Add error views instead of redirecting to `/home`
- [ ] Set max. amount of simultaneously persisted games (100/1000?)
- [ ] Search about timer implementation for games
- [ ] Add turn tracker to front (define how)
- [ ] Enhance board sizing (`vmin`?)
- [ ] Replace king symbol for https://fontawesome.com/icons/crown?style=solid

### Useful information:
* https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
* https://flask.palletsprojects.com/en/1.1.x/quickstart/
* https://medium.com/analytics-vidhya/heroku-deploy-your-flask-app-with-a-database-online-d19274a7a749
* https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
* https://stackoverflow.com/questions/20460339/flask-sqlalchemy-constructor
