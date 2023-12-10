from PIL import ImageTk, Image
#types: 110
KING = "__king__", 'K'
QUEEN = "__queen__", 'Q'
BISHOP = "__bishop__", 'B'
KNIGHT = "__knight__", 'H'
ROOK = "__rook__", 'R'
PAWN = "__pawn__", 'P'
pieceImgDict = {'W':{i[0]:ImageTk.PhotoImage(Image.open("pieces/white{}.png".format(str.upper(i[0][2])+i[0][3:-2])).resize((int(_//3.5) for _ in Image.open("pieces/white{}.png".format(str.upper(i[0][2])+i[0][3:-2])).size))) for i in (KING, QUEEN, BISHOP, KNIGHT, ROOK, PAWN)},
                'B':{i[0]:ImageTk.PhotoImage(Image.open("pieces/black{}.png".format(str.upper(i[0][2])+i[0][3:-2])).resize((int(_//3.5) for _ in Image.open("pieces/black{}.png".format(str.upper(i[0][2])+i[0][3:-2])).size))) for i in (KING, QUEEN, BISHOP, KNIGHT, ROOK, PAWN)}}
"""pieceImgDict = {'W':{KING[0]:ImageTk.PhotoImage(Image.open("pieces/whiteKing.png")), QUEEN[0]:ImageTk.PhotoImage(Image.open("pieces/whiteQueen.png")), BISHOP[0]:ImageTk.PhotoImage(Image.open("pieces/whiteBishop.png")), KNIGHT[0]:ImageTk.PhotoImage(Image.open("pieces/whiteKnight.png")), ROOK[0]:ImageTk.PhotoImage(Image.open("pieces/whiteRook.png")), PAWN[0]:ImageTk.PhotoImage(Image.open("pieces/whitePawn.png"))},
                'B':{KING[0]:ImageTk.PhotoImage(Image.open("pieces/blackKing.png")), QUEEN[0]:ImageTk.PhotoImage(Image.open("pieces/blackQueen.png")), BISHOP[0]:ImageTk.PhotoImage(Image.open("pieces/blackBishop.png")), KNIGHT[0]:ImageTk.PhotoImage(Image.open("pieces/blackKnight.png")), ROOK[0]:ImageTk.PhotoImage(Image.open("pieces/blackRook.png")), PAWN[0]:ImageTk.PhotoImage(Image.open("pieces/blackPawn.png"))}}"""

def checkforcheck(king, board, rotate=False):
    piecesChecking = {}
    
    if rotate: board.rotate()
    for i, j in king.findMoves(board, PAWN)[1]:
        i, j = int(i), int(j)
        if board.grid[i][j].type == PAWN:
            if rotate: board.rotate()
            return True
            piecesChecking[board.grid[i][j]] = (i, j)
    for i, j in king.findMoves(board, BISHOP)[1]:
        i, j = int(i), int(j)
        if board.grid[i][j].type in [BISHOP, QUEEN]:
            if rotate: board.rotate()
            return True
            piecesChecking[board.grid[i][j]] = (i, j)
    for i, j in king.findMoves(board, ROOK)[1]:
        i, j = int(i), int(j)
        if board.grid[i][j].type in [ROOK, QUEEN]:
            if rotate: board.rotate()
            return True
            piecesChecking[board.grid[i][j]] = (i, j)
    for i, j in king.findMoves(board, KNIGHT)[1]:
        i, j = int(i), int(j)
        if board.grid[i][j].type == KNIGHT:
            if rotate: board.rotate()
            return True
            piecesChecking[board.grid[i][j]] = (i, j)
    for i, j in king.findMoves(board, KING)[1]:
        i, j = int(i), int(j)
        if board.grid[i][j].type == KING:
            if rotate: board.rotate()
            return True
            piecesChecking[board.grid[i][j]] = (i, j)
    if rotate: board.rotate()
    return piecesChecking

class piece:
    def __init__(self, _type, loc, plyr, game):
        self.game = game
        self.type = _type
        self.loc = loc
        self.plyr = plyr
        self.nvrMoved = True
        self.color = "white" if plyr=='W' else "black"
    def draw(self, cnvs, rotate = False):
        row, clmn =  (7-self.loc[0], 7-self.loc[1]) if rotate else self.loc
        #cnvs.create_text(clmn*100+50, row*100+50, text=self.type[1], font="Times 45", fill=self.color)
        cnvs.create_image(clmn*100+50, row*100+50, image=pieceImgDict[self.plyr][self.type[0]], anchor="center")
    def findMoves(self, board, exception=None):
        if self.plyr=='B' and exception==None:
            board.rotate()
        moves, targets, castles, transpawn = [], [], {}, {}
        if (self.type==KING and exception==None or exception==KING):
            for i in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)):
                move = (int(self.loc[0]+i[0]), int(self.loc[1]+i[1]))
                if not (0 <= move[0] < 8 and 0 <= move[1] < 8): continue
                getSquare = board.grid[int(move[0])][int(move[1])]
                if getSquare!=0:
                    if getSquare.plyr==self.plyr: continue
                    if not(exception==KING):
                        if self.checkMove(self.loc, move, board, {}): continue
                    targets += [move]
                else:
                    if not(exception==KING):
                        if self.checkMove(self.loc, move, board, {}): continue
                    moves += [move]
            if (exception==None and not(checkforcheck(self, board, True)) or exception==KING) and self.nvrMoved:
                dict1 = {board.grid[7][0]:False, board.grid[7][7]:False}
                for _ in [board.grid[7][0], board.grid[7][7]]:
                    if _ == 0 or _.plyr!=self.plyr: continue
                    if _.type == ROOK and _.nvrMoved:
                        dict1[_] = True
                        rookChange = _.loc[1]-self.loc[1]
                        if rookChange==0: continue
                        for i in range(1, 7):
                            this = board.grid[7][int(i)]
                            if this!=0:
                                if (this.loc[1]-self.loc[1])*rookChange > 0:
                                    dict1[_] = False
                                    break
                        dir = rookChange/abs(rookChange)
                        if dict1[_]:
                            if not(exception==KING) and self.checkMove(self.loc, (self.loc[0], self.loc[1]+dir*2), board, {self:[_, (self.loc[0], self.loc[1] + dir)]}): continue
                            moves += [(self.loc[0], self.loc[1]+dir*2)]
                            castles["{}{}".format(self.loc[0], self.loc[1] + dir*2)] = [_, (self.loc[0], self.loc[1] + dir)]


        MoveLst = []
        if (self.type==QUEEN and exception==None or exception==QUEEN): MoveLst = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        if (self.type==BISHOP and exception==None or exception==BISHOP): MoveLst = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        if (self.type==ROOK and exception==None or exception==ROOK): MoveLst = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if MoveLst:
            for i in MoveLst:
                for dist in range(1, 8):
                    move = (self.loc[0]+i[0]*dist, self.loc[1]+i[1]*dist)
                    if not(0<=move[0]<8 and 0<=move[1]<8): break
                    getSquare = board.grid[int(move[0])][int(move[1])]
                    if getSquare != 0:
                        if getSquare.plyr != self.plyr:
                            if exception == None and self.checkMove(self.loc, move, board, {}): break
                            targets += [move]
                        break
                    elif exception == None and self.checkMove(self.loc, move, board, {}): continue
                    else: moves += [move]
        if (self.type==KNIGHT and exception==None or exception==KNIGHT):
            for i in ((2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)):
                move = (self.loc[0] + i[0], self.loc[1] + i[1])
                if not (0 <= move[0] < 8 and 0 <= move[1] < 8): continue
                getSquare = board.grid[int(move[0])][int(move[1])]
                if getSquare != 0:
                    if getSquare.plyr == self.plyr: continue
                    if exception!=KNIGHT and self.checkMove(self.loc, move, board, {}): continue
                    targets += [move]
                elif exception!=KNIGHT and self.checkMove(self.loc, move, board, {}): continue
                else: moves += [move]
        if (self.type==PAWN and exception==None or exception==PAWN):
            if self.loc[0]>0:
                getSquare = board.grid[int(self.loc[0])-1][int(self.loc[1])]
                if getSquare == 0:
                    if not (exception != PAWN and self.checkMove(self.loc, (self.loc[0] - 1, self.loc[1]), board, {})):
                        moves += [(self.loc[0]-1, self.loc[1])]
                        if self.loc[0]==1: transpawn["{}{}".format(self.loc[0]-1, self.loc[1])] = [QUEEN, ROOK, BISHOP, KNIGHT]
                    get2Square = board.grid[int(self.loc[0]) - 2][int(self.loc[1])]
                    if get2Square == 0 and self.nvrMoved and not(exception!=PAWN and self.checkMove(self.loc, (self.loc[0]-2, self.loc[1]), board, {})):
                        moves += [(self.loc[0] - 2, self.loc[1])]
                for move in [(self.loc[0] - 1, self.loc[1]+1), (self.loc[0] - 1, self.loc[1]-1)]:
                    if not(0 <= move[1] < 8):
                        continue
                    getSquare = board.grid[int(move[0])][int(move[1])]
                    if getSquare != 0 and getSquare.plyr!= self.plyr and not(exception!=PAWN and self.checkMove(self.loc, move, board, {})):
                        targets += [move]
                        if self.loc[0] == 1: transpawn["{}{}".format(move[0], move[1])] = [QUEEN, ROOK, BISHOP, KNIGHT]

        if self.plyr=='B' and exception==None:
            board.rotate()
            moves = [(7-_[0], 7-_[1]) for _ in moves]
            targets = [(7 - _[0], 7 - _[1]) for _ in targets]
            for i in list(castles.keys()):
                in_i = castles[i]
                del castles[i]
                castles[str(7-int(i[0]))+str(7-int(i[1]))] = [in_i[0], (7-in_i[1][0], 7-in_i[1][1])]
            for i in list(transpawn.keys()):
                in_i = transpawn[i]
                del transpawn[i]
                transpawn[str(7-int(i[0]))+str(7-int(i[1]))] = in_i
        return moves, targets, castles, transpawn
    def checkMove(self, fromLoc, move, board, castles):
        moveinfo = board.makeMove(fromLoc, move, castles)
        check = checkforcheck(board.pieces[self.plyr][0], board)
        board.undoMove(*moveinfo)
        if check: return True
        return False

