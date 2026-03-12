import copy
TLR,TRR,BLR,BRR=True,True,True,True #Top left rook, top right rook etc. This is for allowing castle
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
    s2=ally_pieces(not white)#this returns enemy pieces as a string
    if not white:
        first,set1,set2=6,-2,-1
    
    #this tells if first move is a double
    if first==x1 and y2==y1 and set2*(x2-x1)==2 and board[x2][y2]==" " and board[x1+set1][y2]==" " and board[x1+set1//2][y2]==" ":
        board[x1][y1],board[x2][y2]=board[x2][y2],board[x1][y1]
        return
    #this tells if the move is a single
    elif y2==y1 and set2*(x2-x1)==1 and -1<x2<8 and board[x2][y2]==" ":
        board[x1][y1],board[x2][y2]=board[x2][y2],board[x1][y1]
        return
    #this lets pawn to cpature
    elif (y2==y1-1 or y2==y1+1) and set2*(x2-x1)==1 and -1<x2<8 and board[x2][y2] in s2:
        board[x1][y1],board[x2][y2]=" ",board[x1][y1]
        return
def horse_move(board,x1,y1,x2,y2,white):
    s1=ally_pieces(white)
    #this makes horse able to make a move as well as capture
    if [abs(y2-y1),abs(x2-x1)] in [[1,2],[2,1]] and board[x2][y2] not in s1:
        board[x1][y1],board[x2][y2]=" ",board[x1][y1]
        return
def castle(board,x1,y1,x2,y2,white):
    global TLR ,TRR,BLR,BRR
    s1=ally_pieces(white)
    # this allows castle if no piece between rook and king and if no attacking piece is attacking any square
    if not white:
        if x1==7 and y1==4 and x2==7 and y2==6 and BLR and BRR and board[7][5]==" " and board[7][6]==" ":
            temp=copy.deepcopy(board)
            temp[7][4],temp[7][5],temp[7][6],temp[7][7]=" "," "," "," "
            if not act_check(temp,white,7,4) and not act_check(temp,white,7,5) and not act_check(temp,white,7,6):
                board[7][4],board[7][5],board[7][6],board[7][7]=" "," "," "," "
                board[7][6],board[7][5]= "♚","♜"
                BLR,BRR=False,False
                return
        elif x1==7 and y1==4 and x2==7 and y2==2 and TLR and TRR and board[7][3]==" " and board[7][2]==" " and board[7][1]==" ":
            temp=copy.deepcopy(board)
            temp[7][4],temp[7][3],temp[7][2],temp[7][1]=" "," "," "," "
            if not act_check(temp,white,7,4) and not act_check(temp,white,7,3) and not act_check(temp,white,7,2):
                board[7][4],board[7][3],board[7][2],board[7][0]=" "," "," "," "
                board[7][2],board[7][3]= "♚","♜"
                TLR,TRR=False,False
                return
    else:
        if x1==0 and y1==4 and x2==0 and y2==6 and BLR and BRR and board[0][5]==" " and board[0][6]==" ":
            temp=copy.deepcopy(board)
            temp[0][4],temp[0][5],temp[0][6],temp[0][7]=" "," "," "," "
            if not act_check(temp,white,0,4) and not act_check(temp,white,0,5) and not act_check(temp,white,0,6):
                board[0][4],board[0][5],board[0][6],board[0][7]=" "," "," "," "
                board[0][6],board[0][5]= "♔","♖"
                BLR,BRR=False,False
                return
        elif x1==0 and y1==4 and x2==0 and y2==2 and BLR and TLR and board[0][3]==" " and board[0][2]==" " and board[0][1]==" ":
            temp=copy.deepcopy(board)
            temp[0][4],temp[0][3],temp[0][2],temp[0][1]=" "," "," "," "
            if not act_check(temp,white,0,4) and not act_check(temp,white,0,3) and not act_check(temp,white,0,2):
                board[0][4],board[0][3],board[0][2],board[0][0]=" "," "," "," "
                board[0][2],board[0][3]= "♔","♖"
                BLR,TLR=False,False
                return
def rook_move(board,x1,y1,x2,y2,white):
    s1=ally_pieces(white)
    prex=x1
    prey=y1
    #this if checks whether final position is allied or not
    if board[x2][y2] in s1:
        return 
    #this moves the piece one place at a time
    while abs(y2-prey) or abs(x2-prex):
        if y2==prey:
            prex+=abs(x2-prex)//(x2-prex)
        elif x2==prex:
            prey+=abs(y2-prey)//(y2-prey)
        if (prey==y2 and prex==x2):
            break
        if board[prex][prey] !=" ":
            return
    board[x1][y1],board[x2][y2]=" ",board[x1][y1]
def bishop_move(board,x1,y1,x2,y2,white):
    prex=x1
    prey=y1
    s1=ally_pieces(white)
    #this if checks whether final position is allied or not
    if board[x2][y2] in s1 or abs(y2-y1)!=abs(x2-x1):
        return
    #this moves the piece one place at a time
    while abs(y2-prey) or abs(x2-prex):
        prex+=abs(x2-prex)//(x2-prex)
        prey+=abs(y2-prey)//(y2-prey)
        if (prey==y2 and prex==x2):
            break
        if board[prex][prey] !=" ":
            return
    board[x1][y1],board[x2][y2]=" ",board[x1][y1]
def queen_move(board,x1,y1,x2,y2,white):
    #queen is just a rook and bishop combined so we can just call those functions
    if x2==x1 or y1==y2:
        rook_move(board,x1,y1,x2,y2,white)
        return
    elif abs(x2-x1)==abs(y2-y1):
        bishop_move(board,x1,y1,x2,y2,white)
        return
def king_move(board,x1,y1,x2,y2,white):
    s1=ally_pieces(white)
    #moves the king around
    if [abs(x2-x1),abs(y2-y1)] in [[1,0],[1,1],[0,1]] and board[x2][y2] not in s1:
        board[x1][y1],board[x2][y2]=" ",board[x1][y1]
        if white:
            global TLR,TRR
            TLR,TRR=False,False
        else:
            global BLR,BRR
            BLR,BRR=False,False
        return
    if x1==x2 and abs(y2-y1)==2:
        castle(board,x1,y1,x2,y2,white)
def find_king(board):
    #return position of both kings
    ans=[[],[]]
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] in "♔♚":
                if board[i][j]=="♔":
                    ans[0]= [i,j]
                elif board[i][j]=="♚":
                    ans[1]=[i,j]
    return ans
def act_check(board,white,x,y):
    for i in range(8):
        for j in range(8):
            if board[i][j] in ally_pieces(not white):
                temp = copy.deepcopy(board)
                moves_list[(pieces_list.index(board[i][j]))//2](temp,i,j,x,y,not white)
                if temp[x][y]!=board[x][y]:
                    return True
    return False
def check(board):
    ans=False
    #tells if there is a check and who is under check
    kings = find_king(board)
    for x,y in kings:
        white=False
        if board[x][y] in ally_pieces(True):
            white=True
        ans=ans or act_check(board,white,x,y)
    return ans

White_turn=True
board=[["♖","♘","♗","♕","♔","♗","♘","♖"],["♙","♙","♙","♙","♙","♙","♙","♙"],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],["♟","♟","♟","♟","♟","♟","♟","♟"],["♜","♞","♝","♛","♚","♝","♞","♜"]]
pieces_list=["♟","♙","♞","♘","♜","♖","♝","♗","♛","♕","♚","♔"]
moves_list=[pawn_move,horse_move,rook_move,bishop_move,queen_move,king_move]
while True:
    print_board(board)
    if White_turn:
        print("------------------------------------------------------------------------------------------------")
        print("White's turn")
        print("------------------------------------------------------------------------------------------------")
    else:
        print("------------------------------------------------------------------------------------------------")
        print("Black's turn")
        print("------------------------------------------------------------------------------------------------")
    x1=int(input("Type row from"))
    y1=int(input("Type coloumn from"))
    x2=int(input("Type row to"))
    y2=int(input("Type coloumn to"))
    secondary_board=copy.deepcopy(board)
    if board[x1][y1] in pieces_list:
        white=False
        if pieces_list.index(board[x1][y1])%2:
            white=True
        moves_list[(pieces_list.index(board[x1][y1]))//2](board,x1,y1,x2,y2,white)
        check(board)
        if check(board):
            print("Check")
        if board!=secondary_board:
            White_turn= not White_turn
    else:
        print("Not found")