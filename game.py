import random
import time

# Notes:
# assume all player stats are 10, no proficiency bonuses, 15hp for player, no zombie undead fortitude
# possibly for undead, bool class variable in Game, if true on death roll for effect, add hp if succeeds?


class Game:
    counter = 0  # counter for deciding action order in main
    attack = 0
    crit_success = False
    crit_fail = False
    user_input = 'INVALID'  # initialize as the error message to allow player_act to start correctly
    damage = 0

    def __init__(self):
        self.action = ''  # action placeholder
        self.attack = 0  # attack placeholder

    def player_act(self):
        Game.counter += 1  # if user input == 'INVALID' statement after this, else to continue
        while Game.user_input == 'INVALID':
            self.action = input('Attack or heal? (a or h)\n')
            user = self.action
            error_check(user)  # error check called to keep user in while loop until valid input is entered
        if Game.user_input == 'a':
            attack_roll('Player')
            if Game.attack > Monster.mon_ac:
                damage_roll('Player')
                damage = Game.damage
                if Game.crit_success:  # if the attack roll method sets either crit to True, certain effects activate
                    print('Critical hit!')
                    time.sleep(1)
                    damage *= 2
                    Game.crit_success = False
                elif Game.crit_fail:
                    print('Critical fail! You hurt yourself!')
                    time.sleep(1)
                    Player.hp -= (damage // 2)
                    damage = 0
                    Game.crit_fail = False
                Monster.mon_hp -= damage  # remove hp based on damage roll
                print(f'You did {damage} damage!\n')
                time.sleep(1)  # use sleep to add pauses throughout program for a more fluid output
                if (Monster.mon_start_hp // 2) > Monster.mon_hp > (Monster.mon_start_hp // 4):  # check if hp
                    # above half
                    print(f'{Monster.monster} is looking wounded!\n')
                elif (Monster.mon_start_hp // 4) > Monster.mon_hp > 0:  # check if hp between half and a quarter
                    # of max
                    print(f'{Monster.monster} is critically wounded!\n')
                elif Monster.mon_hp <= 0:
                    print(f'{Monster.monster} has been killed!')
                else:
                    print(f'{Monster.monster} seems fine!\n')  # default message for above half hp
            else:
                print('Attack blocked!\n')
        elif Game.user_input == 'h':  # ensures there are actually potions to use
            if Player.potion > 0:
                use_potion()
                Game.user_input = 'INVALID'
            else:
                print('Out of potions! You wasted your turn looking for one!')
        Game.user_input = 'INVALID'

    def monster_act(self):
        Game.counter += 1
        print(Monster.monster, 'attacks with', Monster.mon_weapon, '\n')  # call and print monster name and weapon
        time.sleep(1)
        attack_roll(Monster.monster)
        attack = Game.attack
        if attack > Player.ac:
            damage_roll(Monster.monster)
            damage = Game.damage
            if Game.crit_success:
                print('Critical hit!')
                time.sleep(1)
                damage *= 2
                Game.crit_success = False
            elif Game.crit_fail:
                print('Critical fail! It hurt itself!')
                time.sleep(1)
                Monster.mon_hp -= (damage // 2)
                damage = 0
                Game.crit_fail = False
            Player.hp -= damage
            print('You have', Player.hp, 'hp left!\n')
            time.sleep(1)
            if Player.start_hp // 2 >= Player.hp > Player.start_hp // 4:  # section the same as with player action
                print('You are wounded!\n')
            elif Player.start_hp // 4 >= Player.hp > 0:
                print('You are critically wounded!\n')
            elif Player.hp <= 0:
                print('You have died!')
            else:
                print('You\'re ok!\n')
        else:
            print('Attack blocked!\n')


class Player:  # set base stats for the player. May add complexity in the future if needed
    ac = 14
    hp = 15
    start_hp = 15
    p_attack = 0
    p_damage = 0
    potion = 3

    def __init__(self):
        pass


class Monster:
    mon_hp = 1
    mon_ac = 0
    mon_start_hp = 0
    monster = ''
    monster_damage = 0
    mon_weapon = ''

    def __init__(self):
        pass

    def type(self, monster):  # takes call from main with monster being rolled in main. sets class stats for monster
        if monster == 1:
            Monster.monster = 'Kenku'
            Monster.mon_hp = 13
            Monster.mon_start_hp = 13
            Monster.mon_ac = 13
            Monster.mon_weapon = 'Shortsword'
            return 'Kenku'
        elif monster == 2:
            Monster.monster = 'Zombie'
            Monster.mon_hp = 22
            Monster.mon_start_hp = 22
            Monster.mon_ac = 8
            Monster.mon_weapon = 'Slam'
            return 'Zombie'
        elif monster == 3:
            Monster.monster = 'Wolf'
            Monster.mon_hp = 11
            Monster.mon_start_hp = 11
            Monster.mon_ac = 13
            Monster.mon_weapon = 'Bite'
            return 'Wolf'
        elif monster == 4:
            Monster.monster = 'Ape'
            Monster.mon_hp = 19
            Monster.mon_start_hp = 19
            Monster.mon_ac = 12
            Monster.mon_weapon = 'Fist'
            return 'Ape'


def use_potion():  # method for determining health gain from potion usage, also lowers potion count
    print('You have', Player.potion, 'potions! Using one now.\n')
    heal = random.randint(1, 4) + random.randint(1, 4) + 2
    Player.hp += heal  # allows for over healing, can be considered temporary hp
    Player.potion -= 1
    print('You healed:', heal, '\n')
    return Player.hp


def crit_check():  # check if the attack roll returns a 20 or 1 and changes the Bool in Game accordingly
    attack = Game.attack
    if attack == 20:
        Game.crit_success = True
    elif attack == 1:
        Game.crit_fail = True
    pass


def attack_roll(attacker):  # used by both player and monsters to roll the attack die
    attack = random.randint(1, 20)
    Game.attack = attack
    crit_check()  # checks for critical hits
    match attacker:  # switch statement to add the appropriate modifier to the attacker's roll
        case 'Player':
            Game.attack = attack
        case 'Kenku':
            Game.attack = attack + 5
        case 'Zombie':
            Game.attack = attack + 3
        case 'Wolf':
            Game.attack = attack + 4
        case 'Ape':
            Game.attack = attack + 5


def damage_roll(attacker):  # used by both player and monsters to roll for damage
    match attacker:  # rolls the appropriate damage dice depending on the attacker
        case 'Player':
            Game.damage = random.randint(1, 6)
        case 'Kenku':
            Game.damage = random.randint(1, 6) + 3
        case 'Zombie':
            Game.damage = random.randint(1, 6) + 1
        case 'Wolf':
            Game.damage = random.randint(1, 4) + random.randint(1, 4) + 2
        case 'Ape':
            Game.damage = random.randint(1, 6) + 3


def error_check(user):  # ensures the input is either a, h, attack, or heal and is not case-sensitive
    test = user
    test = test.lower()
    if test == 'a' or test == 'attack':
        Game.user_input = 'a'
    elif test == 'h' or test == 'heal':
        Game.user_input = 'h'
    else:  # triggers the loop in player act so that input is requested until a valid input is entered
        Game.user_input = 'INVALID'
        print('You\'re in battle stop messing around!\n')
