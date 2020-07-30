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

visited = {} # dictionary
# Create an empty queue and enqueue A PATH TO the starting vertex ID.
s = Stack()

path = [player.current_room.id]
s.push(path)
# While the Stack is not empty...
while s.size() > 0:
# Pop from the top of the stack, this is our current path.
    current_path = s.pop()
# current_node is the last thing in the path
    current_node = current_path[-1]
    print('current_node', current_node)
# Check if we've visited yet, if not:
    if current_node not in visited:
        # mark as visited
        visited[current_node] = {}
        room_exits = player.current_room.get_exits()
        
        for room in room_exits:
            visited[current_node][room] = '?'
        traversal_path.append(current_node)
        # get the current room's exits
        neighboring_rooms = player.current_room.get_exits()
        # iterate over the rooms
        for room in neighboring_rooms:
            # add the neighbor to the path
            neighbor_path = current_path.copy()
            neighbor_path.append(room)
            # Push the neighbor's path on the stack
            s.push(neighbor_path)
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
