# Diogo Falcão - 108712
# José Gameiro - 108840
# João Luís - 107403

from tree_search import *
from consts import *
from consts import *



def runAwayFromFygarFlame(enemy_position, enemy_direction, digdug_pos, distance, list):
    if digdug_pos[0] < enemy_position[0]: # If dig dug is on the left
        if enemy_direction == Direction.WEST:
            if fygarisFlaming(list):
                if distance <= 3:
                    return "w"
                else:
                    return "a"
            else:
                if distance <= 2:
                    return "A"
                else:
                    return "d"
        else:
            if distance <= 3:
                return "A"
            else:
                return "d"
    else: # If dig dug is on the right
        if enemy_direction == Direction.EAST:
            if fygarisFlaming(list):
                if distance <= 3:
                    return "s"
                else:
                    return "d"
            else:
                if distance <= 2:
                    return "A"
                else:
                    return "a"
        else:
            if distance <= 3:
                return "A"
            else:
                return "a"
            
def fygarisFlaming(list):
    if 'fire' in list:
        return True
    return False

def checkIfPookaIsGhost(closest_enemy):
    if 'traverse' in closest_enemy:
        if closest_enemy['traverse'] == True:
            return True
    return False

def rockNearBy(rocks, player_pos):
    key= ""
    for rock in rocks:
        rock_pos = rock['pos']
        if player_pos[0] == rock_pos[0]-1 or player_pos[0] == rock_pos[0]+1:
            key= "w"
        elif player_pos[1] == rock_pos[0]-1:
            key= "d"
        else:
            key = "a"
    return key   

def checkEndOfMap(digdug_pos, enemy_pos, enemy_dir, minDistance):
    if digdug_pos[1] == enemy_pos[1] and enemy_dir == Direction.EAST or enemy_dir == Direction.WEST:
        if (digdug_pos[0] == 0 or digdug_pos[0] == 47) and minDistance <= 2:
            if digdug_pos[1] == 0:
                return "s"
            else:
                return "w"
        
    elif digdug_pos[0] == enemy_pos[0] and enemy_dir == Direction.NORTH or enemy_dir == Direction.SOUTH:

        if (digdug_pos[1] == 0 or digdug_pos[1] == 23) and minDistance <= 2:
            if digdug_pos[0] == 0:
                return "d"
            else:
                return "a"
        
        

def run(digdug_pos, enemy_pos, enemy_dir, enemy_distance):
    if enemy_distance <=4:
        if digdug_pos[1] == enemy_pos[1]:
            if digdug_pos[0] > enemy_pos[0] and enemy_dir == 3:
                return "d"
            elif digdug_pos[0] < enemy_pos[0] and enemy_dir == 1:
                return "a"
        elif digdug_pos[0] == enemy_pos[0]:
            if digdug_pos[1] > enemy_pos[1] and enemy_dir == 2:
                return "s"
            elif digdug_pos[1] < enemy_pos[1] and enemy_dir == 0:
                return "w"
    return ""
            


