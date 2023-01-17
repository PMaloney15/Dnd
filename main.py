import time
import random
import game

# Author: Patrick Maloney

# This program simulates a simple fight encounter in the style of Dungeons and Dragons. Rolls emulated by the random
# module and the corresponding modifiers are based on information from the 5th edition Player's handbook and
# Monster manual.


class Main:
    def play(self):
        print('Combat!')
        time.sleep(1)
        print(f'Fighting a(n) {game.Monster.type(self, random.randint(1, 4))}!\n')  # initializes a random monster
        time.sleep(1)
        fight = game.Game()
        initiative = random.randint(1, 2)  # randomly decide who acts first, player on 1, monster on 2
        if initiative == 1:
            game.Game.player_act(self)
            while game.Player.hp > 0 and game.Monster.mon_hp > 0:  # while loops use counter to continue the fight
                if game.Game.counter % 2 != 0:
                    game.Game.monster_act(self)
                else:
                    game.Game.player_act(self)
        else:
            game.Game.monster_act(self)
            while game.Player.hp > 0 and game.Monster.mon_hp > 0:
                time.sleep(1)
                if game.Game.counter % 2 != 0:
                    game.Game.player_act(self)
                else:
                    game.Game.monster_act(self)


game1 = Main()
game1.play()
