from models import db, Guest

def get_new_guest_id():
    return Guest().id

def get_new_game_id():
    pass Game().id