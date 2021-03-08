from server import db, app

with app.app_context():
    db.create_all()

print('db.create_all() run!')