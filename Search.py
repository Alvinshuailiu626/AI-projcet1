"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import sys
import json


class Chess:
    def __init__(self,x,y):
        self.x=x
        self.y=y


    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)
class Search:
    class Node:
        def __init__(self,point, endPoint, g=0):
            self.point = point #
            self.father = None
            self.g = g #g will recalculate when we need them
            self.h = 0
            #max(abs(endPoint.x-point.x),abs(endPoint.y-point.y))*10

    def __init__(self,map,startPoint, endPoint, passTag=0):
        # 开启表
        self.openList = []
        # 关闭表
        self.closeList = []
        # 寻路地图
        self.map =map
        # 起点终点
        self.allWay = []
        self.startPoint = startPoint
        self.endPoint = endPoint
        # 可行走标记
        self.passTag = passTag


    def getMinNode(self):
        """
        get the least f value node from openlist
        :return: Node
        """
        currentNode = self.openList[0]
        for node in self.openList:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
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
        for node in self.closeList:
            if node.point==self.endPoint:
                return node
        return None

    def searchNear(self, minF, offsetX, offsetY):
        """
        搜索节点周围的点
        :param minF:F值最小的节点
        :param offsetX:坐标偏移量
        :param offsetY:
        :return:
        """
        # 越界检测

        vX = minF.point.x + offsetX
        vY = minF.point.y + offsetY
        if abs(vY) > 3 or abs(vX) > 3 or abs(vX+vY) > 3:
            return


        # 如果是障碍，就忽略或者跳
        if self.map[(vX,vY)] == (7 or 1):
            #return
            if abs(vY+offsetY) > 3 or abs(vX+offsetX) > 3 \
            or abs(vY+vX+offsetX+offsetY) > 3:
                return
            elif self.map[(vX+offsetX,vY+offsetY)] == 0:
                currentPoint = Chess(vX+offsetX,vY+offsetY)
            else:
                return
        else:
            currentPoint = Chess(vX,vY)

        # 如果在关闭表中，就忽略
        if self.pointInCloseList(currentPoint):
            return
        # 设置单位花费，暂时不跳
        step = 10
        # 如果不再openList中，就把它加入openlist
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = Search.Node(currentPoint, self.endPoint, g=minF.g + step)
            currentNode.father = minF
            self.openList.append(currentNode)
            return
        # 如果在openList中，判断minF到当前点的G是否更小
        if minF.g + step < currentNode.g:  # 如果更小，就重新计算g值，并且改变father
            currentNode.g = minF.g + step
            currentNode.father = minF



    def multiTask(self):
        if isinstance(self.startPoint, Chess) and \
        isinstance(self.endPoint, Chess):
            self.start()
        else:
            temperary = []
            endP = []
            compareL = []
            for node in self.startPoint:
                temperary.append(node)
            for nod in self.endPoint:
                if map[(nod.x,nod.y)]!=7:
                    endP.append(nod)
            for element in temperary:
                self.openList.clear()
                self.closeList.clear()
                self.startPoint = element
                for item in endP:
                    self.endPoint = item
                    compareL.append(self.start())
                shorterL = compareL[0]
                for item in compareL:
                    if len(shorterL) > len(item):
                        shorterL = item
                compareL = []
                self.allWay.append(shorterL)
                for node in shorterL:
                    print(node)
                print("line----------")
        return self.allWay


    def start(self):
        """
        开始寻路
        :return: None或Point列表（路径）
        """
        # 判断寻路终点是否是障碍
        #if self.map2d[self.endPoint.x][self.endPoint.y] != self.passTag:
            #return None

        # 1.将起点放入开启列表
        startNode = Search.Node(self.startPoint, self.endPoint)
        self.openList.append(startNode)
        # 2.主循环逻辑
        while True:
                    # 找到F值最小的点
            minF = self.getMinNode()
                    # 把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)
                    # 判断这个节点的上下左右节点
            self.searchNear(minF, 0, -1)
            self.searchNear(minF,1,-1)
            self.searchNear(minF, 1, 0)
            self.searchNear(minF, 0, 1)
            self.searchNear(minF,-1,1)
            self.searchNear(minF, -1, 0)

                    # 判断是否终止
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
                        #print(pathList)
                        #print(list(reversed(pathList)))
                        #print(pathList.reverse())
                        pathList.append(cPoint.point)
                        self.map[(self.startPoint.x,self.startPoint.y)]=0
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


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        data = json.load(file)
        board_dict={}
        blockset=[]
        pieceset=[]
        red_final_position=[(3,-3),(3,-2),(3,-1),(3,0)]
        final_postion = []
        ran = range(-3, +3+1)
        map={}#创建dic方便查询flag
        for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
            map[qr]=0
        for pieces in data.keys():
            if pieces == "pieces":
                for piece in data[pieces]:
                    board_dict[tuple(piece)]=data['colour']
                    pieceset.append(Chess(piece[0],piece[1]))
                    map[tuple(piece)] = 1
            elif pieces == "blocks":
                for piece in data[pieces]:
                    board_dict[tuple(piece)]="blocks"
                    blockset.append(tuple(piece))
                    map[tuple(piece)] = 7

    # TODO: Search for and output winning sequence of moves
    # ...:
    #only for test
    for item in red_final_position:
        x = item[0]
        y = item[1]
        final_postion.append(Chess(x,y))
    aStar=Search(map,pieceset,final_postion)
    pathList=aStar.multiTask()
    if pathList:
        for list in pathList:
            for point in list:
                map[(point.x,point.y)]=9
    print_board(board_dict,"ss",True)
    print(map)
