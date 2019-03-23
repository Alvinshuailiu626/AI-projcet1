"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import sys
import json
import time

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)

class Astar:
    class Node:
        def __init__(self, point, endPoint, g=0):
            self.point=point
            self.father = None
            self.g = g
            self.h = (abs(endPoint.x - point.x) + abs(endPoint.y - point.y))

    def __init__(self,board_dict,startPoint, endPoint):
        # 开启表
        self.openList = []
        # 关闭表
        self.closeList = []
        # 寻路地图
        self.board_dict =board_dict
        # 起点终点
        if isinstance(startPoint,Point) and isinstance(endPoint,Point):
            self.startPoint = startPoint
            self.endPoint = endPoint
        else:
            self.startPoint = Point(*startPoint)
            self.endPoint = Point(*endPoint)
    def getNode(self):
        """
        获得openlist中F值最小的节点
        :return: Node
        """
        currentNode = self.openList[0]
        return currentNode

    def pointInCloseList(self, point):
        for node in self.closeList:
            if node.point == point:
                return True
        return False
    def pointInOpenList(self, point):
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def endPointInCloseList(self):
        for node in self.openList:
            if node.point == self.endPoint:
                return node
        return None
    def searchNear(self, minF, offsetX, offsetY):
        new_minF_X=minF.point.x+offsetX
        new_minF_Y=minF.point.y+offsetY
        if new_minF_Y and new_minF_Y not in ran :
            return
        currentPoint = Point(new_minF_X, new_minF_Y)
        if board_dict.__contains__((new_minF_X,new_minF_Y))  and board_dict.get((new_minF_X,new_minF_Y)) is 'blocks':

            if board_dict.__contains__((new_minF_X+offsetX,new_minF_Y+offsetY)):
                return
            else :
                currentPoint = Point(new_minF_X+offsetX,new_minF_Y+offsetY)


        if self.pointInCloseList(currentPoint):
            return
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = Astar.Node(currentPoint, self.endPoint, g=minF.g + 1)
            currentNode.father = minF
            self.openList.append(currentNode)
            return

        if minF.g + 1 < currentNode.g:  # 如果更小，就重新计算g值，并且改变father
            currentNode.g = minF.g + 1
            currentNode.father = minF
    def start(self):
        if self.board_dict.get((self.endPoint.x,self.endPoint.y)) == 'blocks':
            return
        #if self.endPoint.x and self.endPoint.y not in ran :
            #return
        startNode = Astar.Node(self.startPoint, self.endPoint)
        self.openList.append(startNode)
        while True:
            # 找到F值最小的点
            minF = self.getNode()
            # 把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)

            self.searchNear(minF, 0, -1)
            self.searchNear(minF, 1, -1)
            self.searchNear(minF, 1, 0)
            self.searchNear(minF, 0, 1)
            self.searchNear(minF, -1, 1)
            self.searchNear(minF, -1, 0)
            point = self.endPointInCloseList()
            if point:  # 如果终点在关闭表中，就返回结果
                # print("关闭表中")
                cPoint = point
                pathList = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint = cPoint.father
                    else:
                        # print(pathList)
                        # print(list(reversed(pathList)))
                        # print(pathList.reverse())
                        return list(reversed(pathList))
            if len(self.openList) == 0:
                return None
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
    for piece in pieceset:
        startpoint=Point(piece[0],piece[1])
        aStar=Astar(board_dict,startpoint,Point(red_final_position[1][0],red_final_position[1][1]))
        shortest_path=aStar.start()
        for final_possition in red_final_position[1:]:
            aStar=Astar(board_dict,startpoint,Point(final_possition[0],final_possition[1]))
            pathlist=aStar.start()
            if pathlist is not None and len(pathlist)<len(shortest_path):
                shortest_path=pathlist
        for a in shortest_path:
            print(a)

# when this module is executed, run the `main` function:
if __name__ == '__main__':

    start_time = time.time()
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
    end = time.time()
    running_time = end-start_time
    print(running_time)
