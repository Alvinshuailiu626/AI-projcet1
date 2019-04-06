"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import sys
import json

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.openlist=[]

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)

class Astar:
    class Node:
        def __init__(self, point):
            self.points=points
            self.father = None
            self.nextMovePoint=None
            self.nextMove=None
            self.g=0
            self.h=0
            self.openlist=[]
            self.movelist=[Point(1,0),Point(1,-1),Point(0,-1),Point(-1,0),Point(-1,1),Point(0,1)]
        def searchNear(self):
            for point in points:
                New_point_list=[]
                for move in movelist:
                     new_point=point.x+move.x
                     new_point=point.y+move.y
                     if  new_node_X not in ran or new_node_Y not in ran :
                         return
                     currentPoint = Point(new_node_X, new_node_Y)
                     if self.points.__contains__(currentPoint) or self.blockset.__contains__(currentPoint) :
                         if not self.points.__contains__(Point(new_node_X+move.x,new_node_Y+move.y)) and not self.blockset.__contains__(Point(new_node_X+move.x,new_node_Y+move.y)) :
                             currentPoint = Point(new_node_X+move.x,new_node_Y+move.y)
                         else :
                             return

            opennode = node.pointInOpenList(currentPoint)
            if not opennode:
                opennode = Astar.Node(currentPoint)
                opennode.father = node
                node.openlist.append(opennode)

            return
    def __init__(self,board_dict,pieceset,blockset,final_position):
        # 寻路地图

        self.pieceset=pieceset
        self.blockset=blockset
        self.closelist=[]
        self.final_possition=final_position
        self.nodes=[]

        #createnodes
    def getMinNode(self):
        currentNode = self.nodes[0]
        for node in self.nodes:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    def pointInCloseList(self,node):
        for point in node.points:
            for endpoint in node.close_list:
                if point == endpoint:
                    return True


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} |
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        data = json.load(file)
        board_dict={}
        blockset=[]
        pieceset=[]

        open_list={}
        close_list={}
        ran = range(-3, +3+1)
        for pieces in data.keys():
            if pieces == "pieces":
                for piece in data[pieces]:
                    board_dict[tuple(piece)]=data['colour']
                    pieceset.append(Point(piece[0],piece[1]))
            elif pieces == "blocks":
                for block in data[pieces]:
                    board_dict[tuple(piece)]="blocks"
                    blockset.append(Point(block[0],block[1]))
