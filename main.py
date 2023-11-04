import pygame as p
import Chess_Engine
import AI
import button
import os
import sys
from pygame import mixer

mixer.init()
mixer.music.load("Songs&Sounds/MitiS.mp3")
mixer.music.set_volume(0.05)
mixer.music.play(-1)
x = 300
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
p.init()
p.display.set_caption("Chessable App")

board_width = board_height = hist_log_height = 832                                                                      # size of chess board
hist_log_width = 250                                                                                                    # sizes of history log
size = 8                                                                                                                # just like the chess board 8 x 8
sqr = board_width // size                                                                                               # around 100 pixels for each square, just like my images for the pieces
fps = 60                                                                                                                # FPS cap
imgs = {}

menu_height = 500
menu_width = 800
menu = p.display.set_mode((menu_width, menu_height))
menu_font = p.font.SysFont('Verdana', 21, True, False)

whitePlayer_img = p.image.load('Menu/White.png').convert_alpha()
blackPlayer_img = p.image.load('Menu/Black.png').convert_alpha()
white = button.Button(100, 300, whitePlayer_img, 0.6)
black = button.Button(470, 300, blackPlayer_img, 0.6)
humW = menu_font.render("White is Human", True, p.Color("Dark Red"))
humB = menu_font.render("Black is Human", True, p.Color("Dark Red"))
aiW = menu_font.render("White is AI", True, p.Color("Dark Red"))
aiB = menu_font.render("Black is AI", True, p.Color("Dark Red"))
CastAI = menu_font.render("Vs AI: Castling Disabled", True, p.Color("Dark Red"))
CastHum = menu_font.render("Vs Human: Castling Enabled", True, p.Color("Dark Red"))

logo = p.image.load("Menu/Logo.png")

how_to = p.image.load('Menu/How to.png').convert_alpha()
how_to = button.Button(650, 50, how_to, 0.5)
How_to = menu_font.render("How to?", True, p.Color("Dark Red"))

start = p.image.load('Menu/Start.png').convert_alpha()
start = button.Button(340, 430, start, 0.45)

instr_font = p.font.SysFont('Verdana', 18, True, False)

Arrow = p.image.load('Menu/Arrow.png').convert_alpha()
Arrow = button.Button(700, 390, Arrow, 0.25)
Back = instr_font.render("Go Back", True, p.Color("Yellow"))

HorseMoves = p.image.load('Menu/Moves/HorseMoves.png').convert_alpha()
HorseMoves = p.transform.scale(HorseMoves, (100, 100))
HorseText = instr_font.render("Knight Moves", True, p.Color("Green"))
HorseUniq = instr_font.render("L Shape", True, p.Color("Green"))

BishopMoves = p.image.load('Menu/Moves/BishopMoves.png').convert_alpha()
BishopMoves = p.transform.scale(BishopMoves, (100, 100))
BishopText = instr_font.render("Bishop Moves", True, p.Color("Green"))
BishopUniq = instr_font.render("Diagonal", True, p.Color("Green"))

QueenMoves = p.image.load('Menu/Moves/QueenMoves.png').convert_alpha()
QueenMoves = p.transform.scale(QueenMoves, (100, 100))
QueenText = instr_font.render("Queen Moves", True, p.Color("Green"))
QueenUniq = instr_font.render("All ways", True, p.Color("Green"))

RookMoves = p.image.load('Menu/Moves/RookMoves.png').convert_alpha()
RookMoves = p.transform.scale(RookMoves, (100, 100))
RookText = instr_font.render("Rook Moves", True, p.Color("Green"))
RookUniq = instr_font.render("Rectilinear", True, p.Color("Green"))

KingMoves = p.image.load('Menu/Moves/KingMoves.png').convert_alpha()
KingMoves = p.transform.scale(KingMoves, (100, 100))
KingText = instr_font.render("King Moves", True, p.Color("Green"))
KingUniq = instr_font.render("1-Adjacent", True, p.Color("Green"))

CastlingMoves = p.image.load('Menu/Moves/CastlingMoves.png').convert_alpha()
CastlingMoves = p.transform.scale(CastlingMoves, (300, 36))
CastlingText = instr_font.render("Castling", True, p.Color("Green"))

PawnMove1 = p.image.load('Menu/Moves/PawnMoves1.png').convert_alpha()
PawnMove1 = p.transform.scale(PawnMove1, (100, 100))
PawnText1 = instr_font.render("Pawn Move 1", True, p.Color("Green"))

PawnMove2 = p.image.load('Menu/Moves/PawnMoves2.png').convert_alpha()
PawnMove2 = p.transform.scale(PawnMove2, (100, 100))
PawnText2 = instr_font.render("Pawn Move 2", True, p.Color("Green"))

PawnMovePassant = p.image.load('Menu/Moves/PawnMovesPassant.png').convert_alpha()
PawnMovePassant = p.transform.scale(PawnMovePassant, (100, 100))
PawnMovePassantText = instr_font.render("Pawn Move Passant", True, p.Color("Green"))

miniwB = p.image.load("Mini/wB.png")
miniwH = p.image.load("Mini/wH.png")
miniwK = p.image.load("Mini/wK.png")
miniwP = p.image.load("Mini/wP.png")
miniwQ = p.image.load("Mini/wQ.png")
miniwR = p.image.load("Mini/wR.png")

minibB = p.image.load("Mini/bB.png")
minibH = p.image.load("Mini/bH.png")
minibK = p.image.load("Mini/bK.png")
minibP = p.image.load("Mini/bP.png")
minibQ = p.image.load("Mini/bQ.png")
minibR = p.image.load("Mini/bR.png")

coordnrfont = p.font.SysFont('Verdana', 24, True, False)
coordA = coordnrfont.render('a', False, p.Color('Dark Red'))
coordB = coordnrfont.render('b', False, p.Color('Dark Red'))
coordC = coordnrfont.render('c', False, p.Color('Dark Red'))
coordD = coordnrfont.render('d', False, p.Color('Dark Red'))
coordE = coordnrfont.render('e', False, p.Color('Dark Red'))
coordF = coordnrfont.render('f', False, p.Color('Dark Red'))
coordG = coordnrfont.render('g', False, p.Color('Dark Red'))
coordH = coordnrfont.render('h', False, p.Color('Dark Red'))

nr1 = coordnrfont.render('1', False, p.Color('Dark Red'))
nr2 = coordnrfont.render('2', False, p.Color('Dark Red'))
nr3 = coordnrfont.render('3', False, p.Color('Dark Red'))
nr4 = coordnrfont.render('4', False, p.Color('Dark Red'))
nr5 = coordnrfont.render('5', False, p.Color('Dark Red'))
nr6 = coordnrfont.render('6', False, p.Color('Dark Red'))
nr7 = coordnrfont.render('7', False, p.Color('Dark Red'))
nr8 = coordnrfont.render('8', False, p.Color('Dark Red'))



def loadImages():
    pieces = ['wP', 'wR', 'wH', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bH', 'bB', 'bQ', 'bK']
    for piece in pieces:
        imgs[piece] = p.image.load("Piece/" + piece + ".png")


def drawGameState(screen, game, validMoves, currSqr, histLogFont):
    drawBoard(screen)
    highlight(screen, game, validMoves, currSqr)
    drawPieces(screen, game.board)
    drawMoveLog(screen, game, histLogFont)


def drawMoveLog(screen, game, font):
    histLogRect = p.Rect(board_width, 0, hist_log_width, hist_log_height)
    p.draw.rect(screen, p.Color('Dark Blue'), histLogRect)
    histLog = game.histLog
    moveText = []
    paddingX = 5
    paddingY = 5
    Spacing = 5
    moveInRow = 1
    whX = 5
    whY = 5
    blX = 110
    blY = 5
    for i in range(0, len(histLog), 2):
        moveIndex = "        " + str(histLog[i]) + "                "
        if i + 1 < len(histLog):
            moveIndex += str(histLog[i+1])
        moveText.append(moveIndex)
    for i in range(0, len(moveText), moveInRow):
        text = ""
        for j in range(moveInRow):
            if i + j < len(moveText):
                text += moveText[i+j]
        if not game.whiteToMove:
            if text[8] == 'R':
                piece = miniwR
            elif text[8] == 'H':
                piece = miniwH
            elif text[8] == 'B':
                piece = miniwB
            elif text[8] == 'Q':
                piece = miniwQ
            elif text[8] == 'K':
                piece = miniwK
            else:
                piece = miniwP
        elif game.whiteToMove:
            if text[25] == 'R' or text[26] == 'R' or text[27] == 'R':
                piece = minibR
            elif text[25] == 'H' or text[26] == 'H' or text[27] == 'H':
                piece = minibH
            elif text[25] == 'B' or text[26] == 'B' or text[27] == 'B':
                piece = minibB
            elif text[25] == 'Q' or text[26] == 'Q' or text[27] == 'Q':
                piece = minibQ
            elif text[25] == 'K' or text[26] == 'K' or text[27] == 'K':
                piece = minibK
            else:
                piece = minibP
        textObject = font.render(text, False, p.Color('Dark Red'))
        textLocation = histLogRect.move(paddingX, paddingY)
        whLocation = histLogRect.move(whX, whY)
        blLocation = histLogRect.move(blX, blY)
        whY = whY + 30
        blY = blY + 30
        if whY > hist_log_height:
            screen.fill(p.Color("Dark Blue"), (832, 0, 250, 900))
            whY = 5
            blY = 5
            paddingY = -25
        screen.blit(piece, blLocation) if game.whiteToMove else screen.blit(piece, whLocation)
        screen.blit(textObject, textLocation)
        paddingY += textObject.get_height() + Spacing


def drawText(screen, text):
    font = p.font.SysFont("Verdana", 36, True, False)
    textObject = font.render(text, False, p.Color('Black'))
    textLocation = p.Rect(0, 0, board_width, board_height).move(board_width//2 - textObject.get_width()//2, board_width//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Dark Red'))
    screen.blit(textObject, textLocation.move(2, 2))


def drawPieces(screen, board):
    for r in range(size):
        for c in range(size):
            piece = board[r][c]
            if piece != '--':
                screen.blit(imgs[piece], p.Rect(sqr * c, sqr * r, sqr, sqr))


def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color(135, 190, 232)]
    for r in range(size):
        for c in range(size):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(sqr * c, sqr * r, sqr, sqr))
    drawCoords(screen)


def drawCoords(screen):
    screen.blit(coordA, (85, 725))
    screen.blit(coordB, (185, 725))
    screen.blit(coordC, (290, 725))
    screen.blit(coordD, (390, 725))
    screen.blit(coordE, (495, 725))
    screen.blit(coordF, (605, 725))
    screen.blit(coordG, (705, 725))
    screen.blit(coordH, (805, 725))
    screen.blit(nr1, (5, 725))
    screen.blit(nr2, (5, 625))
    screen.blit(nr3, (5, 525))
    screen.blit(nr4, (5, 415))
    screen.blit(nr5, (5, 315))
    screen.blit(nr6, (5, 205))
    screen.blit(nr7, (5, 105))
    screen.blit(nr8, (5, 1))


def highlight(screen, game, validMoves, currSqr):
    if currSqr != ():
        r, c = currSqr
        if game.board[r][c][0] == ('w' if game.whiteToMove else 'b'):                                                   # currSqr is a moveable piece
            s = p.Surface((sqr, sqr))                                                                                   # highlight square
            s.set_alpha(55)
            s.fill(p.Color('Red'))
            screen.blit(s, (c*sqr, r*sqr))
            s.fill(p.Color((102, 0, 204)))                                                                              #highlight moves of piece
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sqr, move.endRow*sqr))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames = 10
    frameCount = (abs(dR) + abs(dC)) * frames
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSQR = p.Rect(move.endCol*sqr, move.endRow*sqr, sqr, sqr)
        p.draw.rect(screen, color, endSQR)
        if move.pieceCaptured != '--':
            if move.isEnpassant:
                EPRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSQR = p.Rect(move.endCol*sqr, EPRow*sqr, sqr, sqr)
            screen.blit(imgs[move.pieceCaptured], endSQR)
        screen.blit(imgs[move.pieceMoved], p.Rect(c*sqr, r*sqr, sqr, sqr))
        p.display.flip()
        clock.tick(60)


def main():
    playerBlack = False
    playerWhite = False
    run_menu = True
    counterBlack = 1
    counterWhite = 1
    menu_pause = True
    menu_state = "menu"
    checkGameOver = 0
    checkDrawStale = 0
    while run_menu:
        menu.fill(p.Color("Dark Blue"))
        if menu_pause:
            if menu_state == "menu":
                menu.blit(logo, (290, 20))
                menu.blit(aiW, (160, 270))
                menu.blit(aiB, (530, 270))
                menu.blit(How_to, (650, 150))
                if white.draw(menu):
                    playerWhite = True
                    counterWhite += 1
                    if counterWhite % 2 != 0:
                        playerWhite = False
                if black.draw(menu):
                    playerBlack = True
                    counterBlack += 1
                    if counterBlack % 2 != 0:
                        playerBlack = False
                if start.draw(menu):
                    run_menu = False
                if how_to.draw(menu):
                    menu_pause = True
                    menu_state = "instr"
                if playerWhite:
                    menu.fill(p.Color("Dark Blue"), (130, 270, 200, 30))
                    menu.blit(humW, (130, 270))
                if playerBlack:
                    menu.fill(p.Color("Dark Blue"), (500, 270, 200, 30))
                    menu.blit(humB, (500, 270))
                if playerBlack or playerWhite:
                    menu.blit(CastAI, (270, 230))
                if playerBlack and playerWhite:
                    menu.fill(p.Color("Dark Blue"), (270, 230, 290, 30))
                    menu.blit(CastHum, (260, 230))
                for event in p.event.get():
                    if event.type == p.QUIT:
                        p.quit()
                        sys.exit()
                p.display.update()
            elif menu_state == 'instr':
                menu.blit(Back, (690, 350))
                menu.blit(HorseText, (30, 10))
                menu.blit(HorseMoves, (45, 40))
                menu.blit(HorseUniq, (50, 150))

                menu.blit(RookText, (195, 10))
                menu.blit(RookMoves, (200, 40))
                menu.blit(RookUniq, (200, 150))

                menu.blit(QueenText, (335, 10))
                menu.blit(QueenMoves, (350, 40))
                menu.blit(QueenUniq, (350, 150))

                menu.blit(BishopText, (485, 10))
                menu.blit(BishopMoves, (500, 40))
                menu.blit(BishopUniq, (505, 150))

                menu.blit(KingText, (650, 10))
                menu.blit(KingMoves, (660, 40))
                menu.blit(KingUniq, (655, 150))

                menu.blit(CastlingText, (240, 370))
                menu.blit(CastlingMoves, (150, 410))

                menu.blit(PawnText1, (60, 200))
                menu.blit(PawnMove1, (70, 240))

                menu.blit(PawnText2, (225, 200))
                menu.blit(PawnMove2, (240, 240))

                menu.blit(PawnMovePassantText, (380, 200))
                menu.blit(PawnMovePassant, (430, 240))

                if Arrow.draw(menu):
                    menu_state = "menu"
                for event in p.event.get():
                    if event.type == p.QUIT:
                        p.quit()
                        sys.exit()
                p.display.update()
    screen = p.display.set_mode((board_width + hist_log_width, board_width))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    histLogFont = p.font.SysFont("Helvetica", 21, True, False)
    mixer.music.pause()
    game = Chess_Engine.GameState()
    validMoves = game.getValidMoves()
    moveMade = False
    animation = False
    loadImages()
    run_game = True
    currSqr = ()
    playerClicks = []                                                                                                   # log of player clicks in tuple form
    gameOver = False
    while run_game:
        playerTurn = (game.whiteToMove and playerWhite) or (not game.whiteToMove and playerBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and playerTurn:
                    location = p.mouse.get_pos()                                                                        # x, y coords of mouse
                    col = location[0] // sqr
                    row = location[1] // sqr
                    if currSqr == (row, col) or col >= 8:                                                            # user clicks twice the same square
                        currSqr = ()                                                                                 # resets the variable
                        playerClicks = []                                                                               # removes it from log of player clicks
                    else:
                        currSqr = (row, col)
                        playerClicks.append(currSqr)                                                                    # adds 1st and 2nd click
                        if len(playerClicks) == 2:                                                                     # after the 2nd click these happen
                            move = Chess_Engine.Move(playerClicks[0], playerClicks[1], game.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    game.makeMove(validMoves[i])
                                    capture = mixer.Sound("Songs&Sounds/Capture.wav")
                                    capture.set_volume(0.1)
                                    mixer.find_channel(True).play(capture)
                                    moveMade = True
                                    animation = True
                                    currSqr = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [currSqr]
            elif e.type == p.KEYDOWN and playerWhite and playerBlack:
                if e.key == p.K_z:                                                                                      # undo a move when you press z
                    game.undoMove()
                    moveMade = True
                    animation = False
                    gameOver = False
        if not gameOver and not playerTurn:
            AIMove = AI.aiMove(game, validMoves)
            AIcapture = mixer.Sound("Songs&Sounds/Capture.wav")
            AIcapture.set_volume(0.1)
            mixer.find_channel(True).play(AIcapture)
            if AIMove is None:
                AIMove = AI.findRandomMove(validMoves)
            game.makeMove(AIMove)
            moveMade = True
            animation = True
        if moveMade:
            if animation:
                animateMove(game.histLog[-1], screen, game.board, clock)
            validMoves = game.getValidMoves()
            moveMade = False
            animation = False
        drawGameState(screen, game, validMoves, currSqr, histLogFont)
        if game.checkMate:
            gameOver = True
            if checkGameOver == 1 and game.whiteToMove:
                drawText(screen, 'Checkmate, Black Wins')
            elif checkGameOver == 1 and not game.whiteToMove:
                drawText(screen, 'Checkmate, White Wins')
            elif checkGameOver == 0:
                trumpets = mixer.Sound("Songs&Sounds/Trumpets.wav")
                trumpets.set_volume(0.1)
                trumpets.play(0)
                checkGameOver = 1
        elif game.staleMate:
            gameOver = True
            if checkDrawStale == 1:
                drawText(screen, 'Draw / Stalemate ')
            elif checkDrawStale == 0:
                shock = mixer.Sound("Songs&Sounds/Shock.wav")
                shock.set_volume(0.1)
                shock.play(0)
                checkDrawStale = 1
        clock.tick(fps)
        p.display.flip()


if __name__ == '__main__':
    main()
