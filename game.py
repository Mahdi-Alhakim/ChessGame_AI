from tkinter import *
import tkinter.messagebox, tkinter.simpledialog

from board import *
from players import *
from PIECES import *

class Game:
    def __init__(self, master, cnvs, botOn="n"):
        self.master = master
        self.cnvs = cnvs

        if botOn:
            self.rotateBoard = False
            self.botON = True
        else:
            self.rotateBoard = True
            self.botON = False

        self.plyrs = [player(self, 'W'), player(self, 'B') if not(self.botON) else AIplayer(self, 'B')]
        self.board = Board({'W':self.plyrs[0].pieces, 'B':self.plyrs[1].pieces})

        self.turn = 'W'
        self.nextTurn = {'W':'B', 'B':'W'}
        self.gameOver = False
        self.winner = None
        self.mateType = None
        self.deselectPiece()

        self.master.bind("<Button-1>", self.click)
        self.drawBoard()
    def drawBoard(self):
        self.cnvs.delete("all")
        for _r in range(8):
            for _c in range(8):
                i, j = (7-_r, 7-_c) if (self.rotateBoard and self.turn=='B') else (_r, _c)
                if self.selectedPiece and (i, j) == self.selectedPiece.loc:
                    self.cnvs.create_rectangle(_c*100, _r*100, _c*100+100, _r*100+100, fill="DarkGoldenRod3")
                elif (i, j) in self.selectedMoves:
                    self.cnvs.create_rectangle(_c * 100, _r * 100, _c * 100 + 100, _r * 100 + 100, fill="orange3")
                elif (i, j) in self.selectedTargets:
                    self.cnvs.create_rectangle(_c * 100, _r * 100, _c * 100 + 100, _r * 100 + 100, fill="tomato3")
                elif (i+j)%2:
                    self.cnvs.create_rectangle(_c*100, _r*100, _c*100+100, _r*100+100, fill="gray44")
                if self.board.grid[i][j] != 0:
                    self.board.grid[i][j].draw(self.cnvs, (self.rotateBoard and self.turn=='B'))
        if self.gameOver:
            tkinter.messagebox.showinfo("Game Over", "|'{}'| wins by CHECKMATE!".format(self.winner) if self.mateType=="__checkmate__" else "It's a draw: STALEMATE!")
            self.destroy()
        if self.turn=='B' and self.botON:
            def doAfter2():
                self.plyrs[1].OptimalMove(self.board)
            self.master.after(2, doAfter2)


    def destroy(self):
        global restart
        for i in self.plyrs:
            for _ in i.pieces:
                del _
            del i
        restart = True
        del self

    def click(self, e):
        if self.gameOver or (self.botON and self.turn=='B'): return
        r, c = int(e.y//100), int(e.x//100)
        if self.rotateBoard and self.turn=='B': r, c = 7-r, 7-c
        if not(0<=e.x<800 and 0<=e.y<800): return
        getPiece = self.board.grid[r][c]
        if getPiece==0 or getPiece.plyr!=self.turn:
            if self.selectedPiece != None and (r, c) in self.selectedMoves+self.selectedTargets:
                transPiece = None
                if str(r)+str(c) in list(self.transpawn.keys()):
                    transPiece = eval(str.upper(tkinter.simpledialog.askstring("Promotion", "New Piece: ")))


                moveinfo = self.board.makeMove(self.selectedPiece.loc, (r, c), self.castles, transPiece)

                killed = moveinfo[2]
                self.board.delPiece(killed)
                self.deselectPiece()
                self.turn = self.nextTurn[self.turn]
                isMate, self.mateType, self.winner = self.checkForMate(self.turn)
                if isMate:
                    self.gameOver = True
                self.drawBoard()
            return
        self.selectedPiece = getPiece
        self.selectedMoves, self.selectedTargets, self.castles, self.transpawn = getPiece.findMoves(self.board)
        self.drawBoard()
    def checkForMate(self, plyr):
        for _piece in self.board.pieces[plyr]:
            moves, targets, castles, transpawn = _piece.findMoves(self.board)
            if moves or targets: return False, None, self.nextTurn[plyr]
        # print(checkforcheck(self.board.pieces[plyr][0], self.board, plyr=='B'))
        return True, ("__checkmate__" if checkforcheck(self.board.pieces[plyr][0], self.board, plyr=='B') else "__stalemate__"), self.nextTurn[plyr]

    def deselectPiece(self):
        self.selectedPiece = None
        self.selectedMoves = []
        self.selectedTargets = []
        self.castles = {}
        self.transpawn = {}
