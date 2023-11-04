class GameState:
    def __init__(self):
        # 8 x 8 board with the following symbols:
        # b = black, w = white
        # R = rook , H = horse , B = bishop , Q = queen , K = king , P = pawn
        self.board = [
            ['bR', 'bH', 'bB', 'bQ', 'bK', 'bB', 'bH', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wH', 'wB', 'wQ', 'wK', 'wB', 'wH', 'wR'],
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'H': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True                                                                                         # white will always start first
        self.histLog = []                                                                                               # keep track of the moves you made for undo purposes
        self.whiteKingLocation = (7, 4)                                                                                 # coords for the white king
        self.blackKingLocation = (0, 4)                                                                                 # coords for the black king
        self.checkMate = False                                                                                          # check with this if king is in checkmate
        self.staleMate = False                                                                                          # check with this if king is in stalemate
        self.enpassantPossible = ()                                                                                     # coords for the sqr where enpassant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)                                                # at starting point king has the rights to castle either side, both for black and white
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        # will take and update every time a king / rook move is made there are 16 different combinations of castling rights

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'                                                                 # replaces the original square with blank square
        self.board[move.endRow][move.endCol] = move.pieceMoved                                                          # replaces destination square with the piece
        self.histLog.append(move)                                                                                       # registers moves for undo purposes
        self.whiteToMove = not self.whiteToMove                                                                         # swap players
        if move.pieceMoved == 'wK':                                                                                     # update king coords if need be
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        if move.isPawnPromotion:                                                                                        # pawn promotion
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        if move.isEnpassant:                                                                                            # enpassant
            self.board[move.startRow][move.endCol] = '--'
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:                                         # basically for enpassant the piece moved needs to be a pawn with a 2 square advance from starting point
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)                                  # coords to do a diagonal move
        else:
            self.enpassantPossible = ()
        self.enpassantPossibleLog.append(self.enpassantPossible)
        if move.isCastleMoves:
            if move.endCol - move.startCol == 2:     # ks castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:                                   #qs castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'
        self.updateCastleRight(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def undoMove(self):                                                                                                 # undo
        if len(self.histLog) != 0:                                                                                      # check if log has moves to undo
            move = self.histLog.pop()                                                                                   # then will remove the move made from the histLog
            self.board[move.startRow][move.startCol] = move.pieceMoved                                                  # move back the piece you moved
            self.board[move.endRow][move.endCol] = move.pieceCaptured                                                   # replace the piece you captured
            self.whiteToMove = not self.whiteToMove                                                                     # switches turns to original
            if move.pieceMoved == 'wK':                                                                                 # update king coords if need be
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassant:                                                                                        # enpassant
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.board[move.startRow][move.startCol] = move.pieceMoved
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            self.castleRightLog.pop()                                                                                   # remove the new castle rights
            self.currentCastlingRight = self.castleRightLog[-1]                                                         # set current rights to the latest in log
            if move.isCastleMoves:
                if move.endCol - move.startCol == 2:    # ks castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:                                   #qs castle
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
            self.checkMate = False
            self.staleMate = False

    def getValidMoves(self):
        tempenpassant = self.enpassantPossible                                                                          # aux variable which takes the initial value
        tempcastle = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = self.getAllPossibleMoves()                                                                              # pretty much what it does is it take all moves, valid or invalid
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves)-1, -1, -1):                                                                           # iterates through them backwards
            self.makeMove(moves[i])                                                                                     # makes the move
            self.whiteToMove = not self.whiteToMove                                                                     # changes the turn to black
            if self.inCheck():                                                                                          # if in check even though you shouldn't be
                moves.remove(moves[i])                                                                                  # removes it
            self.whiteToMove = not self.whiteToMove                                                                     # changes the turn to white
            self.undoMove()                                                                                             # undo the move on the board
        if len(moves) == 0:                                                                                             # it means there are no valid moves to make then you're either in check or in stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False                                                                                      # in case you want to undo a move, reset the value back to False
            self.staleMate = False                                                                                      # in case you want to undo a move, reset the value back to False
        self.enpassantPossible = tempenpassant                                                                          # the aux variable by doing all the valid or invalid moves, it may or may not change so we update the enpassant variable
        self.currentCastlingRight = tempcastle
        return moves                                                                                                    # return the valid moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])                         # white king is attacked
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])                         # black king is attacked

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    if piece != '-':
                        self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove and self.board[r][c][0] == 'w':                                                             # white pawn moves
            if self.board[r-1][c] == '--':                                                                              # 1 sqr advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':                                                               # 2 sqr advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':                                                                      #capturing to left
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassant=True))
            if c+1 < len(self.board):
                if self.board[r-1][c+1][0] == 'b':    #capturing to right
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassant=True))
        else:                                                                                                           # black pawn moves
            if self.board[r+1][c] == '--':                                                                              # 1 sqr advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1:
                    if self.board[r+2][c] == '--':                                                                      # 2 sqr advance
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':                                                                      # capturing to left
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassant=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':                                                                      # capturing to right
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassant=True))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2,), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.KingSideCastle(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.QueenSideCastle(r, c, moves)

    def KingSideCastle(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def QueenSideCastle(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def updateCastleRight(self, move):
        if move.pieceMoved == 'wK':                                                                                     # if white king moves, you can't castle
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':                                                                                   # if black king moves, you can't castle
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':                                                                                   # if rook is not on its starting square, you can't castle for black
            if move.startRow == 7:
                if move.startCol == 0:                                                                                  # queen side
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:                                                                                # king side
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':                                                                                   # if rook is not on its starting square, you can't castle for white
            if move.startRow == 0:
                if move.startCol == 0:                                                                                  # queen side
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:                                                                                # king side
                    self.currentCastlingRight.bks = False
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks                                                                                                  # white king side
        self.bks = bks                                                                                                  # black king side
        self.wqs = wqs                                                                                                  # white queen side
        self.bqs = bqs                                                                                                  # black queen side


class Move:
    # maps with key:value
    RankRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    RowRank = {v: k for k, v in RankRow.items()}
    FileCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    ColFile = {v: k for k, v in FileCol.items()}

    def __init__(self, startSq, endSq, board, isEnpassant=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self. startRow][self. startCol]                                                         # piece moved takes coords of starting poz
        self.pieceCaptured = board[self. endRow][self. endCol]                                                          # piece captured takes coords of ending poz
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isCaptured = self.pieceCaptured != '--'
        self.isPawnPromotion = False                                                                                    # pawn promotion
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):            # if you reach the final line for either a black pawn or white pawn you can promote
            self.isPawnPromotion = True
        self.isEnpassant = isEnpassant                                                                                  # enpassant
        if self.isEnpassant:
            self.pieceCaptured = 'wP' if self.pieceCaptured == 'bP' else 'bP'
        self.isCastleMoves = isCastleMove

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        return isinstance(other, Move) and self.moveId == other.moveId                                                  # override to accept letters and digits

    def getChessNote(self):                                                                                             # gets the coords of the piece on the board + 1 cause python starts from 0 -> n-1
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.ColFile[c] + self.RowRank[r]

    '''
    Overriding the string method
    '''
    def __str__(self):
        if self.isCastleMoves:
            return "KSC" if self.endCol == 6 else "QSC"
        endSQR = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1] == 'P':
            if self.isCaptured:
                return self.ColFile[self.startCol] + "X" + endSQR
            else:
                return endSQR

        moveIndex = self.pieceMoved[1]
        if self.isCaptured:
            moveIndex += 'X'
        return moveIndex + endSQR
