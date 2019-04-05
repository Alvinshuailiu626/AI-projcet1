
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
        self.flag = False
    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)

class Astar:
    class Node:
        def __init__(self, point):
            self.point=point
            self.father = None
            self.nextMove=None
            self.openlist=[]
            self.closelist=[]
        def pointInCloseList(self, point):
            for node in self.closelist:
                if node.point == point:
                    return True
            return False
        def pointInOpenList(self, point):
            for node in self.openlist:
                if node.point == point:
                    return node
            return None

        def __eq__(self, other):
            if self.point==other.point:
                return True
            return False
        def __str__(self):
            return str(self.point.x)+" "+str(self.point.y)

    def __init__(self,board_dict,pieceset,blockset,red_final_position):
        # 寻路地图
        self.board_dict =board_dict
        self.movelist=[Point(1,0),Point(1,-1),Point(0,-1),Point(-1,0),Point(-1,1),Point(0,1)]
        self.pieceset=pieceset
        self.blockset=[]

        self.final_possition=[]

        self.nodes=[]
        self.flag = False
        self.moves=[]
        #createnodes
        for piece in self.pieceset:
            node=Astar.Node(Point(piece[0],piece[1]))
            self.nodes.append(node)
        for position in red_final_position:
            final=Astar.Node(Point(position[0],position[1]))
            self.final_possition.append(final)
        for blocks in blockset:
            node=Astar.Node(Point(blocks[0],blocks[1]))
            self.blockset.append(node)
        for blocks in self.blockset:
            if self.final_possition.__contains__(blocks):
                self.final_possition.remove(blocks)

    def endPointInCloseList(self):
        for node in self.nodes:
            for position in self.final_possition:
                if node == position:
                    self.nodes.remove(node)
                    return True
        return False
    def getNode(self):
        currentNode = self.nodes[n]
        return currentNode

    def recalculateNodes(self,node):
        list=[]
        for open in node.openlist:
            node_cost=0
            for goal in self.final_possition:
                open_z=open.point.x+open.point.y
                goal_z=goal.point.x+goal.point.y
                cost=+max(abs(open.point.x-goal.point.x),abs(open.point.y-goal.point.y),abs(open_z-goal_z))
                node_cost+=cost
            list.append(node_cost)
        return list
    def calulateStayNodeCost(self,node):
        othertotalCost=0
        for other in self.nodes:
            if other is not node:
                for goal in self.final_possition:
                    other_z=other.point.x+other.point.y
                    goal_z=goal.point.x+goal.point.y
                    cost=+max(abs(other.point.x-goal.point.x),abs(other.point.y-goal.point.y),abs(other_z-goal_z))
                    othertotalCost+=cost
        return othertotalCost


    """REDO"""
    def searchNear(self,node,move):
        new_node_X=node.point.x+move.x
        new_node_Y=node.point.y+move.y
        new_node=Astar.Node(Point(new_node_X,new_node_Y))

        if  new_node_X not in ran or new_node_Y not in ran :
            return
        currentPoint = Point(new_node_X, new_node_Y)
        if self.nodes.__contains__(new_node) or self.blockset.__contains__(new_node) :
            if not self.nodes.__contains__(Astar.Node(Point(new_node_X+move.x,\
            new_node_Y+move.y))) and \
            not self.blockset.__contains__(Astar.Node(Point(new_node_X+move.x,\
            new_node_Y+move.y))) :
                currentPoint = Point(new_node_X+move.x,new_node_Y+move.y)
                currentPoint.flag = True
            else :
                return
        if node.pointInCloseList(currentPoint):
            return
        opennode = node.pointInOpenList(currentPoint)
        if not opennode:
            opennode = Astar.Node(currentPoint)
            opennode.father = node
            node.openlist.append(opennode)

        return

    def bestmoveofpiece(self):

      for node in self.nodes:
          for move in self.movelist:
              self.searchNear(node,move)
          list=self.recalculateNodes(node)
          node.nextMove=node.openlist[list.index(min(list))]
      return

    def bestmoveofboard(self):
         minimun_cost=sys.maxsize
         for node in self.nodes:
             node_cost=0
             for goal in self.final_possition:
                 new_node_z=node.nextMove.point.x+node.nextMove.point.y
                 goal_z=goal.point.x+goal.point.y
                 cost=+max(abs(node.nextMove.point.x-goal.point.x),abs(node.nextMove.point.y-goal.point.y),abs(new_node_z-goal_z))
                 node_cost+=cost+self.calulateStayNodeCost(node)
             if node_cost<minimun_cost:
                 minimun_cost=node_cost
                 minimun_cost_node=node


         if self.nodes:

             self.nodes.remove(minimun_cost_node)
             self.nodes.append(minimun_cost_node.nextMove)
             num = minimun_cost_node.point
             x1 = num.x
             y1 = num.y
             tup1 = (x1,y1)
             num2 = minimun_cost_node.nextMove.point
             x2 = num2.x
             y2 = num2.y
             tup2 = (x2,y2)
             if not minimun_cost_node.nextMove.point.flag:
                 print("MOVE from "+str(tup1)+" to "+str(tup2)+'.')
             elif minimun_cost_node.nextMove.point.flag:
                 print("JUMP from "+str(tup1)+" to "+str(tup2)+'.')
             if minimun_cost_node.nextMove in self.final_possition:
                 print("EXIT from " + str(tup2)+'.')
         return
    def start(self):

            while len(self.nodes)>0:
                    while self.endPointInCloseList() is False:
                        self.bestmoveofpiece()
                        self.bestmoveofboard()

            return
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

def start():
    red_final_position=[(3,-3),(3,-2),(3,-1),(3,0)]
    print_board(board_dict,"hi",True)
    aStar=Astar(board_dict,pieceset,blockset,red_final_position)
    shortest_path=aStar.start()
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
                    pieceset.append(tuple(piece))
            elif pieces == "blocks":
                for piece in data[pieces]:
                    board_dict[tuple(piece)]="blocks"
                    blockset.append(tuple(piece))
    # TODO: Search for and output winning sequence of moves
    # ...:
        #aster=Astar(map,chess(pieceset[0]),chess((-3,-2))
        start()
