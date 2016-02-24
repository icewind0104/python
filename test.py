#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class game():
    def __init__(self, players):
        self._players = players
        self._handler = 0

    def handle2next(self):
        if ( self._handler + 1 ) < len(self._players):
            self._handler = self._handler + 1
        else:
            self._handler = 0

    @property
    def players(self):
        return self._players

    def kick(self):
        kick_player = self._players.pop(self._handler)
        
        # 踢掉当前持花者后，花要交给下一位，由于list POP元素后，下一个元素的index正好要前进一位，故handler不变，但当踢出的是末尾玩家时，handler要调整为0,即第一位玩家
        if self._handler == len(self.players):
            self._handler = 0
        return kick_player

    def get_handler(self):
        return self.players[self._handler]






# main
Players = ['han_meimei', 'li_lei', 'xiao_ming', 'xiao_hong', 'xiao_wang', 'zhang3', 'li4']
timeOfHandle = 7

# Game start
Game = game(players = Players)

while True:
    for i in range(timeOfHandle):
        Game.handle2next()
    print("kick: %s" % Game.kick())

    # 仅剩一人时退出
    if len(Game.players) == 1:
        print(Game.get_handler())
        break




