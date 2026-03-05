import copy
def ally_pieces(white):
    return "♔♕♗♘♙♖" if white else "♚♛♞♝♟♜"
def print_board(board):
    for i in range(0,8):
        print(f"\t{i}\t",end='')
    print("")
    temp=0
    for i in board:
        print("---------------------------------------------------------------------------------------------------------------------------------")
        for j in i:
            print(f"|\t{j}\t",end='')
        print(f"|{temp}")
        temp+=1
    print("---------------------------------------------------------------------------------------------------------------------------------")
def finder(board,x,y,white):
    s1=ally_pieces(white)
    if board[x][y] in s1:
        return board[x][y],True
    return " ",False
def pawn_move(board,x1,y1,x2,y2,white):
    first,set1,set2=1,2,1#first represent initial index as at that index pawn can move 2 squares set2 is thaat pawn might move 2 steps at beggining set1 is just a variable that makes white follow downward while black pawn follows upward path
    s1=ally_pieces(white)
    if not white:
        first,set1,set2=6,-2,-1
    if first==x1 and y2==y1 and set2*(x2-x1)==2 and board[x2][y2]==" " and board[x1+set1][y2]==" " and board[x1+set1//2][y2]==" ":
        board[x1][y1],board[x2][y2]=board[x2][y2],board[x1][y1]
        return
    elif y2==y1 and set2*(x2-x1)==1 and -1<x2<8 and board[x2][y2]==" ":
        board[x1][y1],board[x2][y2]=board[x2][y2],board[x1][y1]
        return
def horse_move(board,x1,y1,x2,y2,white):
    s1=ally_pieces(white)
    if [abs(y2-y1),abs(x2-x1)] in [[1,2],[2,1]] and board[x2][y2] not in s1:
        board[x1][y1],board[x2][y2]=" ",board[x1][y1]
        return
def rook_move(board,x1,y1,x2,y2,white):
    s1=ally_pieces(white)
    prex=x1
    prey=y1
    if board[x2][y2] in s1:
        return 
    while abs(y2-prey) or abs(x2-prex):
        if y2==prey:
            prex+=abs(x2-prex)//(x2-prex)
        elif x2==prex:
            prey+=abs(y2-prey)//(y2-prey)
        if board[prex][prey] !=" ":
            return
    board[x1][y1],board[x2][y2]=" ",board[x1][y1]
def bishop_move(board,x1,y1,x2,y2,white):
    prex=x1
    prey=y1
    s1=ally_pieces(white)
    if board[x2][y2] in s1 or abs(y2-y1)!=abs(x2-x1):
        return
    while abs(y2-prey) or abs(x2-prex):
        prex+=abs(x2-prex)//(x2-prex)
        prey+=abs(y2-prey)//(y2-prey)
        if board[prex][prey] !=" ":
            return
    board[x1][y1],board[x2][y2]=" ",board[x1][y1]
def queen_move(board,x1,y1,x2,y2,white):
    if x2==x1 or y1==y2:
        rook_move(board,x1,y1,x2,y2,white)
        return
    elif abs(x2-x1)==abs(y2-y1):
        bishop_move(board,x1,y1,x2,y2,white)
        return
def king_move(board,x1,y1,x2,y2,white):
    s1=ally_pieces(white)
    if [abs(x2-x1),abs(y2-y1)] in [[1,0],[1,1],[0,1]] and board[x2][y2] not in s1:
        board[x1][y1],board[x2][y2]=" ",board[x1][y1]
        return
def find_king(board,white):
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] in "♔♚":
                if board[i][j]=="♔" and white:
                    return i,j
                elif board[i][j]=="♚" and not white:
                    return i,j
def check(board,white):
    x,y = find_king(board,white)
    for i in range(8):
        for j in range(8):
            if board[i][j] in ally_pieces(not white):
                temp = copy.deepcopy(board)
                moves_list[(pieces_list.index(board[i][j]))//2](temp,i,j,x,y,not white)
                if temp[x][y]!=board[x][y]:
                    print("Check")
                    return True
    return False

board=[["♖","♘","♗","♕","♔","♗","♘","♖"],["♙","♙","♙","♙","♙","♙","♙","♙"],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],["♟","♟","♟","♟","♟","♟","♟","♟"],["♜","♞","♝","♛","♚","♝","♞","♜"]]
pieces_list=["♟","♙","♞","♘","♜","♖","♝","♗","♛","♕","♚","♔"]
moves_list=[pawn_move,horse_move,rook_move,bishop_move,queen_move,king_move]
while True:
    print_board(board)
    x1=int(input("Type row from"))
    y1=int(input("Type coloumn from"))
    x2=int(input("Type row to"))
    y2=int(input("Type coloumn to"))
    if board[x1][y1] in pieces_list:
        white=False
        if pieces_list.index(board[x1][y1])%2:
            white=True
        moves_list[(pieces_list.index(board[x1][y1]))//2](board,x1,y1,x2,y2,white)
    else:
        print("Not found")