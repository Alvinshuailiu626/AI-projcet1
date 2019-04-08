"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching
Authors:
"""

import sys
import json
import copy

class Piece:
    def __init__(self,x,y,colour,endpoint=None):
        self.x=x
        self.y=y
        self.colour=colour
        self.endpoint=endpoint

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+ ")"

class Node:

    def __init__(self,pieceset,blockset,final_position,g=0,lastmove=None,father=None):
        # 寻路地图
        self.printList = []
        self.pieceset=pieceset
        self.blockset=blockset
        self.g=g
        self.h=0
        self.final_position=final_position
        self.nextnodes=[]
        self.lastmove=lastmove
        self.father=father
        self.flag = False
        self.exit = False
        #createnodes
    def piecereachedEnd(self):
        newpieceset=copy.deepcopy(self.pieceset)
        for piece in self.pieceset:
            for endposition in self.final_position:
                if piece.x == endposition[0] and piece.y==endposition[1]:
                    newpieceset.remove(piece)
                    self.exit = True
        self.pieceset=newpieceset
        return
    def Legal_move(self,piece,move):
        new_piece=Piece(piece.x+move[0],piece.y+move[1],piece.colour)
        if  abs(piece.x+move[0]+piece.y+move[1])>3 or piece.x+move[0] not in ran or piece.y+move[1] not in ran:
            return None
        if self.pieceinBlockset(new_piece) or self.pieceinPieceset(new_piece) :
            new_piece=Piece(piece.x+move[0]+move[0],piece.y+move[1]+move[1],piece.colour)
            if self.pieceinBlockset(new_piece) or self.pieceinPieceset(new_piece) :
                return None
            self.flag = True
        return new_piece
    def pieceinBlockset(self,new_piece):
        for block in self.blockset:
            if block==new_piece:
                return True
        return False
    def pieceinPieceset(self,new_piece):
        for piece in self.pieceset:
            if piece==new_piece:
                return True
        return False
    def closestEndpoint(self,piece):
        minimun_cost_toEnd=sys.maxsize
        closestEndpoint=self.final_position[0]
        for endposition in self.final_position:
            cost=max(abs(piece.x-endposition[0]),abs(piece.y-endposition[1]),abs((piece.x+piece.y)-(endposition[0]+endposition[1])))*0.8
            if cost<minimun_cost_toEnd:
                minimun_cost_toEnd=cost
                closestEndpoint=endposition
        piece.endpoint=closestEndpoint
        return closestEndpoint

    def getCost(self):
        for piece in self.pieceset:
            self.closestEndpoint(piece)
            self.h+=max(abs(piece.x-piece.endpoint[0]),abs(piece.y-piece.endpoint[1]),abs((piece.x+piece.y)-(piece.endpoint[0]+piece.endpoint[1])))*0.8
        return

    def new_piece_list(self,moved_piece):
        piecelist=[]
        for piece in self.pieceset:
            if piece is not moved_piece:
                piecelist.append(piece)
        return piecelist
    def generate_nextnodes(self):
        for piece in self.pieceset:
            for move in moves:
                if self.Legal_move(piece,move) is not None:
                    list=self.new_piece_list(piece)
                    list.append(self.Legal_move(piece,move))
                    if not self.flag:
                        New_node=Node(list,self.blockset,self.final_position,self.g+1,"MOVE from "+str(piece)+" to " +str(self.Legal_move(piece,move)),self)
                    elif self.flag:
                        New_node=Node(list,self.blockset,self.final_position,self.g+1,"JUMP from "+str(piece)+" to " +str(self.Legal_move(piece,move)),self)
                        self.flag = False
                    openlist.append(New_node)
                    New_node.getCost()
    def getMinnode(self):
        Minnode=openlist[0]
        for node in openlist:
            if node.h+node.g< Minnode.h+Minnode.g:
                Minnode=node
        closelist.append(Minnode)
        self.nodeinclosedlist(node)
        return Minnode
    def nodeinclosedlist(self,node):
        for closednode in closelist:
            for open in openlist:
                if open is closednode:
                    openlist.remove(open)
        return False
    def returnFather(self,node):
        if node.father is not None:
            if node.exit:
                input = node.lastmove.split()
                output = "EXIT "+input[1]+" "+input[4]
                self.printList.append(output+".")

            self.printList.append(node.lastmove+".")
            self.returnFather(node.father)
        return
    def start(self):
        self.piecereachedEnd()
        if len(self.pieceset)<1:
            print(len(openlist))
            self.returnFather(self)
            for item in reversed(self.printList):
                print(item)
        else:
            self.generate_nextnodes()
            node=self.getMinnode()
            node.start()
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
    final_position=[(3,-3),(3,-2),(3,-1),(3,0)]
    print_board(board_dict,"hi",True)
    astar=Node(pieceset,blockset,final_position)
    astar.start()
# when this module is executed, run the `main` function:
if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        data = json.load(file)
        board_dict={}
        blockset=[]
        pieceset=[]
        openlist=[]
        closelist=[]
        moves=[(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)]
        ran = range(-3, +3+1)
        for pieces in data.keys():
            if pieces == "pieces":
                for piece in data[pieces]:
                    board_dict[tuple(piece)]=data['colour']
                    pieceset.append(Piece(piece[0],piece[1],data['colour']))
            elif pieces == "blocks":
                for block in data[pieces]:
                    board_dict[tuple(block)]="blocks"
                    blockset.append(Piece(block[0],block[1],'blocks'))
        start()
