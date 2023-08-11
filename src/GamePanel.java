import javax.swing.JComponent;
import javax.swing.JOptionPane;
import java.awt.Color;
import java.awt.Point;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.event.MouseListener;
import java.awt.event.MouseEvent;
import javax.imageio.ImageIO;
import java.io.File;
import java.util.List;

public class GamePanel extends JComponent implements MouseListener {
    
    private enum GameStatus {Idle, Error, Started, Checkmate, Stalemate};
    
    GameStatus status = GameStatus.Idle;
    boolean imagesLoaded = false;
    
    Board gameBoard;

    Piece selectedPiece = null;
    Piece invalidPiece = null;
    List<Move> okMoves;
    
    final Color invalidColor = new Color(255, 0, 0, 127);
    final Color selectionColor = new Color(255,255,0,127);
    final Color validMoveColor = new Color(0,255,0,127);
    final Color checkColor = new Color(127,0,255,127);
    final Color lastMovedColor = new Color(0,255,255,75);
    final Color lightColor = new Color(240,215,179,255);
    final Color darkColor = new Color(190,113,73,255);
    
    public GamePanel(int w, int h) {
        this.setSize(w, h);
        loadImages();
        newGame();
        this.addMouseListener(this);
    }    
    
    public void newGame() {
        gameBoard = new Board(true);
        status = GameStatus.Started;
        
        selectedPiece = null;
        invalidPiece = null;

        this.repaint();
    }
    
    public void newAiGame() {       
        int aiDepth;
        Piece.Color aiColor;
        
        Object level = JOptionPane.showInputDialog(this, "Select AI level:", 
                "New 1-Player game",
                JOptionPane.QUESTION_MESSAGE,
                null,
                new Object[] {"Easy", "Normal"},
                "Easy");
        
        if (level == null)
            return;
        else
            if (level.toString().equals("Easy"))
                aiDepth = 2;
            else 
                aiDepth = 3;
           
        Object color = JOptionPane.showInputDialog(this, "Select AI Color:", 
                "New 1-Player game",
                JOptionPane.QUESTION_MESSAGE,
                null,
                new Object[] { "Black", "White" },
                "Black");
        
        if (color == null)
            return;
        else
            if (color.toString().equals("White"))
                aiColor = Piece.Color.White;
            else
                aiColor = Piece.Color.Black;
        
        newGame();
        gameBoard.setAi(new Ai(aiColor, aiDepth));
        
        if (aiColor == Piece.Color.White)
            mousePressed(null);
    }
   
    public void undo() {
        selectedPiece = null;
        invalidPiece = null;
        okMoves = null;
               
        if (gameBoard.getAi() == null)
            gameBoard = gameBoard.getPreviousState();
        else
            if (gameBoard.getTurn() != gameBoard.getAi().getColor())
                gameBoard = gameBoard.getPreviousState().getPreviousState();
            else
                gameBoard = gameBoard.getPreviousState();
        
        status = GameStatus.Started;
        
        this.repaint();      
    }
    
    private void loadImages(){
        try {
            BufferedImage[] whiteImages = new BufferedImage[6];            
            BufferedImage[] blackImages = new BufferedImage[6];

            File directory = new File ("PIECES");
            if (!directory.exists()) {
                if (directory.mkdir()) {
                throw new Exception("The PIECES directory did not exist. " +
                        "It has been created. Ensure that it contains the following files: \n" +
                        "WHITE_PAWN.PNG\n" +
                        "WHITE_KNIGHT.PNG\n" +
                        "WHITE_BISHOP.PNG\n" +
                        "WHITE_ROOK.PNG\n" +
                        "WHITE_QUEEN.PNG\n" +
                        "WHITE_KING.PNG\n" +
                        "BLACK_PAWN.PNG\n" +
                        "BLACK_KNIGHT.PNG\n" +
                        "BLACK_BISHOP.PNG\n" +
                        "BLACK_ROOK.PNG\n" +
                        "BLACK_QUEEN.PNG\n" +
                        "BLACK_KING.PNG");
                }
            }

            whiteImages[0] = ImageIO.read(new File("PIECES/WHITE_PAWN.PNG"));
            whiteImages[1] = ImageIO.read(new File("PIECES/WHITE_KNIGHT.PNG"));
            whiteImages[2] = ImageIO.read(new File("PIECES/WHITE_BISHOP.PNG"));
            whiteImages[3] = ImageIO.read(new File("PIECES/WHITE_ROOK.PNG"));
            whiteImages[4] = ImageIO.read(new File("PIECES/WHITE_QUEEN.PNG"));
            whiteImages[5] = ImageIO.read(new File("PIECES/WHITE_KING.PNG"));
            
            blackImages[0] = ImageIO.read(new File("PIECES/BLACK_PAWN.PNG"));
            blackImages[1] = ImageIO.read(new File("PIECES/BLACK_KNIGHT.PNG"));
            blackImages[2] = ImageIO.read(new File("PIECES/BLACK_BISHOP.PNG"));
            blackImages[3] = ImageIO.read(new File("PIECES/BLACK_ROOK.PNG"));
            blackImages[4] = ImageIO.read(new File("PIECES/BLACK_QUEEN.PNG"));
            blackImages[5] = ImageIO.read(new File("PIECES/BLACK_KING.PNG"));
            
            Piece.setBlackImages(blackImages);
            Piece.setWhiteImages(whiteImages);
            
            imagesLoaded = true;
        } catch (Exception e) {
            status = GameStatus.Error;
            String message = "Could not load piece images. " +
                    "Check that all 12 images exist in the PIECES folder " +
                    "and are accessible to the program.\n" +
                    "The program will not function properly until this is resolved.\n\n" +
                    "Error details: " + e.getMessage();
            JOptionPane.showMessageDialog(this, message, "Error!", JOptionPane.ERROR_MESSAGE);
        }
    }
    
    public void mousePressed(MouseEvent e) { 
        if (status == GameStatus.Started) {
            invalidPiece = null;
            int w = getWidth();
            int h = getHeight();

            if (gameBoard.getAi() == null || 
                gameBoard.getAi().getColor() != gameBoard.getTurn()) { 
                Point boardPt = new Point(e.getPoint().x / (w / 8),
                        e.getPoint().y / (h / 8));

                if(selectedPiece == null) {
                    selectedPiece = gameBoard.getPieceAt(boardPt);
                    if (selectedPiece != null) {  
                        okMoves = selectedPiece.getValidMoves(gameBoard, true);
                        if(selectedPiece.getColor() != gameBoard.getTurn()) {
                            okMoves = null;
                            invalidPiece = selectedPiece;
                            selectedPiece = null;
                        }
                    }
                } else {
                    Move playerMove = moveWithDestination(boardPt);

                    if (playerMove != null) {
                        gameBoard.doMove(playerMove, true);
                        selectedPiece = null;
                        okMoves = null;
                    } else {
                        selectedPiece = null;
                        okMoves = null;
                    }
                }
            }         
            if (gameBoard.getAi() != null && 
                gameBoard.getAi().getColor() == gameBoard.getTurn()) { 
                
                this.paintImmediately(0, 0, this.getWidth(), this.getHeight());
                
                Move computerMove = gameBoard.getAi().getMove(gameBoard);

                if (computerMove != null) {
                    gameBoard.doMove(computerMove, false);
                }
            }
            
            if (gameBoard.gameOver()) {             
                this.paintImmediately(0, 0, this.getWidth(), this.getHeight());
                
                if (gameBoard.getPieceInCheck() == null) {
                    status = GameStatus.Stalemate;
                    JOptionPane.showMessageDialog(this,
                            "Stalemate!",
                            "",
                            JOptionPane.INFORMATION_MESSAGE);
                } else {
                    status = GameStatus.Checkmate; 
                    JOptionPane.showMessageDialog(this,
                            "Checkmate!",
                            "",
                            JOptionPane.INFORMATION_MESSAGE);
                }
                   
            }
            
            this.repaint();
        }       
    }
    
    protected void paintComponent(Graphics gr) {
        int w = getWidth();
        int h = getHeight();

        int sW = w / 8;
        int sH = h / 8;
        
        Image buffer = createImage(w, h);

        Graphics g = buffer.getGraphics();

        drawBoard(g, sW, sH);        
        
        drawHelperCircles(g, sW, sH);
        
        if (imagesLoaded)
            drawPieces(g, sW, sH);

        gr.drawImage(buffer, 0, 0, this);
    }
           
    private void drawHelperCircles(Graphics g, int sW, int sH) {
        if(selectedPiece != null) {     
            Point p = selectedPiece.getLocation();
            g.setColor(selectionColor);
            g.fillOval(p.x * sW, p.y * sH, sW, sH);
            
            g.setColor(validMoveColor);           
            for(Move m : okMoves) {
                Point pt = m.getMoveTo();
                g.fillOval(pt.x * sW, pt.y * sH, sW, sH);
            }
        }
        if(invalidPiece != null) {
            Point p = invalidPiece.getLocation();
            g.setColor(invalidColor);
            g.fillOval(p.x * sW, p.y * sH, sW, sH);
        }
        if (gameBoard.getPieceInCheck() != null) {
            Point p = gameBoard.getPieceInCheck().getLocation();
            g.setColor(checkColor);
            g.fillOval(p.x * sW, p.y * sH, sW, sH);
        }   
        if (gameBoard.getLastMovedPiece() != null) {
            Point p = gameBoard.getLastMovedPiece().getLocation();
            g.setColor(lastMovedColor);
            g.fillOval(p.x * sW, p.y * sH, sW, sH);
        }
    }
    
    private void drawPieces(Graphics g, int sW, int sH) {
        for(Piece pc : gameBoard.getPieces()) {
            if(pc.getColor() == Piece.Color.White) {
                g.drawImage(pc.getWhiteImage(), pc.getLocation().x * sW,
                        pc.getLocation().y * sH, sW, sH, null);
            } else {
                g.drawImage(pc.getBlackImage(), pc.getLocation().x * sW,
                        pc.getLocation().y * sH, sW, sH, null);
            }
        }
    }
    
    private void drawBoard(Graphics g, int sW, int sH) {
        g.setColor(lightColor);
        g.fillRect(0, 0, sW * 8, sH * 8);
        
        boolean dark = false;
        g.setColor(darkColor);
        for(int y = 0; y < 8; y++) {
            for(int x = 0; x < 8; x++) {
                if(dark) {
                    g.fillRect(x * sW, y * sH, sW, sH);
                }
                dark = !dark;
            }         
            dark = !dark;
        }
    }  
    
    private Move moveWithDestination(Point pt) {
        for(Move m : okMoves)
            if(m.getMoveTo().equals(pt)) 
                return m;
        return null;
    }    
    
    public void mouseExited(MouseEvent e) { }    

    public void mouseEntered(MouseEvent e) { } 

    public void mouseReleased(MouseEvent e) { }

    public void mouseClicked(MouseEvent e) { }
}
