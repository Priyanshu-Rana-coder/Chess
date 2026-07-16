import random
from play_chess.act import Game

class Room:
    def __init__(self, room_id, user1=None, user2=None):
        self.room_id = room_id
        self.white = user1
        self.black = user2
        self.white_socket = None
        self.black_socket = None
        self.game = Game()
        self.started = False
        self.finished = False

class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.user_rooms = {}

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def delete_room(self, room_id):
        room = self.rooms.get(room_id)
        if room is not None:
            del self.user_rooms[room.white["username"]]
            if room.black is not None:
                del self.user_rooms[room.black["username"]]
            del self.rooms[room_id]

    def create_room(self, user):
        if user["username"] in self.user_rooms:
            room_id = self.user_rooms[user["username"]]
            return self.rooms[room_id]
        chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
        while True:
            new_room_id = ''
            for i in range(10):
                new_room_id += random.choice(chars)
            if new_room_id not in self.rooms:
                self.rooms[new_room_id] = Room(new_room_id, user1=user)
                self.user_rooms[user["username"]] = new_room_id
                return self.rooms[new_room_id]

    def join_room(self, user, room_id):
        if user["username"] in self.user_rooms:
            existing_room_id = self.user_rooms[user["username"]]
            return self.rooms[existing_room_id]
        room = self.rooms.get(room_id)
        if room is None:
            return None
        if room.black is not None:
            return "full"
        room.black = user
        room.started = True
        self.user_rooms[user["username"]] = room_id
        return room
    
MANAGER = RoomManager()