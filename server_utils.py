import random
import string
import manager_exceptions

class GameManager:
    def __init__(self):
        random.seed()
        self.games=[]
        self.id_manager=IDManager(12)

    def generate_game(self):
        new_game=Game(self.id_manager)
        self.games.append(new_game)
        return new_game

    def get_new_gameview_id_pair(self):
        game=self.generate_game()
        return game.get_id_pair()

    def get_game(self, gameview_id):
        if not self.games:
            raise manager_exceptions.NonExistantGameView()
        return next(game for game in self.games if game.has_gameview_id(gameview_id))

class Game:
    def __init__(self, id_manager):
        ids = [id_manager.generate_new_id(), id_manager.generate_new_id()]
        is_inviter=[True, False]
        random.shuffle(ids)
        random.shuffle(is_inviter)
        self.blue=BoardSide(gameview_id=ids[0], is_inviter=is_inviter[0])
        self.red=BoardSide(gameview_id=ids[1], is_inviter=is_inviter[1])

    def get_id_pair(self):
        if self.blue.is_inviter:
            return self.blue.gameview_id, self.red.gameview_id
        else:
            return self.red.gameview_id, self.blue.gameview_id

    def has_gameview_id(self, gameview_id):
        return (self.blue.gameview_id==gameview_id) or (self.red.gameview_id==gameview_id)

    def get_side_name(self, gameview_id):
        if self.blue.gameview_id==gameview_id:
            return 'blue'
        else:
            return 'red'

    def is_inviter(self, gameview_id):
        if self.blue.gameview_id==gameview_id:
            return self.blue.is_inviter
        else:
            return self.red.is_inviter

    def get_invited_id(self):
        if not self.blue.is_inviter:
            return self.blue.gameview_id
        else:
            return self.red.gameview_id    


class IDManager:
    def __init__(self, id_length):
        self.ids=[]
        self.id_length=id_length

    def generate_new_id(self):
        id=self.generate_id()
        while id in self.ids:
            id=self.generate_id()
        self.ids.append(id)
        return id

    def generate_id(self):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(self.id_length))
        
class BoardSide:
    def __init__(self, gameview_id, is_inviter):
        self.gameview_id=gameview_id
        self.is_inviter=is_inviter
