class Board:
    def __init__(self, pieces):
        self.pieces = pieces
        self.grid = [[0 for i in range(8)]for j in range(8)]
        for _ in ['W', 'B']:
            for i in self.pieces[_]:
                self.grid[int(i.loc[0])][int(i.loc[1])] = i
    def rotate(self):
        array = []
        for i in range(8):
            row = []
            for j in range(8):
                row += [self.grid[7-i][7-j]]
                if self.grid[i][j]!=0: self.grid[i][j].loc = (7-self.grid[i][j].loc[0], 7-self.grid[i][j].loc[1])
            array+=[row]
        self.grid = array
    def makeMove(self, fromLoc, move, castles, transPiece=None):
        movingPiece = self.grid[int(fromLoc[0])][int(fromLoc[1])]
        self.grid[int(fromLoc[0])][int(fromLoc[1])] = 0

        killedPiece = self.grid[int(move[0])][int(move[1])]
        if killedPiece != 0: self.pieces[killedPiece.plyr].remove(killedPiece)
        self.grid[int(move[0])][int(move[1])] = movingPiece
        movingPiece.loc = move

        extra = [()]
        if "{}{}".format(move[0], move[1]) in list(castles.keys()):
            rookPiece, rookMove = castles["{}{}".format(move[0], move[1])]
            extra = [(rookPiece, rookPiece.loc)]
            self.grid[int(rookPiece.loc[0])][int(rookPiece.loc[1])] = 0
            self.grid[int(rookMove[0])][int(rookMove[1])] = rookPiece
            rookPiece.loc = rookMove

        extra += [movingPiece.type if transPiece != None else None]
        if transPiece != None: movingPiece.type = transPiece

        returnSet = [movingPiece, fromLoc, killedPiece, move, 0]
        if movingPiece.nvrMoved:
            movingPiece.nvrMoved = False
            returnSet[-1] = 1
        return returnSet + extra
    def undoMove(self, movingPiece, fromLoc, killedPiece, toLoc, firstMove, extraMoves, transPiece):
        if extraMoves:
            self.grid[int(extraMoves[0].loc[0])][int(extraMoves[0].loc[1])] = 0
            self.grid[int(extraMoves[1][0])][int(extraMoves[1][1])] = extraMoves[0]
            extraMoves[0].loc = extraMoves[1]
        if transPiece != None: movingPiece.type = transPiece
        self.grid[int(fromLoc[0])][int(fromLoc[1])] = movingPiece
        movingPiece.loc = fromLoc
        self.grid[int(toLoc[0])][int(toLoc[1])] = killedPiece
        if killedPiece!=0: self.pieces[killedPiece.plyr] += [killedPiece]
        if firstMove: movingPiece.nvrMoved = True
    def delPiece(self, aPiece):
        if aPiece == 0: return
        inGrid = self.grid[int(aPiece.loc[0])][int(aPiece.loc[1])]
        if inGrid == aPiece: self.grid[int(aPiece.loc[0])][int(aPiece.loc[1])] = 0
        #self.pieces[aPiece.plyr].remove(aPiece)
        del aPiece

