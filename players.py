from PIECES import *
class player:
    def __init__(self, game, plyr='W'):
        self.game = game
        self.plyr = plyr
        self.pieces = []
        self.createPieces((lambda x:(x[0], x[1])) if plyr=='W' else (lambda x:(7-x[0],x[1])))

    def createPieces(self, modify=lambda x:(x[0], x[1])):

        self.pieces = [
            piece(KING, modify((7,4)), self.plyr, self.game),
            piece(QUEEN, modify((7, 3)), self.plyr, self.game),
            piece(BISHOP, modify((7, 2)), self.plyr, self.game), piece(BISHOP, modify((7, 5)), self.plyr, self.game),
            piece(KNIGHT, modify((7, 1)), self.plyr, self.game), piece(KNIGHT, modify((7, 6)), self.plyr, self.game),
            piece(ROOK, modify((7, 0)), self.plyr, self.game), piece(ROOK, modify((7, 7)), self.plyr, self.game)
        ] + [piece(PAWN, modify((6, _)), self.plyr, self.game) for _ in range(8)]

class AIplayer(player):
    def __init__(self, game, plyr):
        self.plyr = plyr
        self.game = game
        self.pieces = []
        self.createPieces((lambda x:(x[0], x[1])) if plyr=='W' else (lambda x:(7-x[0],x[1])))

        self.funcD = {min:max, max:min}
    def miniMax(self, board, plyr, goal, depth=0, parent_ab_val=float("inf")):
        strBoard = self.BoardToString(board, plyr)
        move = self.storedBoardVals.get(strBoard, "NOTHING")
        if move != "NOTHING":
            return move
        mateinfo = self.game.checkForMate(plyr)
        if mateinfo[0]:
            if mateinfo[1]=="__checkmate__":
                return ((1000 if plyr!=self.plyr else -1000), None, None, None, {})
            else:
                return (0, None, None, None,  {})

        if depth==goal:
            val = self.staticeval(board)
            self.gameVal+=1
            self.storedBoardVals[strBoard] = (val, None, None, None, {})
            return (val, None, None, None, {})
        comparFunc, bestMove = (max, (-float("inf"), None, None, None, {})) if plyr == self.plyr else (min, (float("inf"), None, None, None, {}))
        for _ in board.pieces[plyr]:
            moves, targets, castles, transpawn = _.findMoves(board)
            ogType = _.type
            for _move in moves+targets:
                moveStr = "{}{}".format(_move[0], _move[1])
                TypeVariations = transpawn[moveStr] if moveStr in list(transpawn.keys()) else [_.type]
                for TYPE in TypeVariations:
                    _.type = TYPE
                    moveinfo = board.makeMove(_.loc, _move, castles, ogType)
                    curMove = self.miniMax(board, self.game.nextTurn[plyr], goal, depth+1, bestMove[0])
                    _.type=ogType
                    board.undoMove(*moveinfo)
                    bestMove = comparFunc([bestMove, (curMove[0], _.loc, _move, TYPE, castles)], key=lambda x:x[0])
                    if self.funcD[comparFunc]([parent_ab_val, bestMove[0]]) == parent_ab_val:
                        self.gameVal+=1
                        self.storedBoardVals[strBoard] = bestMove
                        return bestMove
        self.gameVal+=1
        self.storedBoardVals[strBoard] = bestMove
        return bestMove
    def OptimalMove(self, board):
        self.gameVal = 0
        self.storedBoardVals = {}
        moveVal, pieceLoc, move, typ, castles = self.miniMax(board, self.plyr, 2)
        #print moveVal, pieceLoc, move, type, castles
        board.makeMove(pieceLoc, move, castles, typ)
        #print ">>>>>>>++", self.staticeval(board)
        self.game.turn = self.game.nextTurn[self.game.turn]
        isMate, self.game.mateType, self.game.winner = self.game.checkForMate(self.game.turn)
        if isMate:
            self.game.gameOver = True
        self.game.drawBoard()
        #print self.gameVal

    def staticeval(self, board):
        #return len(board.pieces[self.plyr])-len(board.pieces[self.game.nextTurn[self.plyr]])
        calcs = {'W': 0, 'B': 0}
        for i in ['W', 'B']:
            for _ in board.pieces[i]:
                moves, targets, castles, transpawn = _.findMoves(board)
                if transpawn: calcs[i] += 3
                if castles: calcs[i] += 2
                if len(targets) < 4:
                  val = 4-len(targets)
                  for r, c in moves:
                      if val == 0: break
                      calcs[i] += 1 / (((r - 3.5) ** 2 + (c - 3.5) ** 2) ** 0.5 + 10)
                      val -= 1
                for r, c in targets:
                    calcs[i] += 0.1 + 1 / (((r - 3.5) ** 2 + (c - 3.5) ** 2) ** 0.5 + 12)
                if _.type == KING:
                    calcs[i] -= 8 if checkforcheck(_, board) else 0
                    calcs[i] += .3*len(board.pieces) / (((_.loc[0] - 3.5) ** 2 + (_.loc[1] - 3.5) ** 2) ** 0.5 +4 )
                elif _.type == PAWN:
                    calcs[i] += 1 +  1 / ((_.loc[0] if _.plyr=='W' else 8-_.loc[0]) + 8)
                elif _.type in [BISHOP, KNIGHT]:
                    calcs[i] += 3
                elif _.type == ROOK:
                    calcs[i] += 5
                elif _.type == QUEEN:
                    calcs[i] += 9
                calcs[i] += 1 / (((_.loc[0] - 3.5) ** 2 + (_.loc[1] - 3.5) ** 2) ** 0.5 + 36/calcs[i])
        return calcs[self.plyr] - calcs[self.game.nextTurn[self.plyr]]
    def BoardToString(self, board, plyr):
        str1 = plyr
        for i in board.grid:
            for j in i:
                str1 += (j.plyr+j.type[1]) if j!=0 else "0"
        return str1

