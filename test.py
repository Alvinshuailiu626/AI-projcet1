import sys
import json

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        board_dict={}
        for pieces in data.keys():
            if pieces =="pieces":
                for piece in data[pieces]:
                     board_dict[tuple(piece)]=data['colour']
            elif pieces == "blocks":
                for piece in data[pieces]:
                    board_dict[tuple(piece)]="blocks"
        print(board_dict)
#        for onepiece in pieces:
#            board_dict[tuple(onepiece)]=colour
#        for block in blocks:
#            board_dict[tuple(block)]="blocks"
# TODO: Search for and output winning sequence of moves
# ...

#    print (board_dict)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
