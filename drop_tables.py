from server import db, app

with app.app_context():
    db.drop_all()

print('db.drop_all() run!')