"""Example client."""
import asyncio
import getpass
import json
import os
import math

# Next 4 lines are not needed for AI agents, please remove them from your code!
import websockets

from complementary_functions import *
from tree_search import *
from mapa import *

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        digdug_direction = Direction.EAST

        #### DIGDUG NONSTOP
        digdug_position_counter = 0
        previous_digdug_pos = []
        new_previous_digdug_position = []
        while True:

            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                if 'map' in state:
                    map = Map(mapa=state['map'])
                key = ""

                if 'level' in state:
                    level = state.get('level')

                digdug_position = state.get('digdug')

                #### DIGDUG NONSTOP
                if previous_digdug_pos == []:
                    previous_digdug_pos = new_previous_digdug_position
                new_previous_digdug_position = digdug_position

                if previous_digdug_pos == digdug_position:
                    digdug_position_counter += 1
                else:
                    digdug_position_counter = 0

                enemies = state.get('enemies')
                distances = []
                dists = {}
                rocks = state.get('rocks', [])

                if rocks != None:
                    rocks_pos = []
                    for r in rocks:
                        rocks_pos.append(r['pos'])

                # LineCounter = -1
                # Columns_with_empty_spaces = []
                # Enemies_in_Vertical = []
                # for i in map:
                #     LineCounter +=1
                #     for j in range(2, len(i)):
                #         if i[j] == 0 and i[j-1] == 0 and i[j-2] == 0 and i[j] == i[j-1]:
                #             if LineCounter in Columns_with_empty_spaces:
                #                 continue
                #             else:
                #                 Columns_with_empty_spaces.append(LineCounter)
                #                 print("Colunas com espaços cavados", LineCounter)
                #         else:
                #             pass

                if enemies != None:
                    for enemy in enemies:
                        enemyPos = enemy['pos']
                        distance = math.dist(digdug_position, enemyPos)
                        dists[distance] = enemy['id']
                        distances.append(distance)
                    if distances != []:
                        minDistance = min(distances)

                    for enemy in enemies:
                        if enemy['id'] == dists[minDistance]:
                            closest_enemy = enemy
                            break

                    if closest_enemy is not None:
                        closest_enemy_pos = closest_enemy['pos']
                        closest_enemy_dir = closest_enemy['dir']
                        closest_enemy_type = closest_enemy['name']

                        if checkIfPookaIsGhost(closest_enemy):
                            key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)

                        if level >= 7 and digdug_position_counter >= 10:
                            if closest_enemy_dir == Direction.WEST:
                                key = "d"
                            elif closest_enemy_dir == Direction.EAST:
                                key = "a"
                            elif closest_enemy_dir == Direction.NORTH:
                                key = "s"
                            else:
                                key = "w"
                            
                        if key == "":
                            if minDistance <= 3:

                                if closest_enemy_dir == Direction.EAST or closest_enemy_dir == Direction.WEST:

                                    if digdug_position[1] == closest_enemy_pos[1]: # If Dig Dug is in the same row as the enemy
                                        if digdug_position[0] < closest_enemy_pos[0]: # If Dig Dug is to the left of the enemy
                                            if map.map[digdug_position[0] + 1][digdug_position[1]] == Tiles.STONE: 

                                                if digdug_position[0] + 2 == closest_enemy_pos[0]:
                                                    key = 'a'

                                                else:
                                                    if checkIfPookaIsGhost(closest_enemy):
                                                        key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 'd'
                                            else:   
                                                if digdug_position[0] + 1 == closest_enemy_pos[0]:
                                                    if digdug_position[0] == 0 or digdug_position[0] == 47:
                                                        key = checkEndOfMap(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)

                                                    elif closest_enemy_type == 'Fygar':
                                                        key = runAwayFromFygarFlame(closest_enemy_pos, closest_enemy_dir, digdug_position, minDistance, closest_enemy)

                                                    else:
                                                        key = rockNearBy(rocks, digdug_position)
                                                    
                                                else:
                                                    key = 'A'
                                        else: # If Dig Dug is to the right of the enemy
                                            if map.map[digdug_position[0] - 1][digdug_position[1]] == Tiles.STONE:

                                                if digdug_position[0] - 2 == closest_enemy_pos[0]:
                                                    key = 'w'

                                                else:
                                                    key = 'a'

                                            else:
                                                if closest_enemy_pos[0] == digdug_position[0] - 1:
                                                    if digdug_direction == Direction.WEST:
                                                        key = 'A'
                                                    elif closest_enemy_type == 'Fygar':
                                                        key = runAwayFromFygarFlame(closest_enemy_pos, closest_enemy_dir, digdug_position, minDistance, closest_enemy)

                                                    else: 
                                                        key = 'w'
                                                else:
                                                    if minDistance <= 1:
                                                        key = 'w'
                                                    else:
                                                        key = 'A'
                                    elif digdug_position[1] < closest_enemy_pos[1]: # If Dig Dug is above the enemy in a diferent row
                                        if map.map[digdug_position[0]][digdug_position[1] + 1] == Tiles.STONE:
                                            if closest_enemy_pos[0] == digdug_position[0] and digdug_position[1] + 2 == closest_enemy_pos[1]: # if Dig Dug and the enemy are in the same column
                                                key = 'w'

                                            else:
                                                if minDistance <= 2:
                                                    if checkIfPookaIsGhost(closest_enemy):
                                                        key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 'a'
                                                else:
                                                    key = 's'

                                        else:
                                            if digdug_position[0] == closest_enemy_pos[0]:
                                                if digdug_direction != Direction.SOUTH or minDistance <= 1:
                                                    if checkIfPookaIsGhost(closest_enemy):
                                                        key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 'w'
                                                if minDistance > 1:
                                                    key = 's'
                                                
                                                key = 'A'
                                            else:
                                                if digdug_direction != Direction.SOUTH:
                                                    if checkIfPookaIsGhost(closest_enemy):
                                                        key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 'w'
                                                else:
                                                    if minDistance <= 1:
                                                        key = "w"
                                                    else:
                                                        key = 'A'
                                    elif digdug_position[1] > closest_enemy_pos[1]: # If Dig Dug is below the enemy in a diferent row
                                        if map.map[digdug_position[0]][digdug_position[1] - 1] == Tiles.STONE: 

                                            if closest_enemy_pos[0] == digdug_position[0] and digdug_position[1] - 2 == closest_enemy_pos[1]: # if Dig Dug and the enemy are in the same column
                                                key = 'a'
                                            else:
                                                if minDistance <= 2:
                                                    key = 's'
                                                else:
                                                    key = 'w'
                                        else:
                                            if digdug_position[0] == closest_enemy_pos[0]:
                                                if digdug_direction != Direction.NORTH:
                                                    key = 's'
                                                else:
                                                    key = 'A'
                                            else:
                                                if minDistance <= 1 or digdug_direction != Direction.NORTH:
                                                    if digdug_position[1] == 23:
                                                        key = 'a'
                                                    else:
                                                        key = 's'
                                                else:
                                                    key = 'A'
                                elif closest_enemy_dir == Direction.NORTH or closest_enemy_dir == Direction.SOUTH:      
                                    if digdug_position[0] == closest_enemy_pos[0]: # If dig dug and the closest enemy are in the same column
                                        if digdug_position[1] < closest_enemy_pos[1]: # If dig dug is above the enemy
                                            if map.map[digdug_position[0]][digdug_position[1] + 1] == Tiles.STONE:
                                                if closest_enemy_pos[1] == digdug_position[1] + 2:
                                                    key = 'a'
                                                else:
                                                    key = 's'
                                            else:
                                                if closest_enemy_pos[1] == digdug_position[1] + 1:
                                                    if digdug_position[1] == 0 or digdug_position[1] == 23:
                                                        key = checkEndOfMap(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 'w'
                                                else:
                                                    key = 'A'

                                        elif digdug_position[1] > closest_enemy_pos[1]: # If dig dug is bellow the enemy and in the same column
                                            if map.map[digdug_position[0]][digdug_position[1] - 1] == Tiles.STONE:
                                                if closest_enemy_pos[1] == digdug_position[1] - 2:
                                                    key = 's'
                                                else:
                                                    key = 'w'
                                            else:
                                                if closest_enemy_pos[1] == digdug_position[1] - 1:
                                                    if digdug_position[1] == 0 or digdug_position[1] == 23:
                                                        key = checkEndOfMap(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 's'
                                                else:
                                                    key = 'A'
                                    elif digdug_position[0] < closest_enemy_pos[0]: # If dig dug is to the left of the enemy in a diferent column

                                        if map.map[digdug_position[0] + 1][digdug_position[1]] == Tiles.STONE:
                                            if closest_enemy_pos[1] == digdug_position[1] and closest_enemy_pos[0] == digdug_position[0] + 2:
                                                key = 'w'
                                            else:
                                                if minDistance <= 2:
                                                    if checkIfPookaIsGhost(closest_enemy):
                                                        key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = ''
                                                else:
                                                    if checkIfPookaIsGhost(closest_enemy):
                                                        key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                    else:
                                                        key = 'd'
                                        else:
                                            if digdug_direction == Direction.EAST:
                                                key = 'A'
                                            else:
                                                if checkIfPookaIsGhost(closest_enemy):
                                                    key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                else:
                                                    key = 'a'
                                    elif digdug_position[0] > closest_enemy_pos[0]: # If dig dug is to the right of the enemy of the column
                                        if map.map[digdug_position[0] - 1][digdug_position[1]] == Tiles.STONE:

                                            if closest_enemy_pos[1] == digdug_position[1] and closest_enemy_pos[0] == digdug_position[0] - 2:
                                                key = 'w'
                                            else:
                                                if minDistance <= 2:
                                                    key = 'd'    
                                                else:
                                                    key = 'a'
                                        else:
                                            if minDistance <= 1:
                                                if checkIfPookaIsGhost(closest_enemy):
                                                    key = run(digdug_position, closest_enemy_pos, closest_enemy_dir, minDistance)
                                                else:
                                                    key = 'w'
                                            else:
                                                key='A'
                            else:
                                keys = a_star_search(digdug_position, closest_enemy['pos'], [rock['pos'] for rock in rocks]  )
                                key = keys[0]

                            #### DIGDUG NONSTOP
                            previous_digdug_pos = new_previous_digdug_position
                            # Update map
                            if key != 'A':
                                if key == 'w':
                                    update_pos = [digdug_position[0], digdug_position[1] - 1]
                                    digdug_direction = Direction.NORTH
                                elif key == 'a':
                                    update_pos = [digdug_position[0] - 1, digdug_position[1]]
                                    digdug_direction = Direction.WEST
                                elif key == 's':
                                    update_pos = [digdug_position[0], digdug_position[1] + 1]
                                    digdug_direction = Direction.SOUTH
                                elif key == 'd':
                                    update_pos = [digdug_position[0] + 1, digdug_position[1]]
                                    digdug_direction = Direction.EAST

                                map.dig(update_pos)
                        
                # {'level': 1, 'step': 15, 'timeout': 3000, 'player': 'josemcg', 'score': 0, 'lives': 3, 'digdug': [1, 16], 
                # 'enemies': [{'name': 'Fygar', 'id': 'aa5d5e57-0f84-4da6-8821-7a28902e47a9', 'pos': [32, 6], 'dir': 3, 'fire': [[31, 6], [30, 6], [29, 6]]}, 
                #           {'name': 'Pooka', 'id': 'de2f1597-0139-4a1c-bdb1-33805a5fe04b', 'pos': [9, 16], 'dir': 3}, 
                #           {'name': 'Pooka', 'id': '2696ba52-145c-41ac-bb8d-a6edf516f65b', 'pos': [34, 6], 'dir': 2}], 
                # 'rocks': [{'id': '06dd0e40-7f50-4ca4-beb0-6b7e49f4e3f2', 'pos': [7, 12]}]}
                await websocket.send(json.dumps({"cmd": "key", "key": key}))

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))