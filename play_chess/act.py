import copy
from .schema import MoveResponse
class Game:
    
    def __init__(self):
        self.board = [["♖","♘","♗","♕","♔","♗","♘","♖"],["♙","♙","♙","♙","♙","♙","♙","♙"],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],["♟","♟","♟","♟","♟","♟","♟","♟"],["♜","♞","♝","♛","♚","♝","♞","♜"]]
        self.white_turn = True
        self.White_queen_rook = True
        self.White_king_rook = True
        self.Black_queen_rook = True
        self.Black_king_rook = True
        self.undo_stack=[]
        self.pieces_list=["♟","♙","♞","♘","♜","♖","♝","♗","♛","♕","♚","♔"]
        self.moves_list=[self.pawn_move,self.horse_move,self.rook_move,self.bishop_move,self.queen_move,self.king_move]
    def move(self, x1, y1, x2, y2):
        response = MoveResponse(success=False,board=self.board,white_move=self.white_turn,check=False,checkmate=False,stalemate=False,state=0,)
        board = self.board
        secondary_state = [self.white_turn,self.White_queen_rook,self.White_king_rook,self.Black_queen_rook,self.Black_king_rook,]
        secondary_board = copy.deepcopy(board)
        previous_response = MoveResponse(success=False,board=secondary_board,white_move=self.white_turn,check=False,checkmate=False,stalemate=False,state=0,)
        if not (0<=x1<8 and 0<=y1<8 and 0<=x2<8 and 0<=y2<8):
            return previous_response
        if board[x1][y1] not in self.pieces_list:
            return previous_response
        white = self.pieces_list.index(board[x1][y1]) % 2 == 1
        if white != self.white_turn:
            return previous_response
        self.moves_list[(self.pieces_list.index(board[x1][y1])) // 2](board, x1, y1, x2, y2, white)
        if board != secondary_board:
            if self.king_in_check(self.board, white):
                self.board=secondary_board
                (self.white_turn,self.White_queen_rook,self.White_king_rook,self.Black_queen_rook,self.Black_king_rook,)=secondary_state
                return previous_response
            else:
                self.promote()
                response.success=True
                self.white_turn = not self.white_turn 
                self.check(response)
                response.white_move = not response.white_move
                if response.check:
                    self.checkmate(response)
                    if response.checkmate:
                        response.state=2
                else:
                    if response.stalemate:
                        response.state=1
                response.board=self.board 
                return response
        return previous_response
    def ally_pieces(self,white):
        return "♔♕♗♘♙♖" if white else "♚♛♞♝♟♜"
    def print_board(self):
        for i in range(0,8):
            print(f"\t{i}\t",end='')
        print("")
        temp=0
        for i in self.board:
            print("---------------------------------------------------------------------------------------------------------------------------------")
            for j in i:
                print(f"|\t{j}\t",end='')
            print(f"|{temp}")
            temp+=1
        print("---------------------------------------------------------------------------------------------------------------------------------")
    def finder(self,board,x,y,white):
        s1=self.ally_pieces(white)
        if board[x][y] in s1:
            return board[x][y],True
        return " ",False
    def promote(self):
        for i in range(8):
            if self.board[0][i] == "♟":
                self.board[0][i] = "♛"
            elif self.board[7][i] == "♙":
                self.board[7][i] = "♕"
    def pawn_move(self,board,x1,y1,x2,y2,white):
        first,set1,set2=1,2,1#first represent initial index as at that index pawn can move 2 squares set2 is thaat pawn might move 2 steps at beggining set1 is just a variable that makes white follow downward while black pawn follows upward path
        s1=self.ally_pieces(white)
        s2=self.ally_pieces(not white)#this returns enemy pieces as a string
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
    def horse_move(self,board,x1,y1,x2,y2,white):
        s1=self.ally_pieces(white)
        #this makes horse able to make a move as well as capture
        if [abs(y2-y1),abs(x2-x1)] in [[1,2],[2,1]] and board[x2][y2] not in s1:
            board[x1][y1],board[x2][y2]=" ",board[x1][y1]
            return
    def castle(self,board,x1,y1,x2,y2,white):
        # this allows castle if no piece between rook and king and if no attacking piece is attacking any square
        if not white:
            if x1==7 and y1==4 and x2==7 and y2==6 and self.Black_queen_rook and self.Black_king_rook and board[7][5]==" " and board[7][6]==" ":
                temp=copy.deepcopy(board)
                temp[7][4],temp[7][5],temp[7][6],temp[7][7]=" "," "," "," "
                if not self.act_check(temp,white,7,4) and not self.act_check(temp,white,7,5) and not self.act_check(temp,white,7,6):
                    board[7][4],board[7][5],board[7][6],board[7][7]=" "," "," "," "
                    board[7][6],board[7][5]= "♚","♜"
                    self.Black_queen_rook,self.Black_king_rook=False,False
                    return
            elif x1==7 and y1==4 and x2==7 and y2==2 and self.White_queen_rook and self.White_king_rook and board[7][3]==" " and board[7][2]==" " and board[7][1]==" ":
                temp=copy.deepcopy(board)
                temp[7][4],temp[7][3],temp[7][2],temp[7][1]=" "," "," "," "
                if not self.act_check(temp,white,7,4) and not self.act_check(temp,white,7,3) and not self.act_check(temp,white,7,2):
                    board[7][4],board[7][3],board[7][2],board[7][0]=" "," "," "," "
                    board[7][2],board[7][3]= "♚","♜"
                    self.White_queen_rook,self.White_king_rook=False,False
                    return
        else:
            if x1==0 and y1==4 and x2==0 and y2==6 and self.Black_queen_rook and self.Black_king_rook and board[0][5]==" " and board[0][6]==" ":
                temp=copy.deepcopy(board)
                temp[0][4],temp[0][5],temp[0][6],temp[0][7]=" "," "," "," "
                if not self.act_check(temp,white,0,4) and not self.act_check(temp,white,0,5) and not self.act_check(temp,white,0,6):
                    board[0][4],board[0][5],board[0][6],board[0][7]=" "," "," "," "
                    board[0][6],board[0][5]= "♔","♖"
                    self.Black_queen_rook,self.Black_king_rook=False,False
                    return
            elif x1==0 and y1==4 and x2==0 and y2==2 and self.Black_queen_rook and self.White_queen_rook and board[0][3]==" " and board[0][2]==" " and board[0][1]==" ":
                temp=copy.deepcopy(board)
                temp[0][4],temp[0][3],temp[0][2],temp[0][1]=" "," "," "," "
                if not self.act_check(temp,white,0,4) and not self.act_check(temp,white,0,3) and not self.act_check(temp,white,0,2):
                    board[0][4],board[0][3],board[0][2],board[0][0]=" "," "," "," "
                    board[0][2],board[0][3]= "♔","♖"
                    self.Black_queen_rook,self.White_queen_rook=False,False
                    return
    def rook_move(self,board,x1,y1,x2,y2,white):
        s1=self.ally_pieces(white)
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
        if x1==0 and y1==0:
            self.White_queen_rook=False
        elif x1==0 and y1==7:
            self.White_king_rook=False
        elif x1==7 and y1==0:
            self.Black_queen_rook=False
        elif x1==7 and y1==7:
            self.Black_king_rook=False
        board[x1][y1],board[x2][y2]=" ",board[x1][y1]
    def bishop_move(self,board,x1,y1,x2,y2,white):
        prex=x1
        prey=y1
        s1=self.ally_pieces(white)
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
    def queen_move(self,board,x1,y1,x2,y2,white):
    #queen is just a rook and bishop combined so we can just call those functions
        if x2==x1 or y1==y2:
            self.rook_move(board,x1,y1,x2,y2,white)
            return
        elif abs(x2-x1)==abs(y2-y1):
            self.bishop_move(board,x1,y1,x2,y2,white)
            return
    def king_move(self,board,x1,y1,x2,y2,white):
        s1=self.ally_pieces(white)
        #moves the king around
        if [abs(x2-x1),abs(y2-y1)] in [[1,0],[1,1],[0,1]] and board[x2][y2] not in s1:
            board[x1][y1],board[x2][y2]=" ",board[x1][y1]
            if white:
                self.White_queen_rook,self.White_king_rook=False,False
            else:
                self.Black_queen_rook,self.Black_king_rook=False,False
            return
        if x1==x2 and abs(y2-y1)==2:
            self.castle(board,x1,y1,x2,y2,white)
    def find_king(self,board):
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
    def find_attackers(self, board, white, x, y):
        attackers = []
        for i in range(8):
            for j in range(8):
                if board[i][j] in self.ally_pieces(not white):
                    temp = copy.deepcopy(board)
                    self.moves_list[self.pieces_list.index(board[i][j])//2](temp,i,j,x,y,not white)
                    if temp[x][y]!=board[x][y]:
                        attackers.append((i, j))
        return attackers
    def act_check(self, board, white, x, y):
        return bool(len(self.find_attackers(board, white, x, y))>0)
    def check(self, response):
        response.check = self.king_in_check(self.board, self.white_turn)
    def king_in_check(self, board, white):
        kings = self.find_king(board)
        x, y = kings[0] if white else kings[1]
        return self.act_check(board, white, x, y)
    def save_state(self):
        return (copy.deepcopy(self.board),self.white_turn,self.White_queen_rook,self.White_king_rook,self.Black_queen_rook,self.Black_king_rook,)
    def restore_state(self, state):
        (self.board,self.white_turn,self.White_queen_rook,self.White_king_rook,self.Black_queen_rook,self.Black_king_rook,)=state
    def checkmate(self, response):
        check_board=copy.deepcopy(self.board)
        # 1. Can the king escape?
        if self.king_can_escape(check_board):
            return
        print(check_board)
        # 2. Find all checking pieces
        kings = self.find_king(check_board)
        x, y = kings[0] if self.white_turn else kings[1]
        attackers = self.find_attackers(check_board, self.white_turn, x, y)
        print(check_board)
        # 3. Double check
        if len(attackers) > 1:
            response.checkmate = True
            return
        
        ax, ay = attackers[0]
        # 4. Can attacker be captured?
        if self.can_any_piece_reach_square(check_board, ax, ay):
            return
        print(check_board)
        piece = check_board[ax][ay]
        # 5. Knight/Pawn can't be blocked
        if piece in "♞♘♟♙":
            response.checkmate = True
            return
        print(check_board)
        # 6. Can attack be blocked?
        if self.can_block_attack(check_board, ax, ay):
            return
        print(check_board)
        response.checkmate = True
    def king_can_escape(self,check_board):
        white = self.white_turn
        kings = self.find_king(check_board)
        x, y = kings[0] if white else kings[1]
        state = self.save_state()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx = x + dx
                ny = y + dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    continue
                self.king_move(check_board, x, y, nx, ny, white)
                # Illegal king move
                if check_board == state[0]:
                    continue
                # Escaped check
                if not self.king_in_check(check_board, white):
                    self.restore_state(state)
                    check_board=copy.deepcopy(state[0])
                    return True
                check_board=copy.deepcopy(state[0])
        self.restore_state(state)
        return False
    def find_allies(self, board, white):
        allies = []
        for i in range(8):
            for j in range(8):
                if board[i][j] in self.ally_pieces(white):
                    allies.append((i, j))
        return allies
    def can_any_piece_reach_square(self, check_board, ax, ay):
        white = self.white_turn
        allies = self.find_allies(check_board, white)
        state = self.save_state()
        for x, y in allies:
            self.restore_state(state)
            check_board = copy.deepcopy(state[0])
            self.moves_list[(self.pieces_list.index(check_board[x][y]))//2](check_board,x,y,ax,ay,white)
            if check_board == state[0]:
                continue
            if not self.king_in_check(check_board, white):
                self.restore_state(state)
                check_board=copy.deepcopy(state[0])
                return True
            check_board=copy.deepcopy(state[0])
        self.restore_state(state)
        return False
    def can_block_attack(self,check_board,  ax, ay):
        white = self.white_turn
        kings = self.find_king(check_board)
        kx, ky = kings[0] if white else kings[1]
        dx = 0 if ax == kx else (kx - ax) // abs(kx - ax)
        dy = 0 if ay == ky else (ky - ay) // abs(ky - ay)
        x = ax + dx
        y = ay + dy
        while (x, y) != (kx, ky):
            if self.can_any_piece_reach_square(check_board, x, y):
                return True
            x += dx
            y += dy
        return False