from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
#traversal_path = ['n', 'n']
traversal_path = []

# Queue and Stack classes to use with graph traversals.
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


# Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.

# FIRST PASS PSEUDOCODE

# Going to be starting traversal from room '0'.
# Pick a direction (at random), and perform a Depth First Traversal down that path.
# Keep track of what was visited.
# Keep track of the path that we have gone to visit each room.
# When we reach a room that has nothing left to explore, we will need to backtrack to look for a new path.
# When a direction is selected, add it to the traversal_path list
# For each room you enter:
#   - Call player.current_room.id -> Room ID to add to the
#   - Call player.current_room.get_exits
#   - Perform a Breadth First Search to fill in the details for any room with a '?' for an exit.
#       - The '?' will be the focus of the search, instead of a target vertex.
#       - If an exit has been explored, you can put it in your BFS queue like normal.
#       - BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add
#         it to your traversal path.
#   - Call player.travel(direction) to move to the next room.

visited = {
    player.current_room.id: {}
} # dictionary
# Create an empty queue and enqueue A PATH TO the starting vertex ID.
s = Stack()
# hold the ID of the starting room:
starting_room = player.current_room.id
previous_room = None
breadcrumbs = []

# get direction for backtracking once all the exits of a room have been searched
def backtrack(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'

path = [random.choice(player.current_room.get_exits())]
s.push(path)
breadcrumbs.append(backtrack(path))

starting_exits = player.current_room.get_exits()

for start_exits in starting_exits:
    visited[player.current_room.id][start_exits] = "?"

print('Breadcrumbs', breadcrumbs)

while len(visited) < len(room_graph):
    # Pop from the top of the stack, this is our current path.
    current_path = s.pop()
    previous_room = player.current_room.id
    # current_direction is the last thing in the path
    current_direction = current_path[-1]
    player.travel(current_direction)
    curr_room_id = player.current_room.id
    traversal_path.append(current_direction)

    visited[previous_room][current_direction] = player.current_room.id
    
    # print('current_node', curr_room_id)
    # Check if we've visited yet, if not:
    if player.current_room.id not in visited:
        # mark as visited
        visited[player.current_room.id] = {}
    
    if previous_room is not None:
        visited[player.current_room.id][backtrack(current_direction)] = previous_room
        
    # get the current room's exits
    neighboring_rooms = player.current_room.get_exits()

    # next_room = random.choice(neighboring_rooms)
    # keep track of unsearched rooms
    unsearched_rooms = []
    # iterate over the rooms
    for room in neighboring_rooms:
        #print('Room', room)
        if room not in visited[player.current_room.id]:
            visited[player.current_room.id][room] = "?"

        if visited[player.current_room.id][room] is "?":
            unsearched_rooms.append(room)
        print("Unsearched rooms", unsearched_rooms)
    if len(unsearched_rooms) > 0:
        s.push(unsearched_rooms[-1])
        breadcrumbs.append(backtrack(unsearched_rooms[-1]))
    else:
        back = breadcrumbs.pop()
        s.push(back)
        
        # loop through each of the exits for the current room
        # if the value is '?', then add that that room to the stack to be visited.
        # 

        
        
print('Visited', visited)
print('Traversal Path', traversal_path)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
