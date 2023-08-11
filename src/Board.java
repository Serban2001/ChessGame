import java.io.Serializable;
import java.awt.Point;
import java.util.List;
import java.util.ArrayList;

public class Board implements Serializable, Cloneable {
    private Board previousState = null;
    private Piece.Color turn;
    private List<Piece> pieces = new ArrayList<Piece>();
    
    private Piece inCheck = null;
    private Piece lastMoved = null;
    private Ai ai = null;
    
    public void setAi(Ai computerPlayer) {
        this.ai = computerPlayer;
    }
    
    public Ai getAi() {
        return ai;
    }
    
    public Piece getPieceInCheck() {
        return inCheck;
    }
    
    public Piece getLastMovedPiece() {
        return lastMoved;
    }
    
    public Board(boolean initPieces) {
        turn = Piece.Color.White;
        
        if (initPieces) {    
            pieces.add(new Pawn(new Point(0, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(1, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(2, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(3, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(4, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(5, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(6, 1), Piece.Color.Black));
            pieces.add(new Pawn(new Point(7, 1), Piece.Color.Black));

            pieces.add(new Rook(new Point(0, 0), Piece.Color.Black));
            pieces.add(new Knight(new Point(1, 0), Piece.Color.Black));
            pieces.add(new Bishop(new Point(2, 0), Piece.Color.Black));
            pieces.add(new Queen(new Point(3, 0), Piece.Color.Black));
            pieces.add(new King(new Point(4, 0), Piece.Color.Black));
            pieces.add(new Bishop(new Point(5, 0), Piece.Color.Black));
            pieces.add(new Knight(new Point(6, 0), Piece.Color.Black));
            pieces.add(new Rook(new Point(7, 0), Piece.Color.Black));

            pieces.add(new Pawn(new Point(0, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(1, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(2, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(3, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(4, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(5, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(6, 6), Piece.Color.White));
            pieces.add(new Pawn(new Point(7, 6), Piece.Color.White));

            pieces.add(new Rook(new Point(0, 7), Piece.Color.White));
            pieces.add(new Knight(new Point(1, 7), Piece.Color.White));
            pieces.add(new Bishop(new Point(2, 7), Piece.Color.White));
            pieces.add(new Queen(new Point(3, 7), Piece.Color.White));
            pieces.add(new King(new Point(4, 7), Piece.Color.White));
            pieces.add(new Bishop(new Point(5, 7), Piece.Color.White));
            pieces.add(new Knight(new Point(6, 7), Piece.Color.White));
            pieces.add(new Rook(new Point(7, 7), Piece.Color.White));
        }
    }

    private Board(Piece.Color turn, Board previousState, List<Piece> pieces,
            Piece lastMoved, Piece inCheck, Ai ai) {
        this.turn = turn;
        if (inCheck != null)
            this.inCheck = inCheck.clone();
        if (lastMoved != null)
            this.lastMoved = lastMoved.clone();
        this.ai = ai;
        this.previousState = previousState;
        for(Piece p : pieces) {
            this.pieces.add(p.clone());
        }
    }
    
    public List<Piece> getPieces() {
        return pieces;
    }
    
    public Piece getPieceAt(Point p) {
        for(Piece pc : pieces) {
            if(pc.getLocation().x == p.x &&
               pc.getLocation().y == p.y)
                return pc;
        }
        return null;
    }
    
    public void removePiece(Piece p) {
        if (pieces.contains(p)) {
            pieces.remove(p);
            return;
        }
    }
    
    public void addPiece(Piece p) {
        pieces.add(p);
    }
    
    public void removePieceAt(Point p) {
        Piece temp = null;
        for(Piece pc : pieces) {
            if (pc.getLocation().equals(p)) {
                temp = pc;
                break;
            }
        }
        if (temp != null)
            pieces.remove(temp);
    }
    
    public Piece.Color getTurn() {
        return turn;
    }
    
    public void doMove(Move m, boolean playerMove) {
        this.previousState = this.clone();
        
        for(Piece pc : pieces)
            if (pc.getColor() == turn && pc instanceof Pawn)
                ((Pawn)pc).enPassantOk = false;
        
        if (m instanceof CastleMove) {
            CastleMove c = (CastleMove)m;
            c.getPiece().moveTo(c.getMoveTo());
            c.getRook().moveTo(c.getRookMoveTo());
        } else {
            if(m.getCaptured() != null);
                this.removePiece(m.getCaptured());
            
            if (m.getPiece() instanceof Pawn)
                if (Math.abs(m.getPiece().getLocation().y - m.getMoveTo().y) == 2)
                    ((Pawn)m.getPiece()).enPassantOk = true;                
            
            m.getPiece().moveTo(m.getMoveTo());    
            
            checkPawnPromotion(m.getPiece(), playerMove);
        }
        
        this.lastMoved = m.getPiece();
        this.inCheck = kingInCheck();
        
        turn = Piece.Color.values()[(turn.ordinal() + 1) % 2];
    }
    
    private void checkPawnPromotion(Piece pawn, boolean showDialog) {
        if(pawn instanceof Pawn && (pawn.getLocation().y == 0 || pawn.getLocation().y == 7)) {
            Piece promoted;
            
            if (!showDialog || (ai != null && ai.getColor() == pawn.getColor())) {
                promoted = new Queen(pawn.getLocation(), pawn.getColor());
            } else { 
                Object type = javax.swing.JOptionPane.showInputDialog(
                        null, "", 
                        "Choose promotion:",
                        javax.swing.JOptionPane.QUESTION_MESSAGE,
                        null,
                        new Object[] { "Queen", "Rook", "Bishop", "Knight" },
                        "Queen");
                
                if (type == null)
                    type = "Queen";
                
                if (type.toString().equals("Queen"))
                    promoted = new Queen(pawn.getLocation(), pawn.getColor());
                else if (type.toString().equals("Rook"))
                    promoted = new Rook(pawn.getLocation(), pawn.getColor());
                else if (type.toString().equals("Bishop"))
                    promoted = new Bishop(pawn.getLocation(), pawn.getColor());
                else
                    promoted = new Knight(pawn.getLocation(), pawn.getColor());
            }

            pieces.remove(pawn);
            pieces.add(promoted);
        }
    }
    
    public Board tryMove(Move m) {
        Board helper = this.clone();
        
        if (m instanceof CastleMove) {
            CastleMove c = (CastleMove)m;
            Piece king = helper.getPieceAt(c.getPiece().getLocation());
            Piece rook = helper.getPieceAt(c.getRook().getLocation());
            
            helper.doMove(new CastleMove(king, c.getMoveTo(),
                    rook, c.getRookMoveTo()), false);
        } else {       
            Piece capture = null;
            if(m.getCaptured() != null)
                capture = helper.getPieceAt(m.getCaptured().getLocation());

            Piece moving = helper.getPieceAt(m.getPiece().getLocation());

            helper.doMove(new Move(moving,
                    m.getMoveTo(), capture), false);
        }
        
        return helper;
    }  
    
    private Piece kingInCheck() {
        for(Piece pc : pieces)
            for(Move mv : pc.getValidMoves(this, false))
                if (mv.getCaptured() instanceof King) {
                    this.inCheck = mv.getCaptured();
                    return mv.getCaptured();
                }
        return null;
    }
    
    public boolean movePutsKingInCheck(Move m, Piece.Color kingColor) {
        Board helper = tryMove(m);
        
        for(Piece pc : helper.getPieces())
            if (pc.color != kingColor)
                for(Move mv : pc.getValidMoves(helper, false))
                    if (mv.getCaptured() instanceof King) 
                        return true;
        return false;
    }
    
    public boolean gameOver() {
        List<Move> whiteMoves = new ArrayList<Move>();
        List<Move> blackMoves = new ArrayList<Move>();
        
        for(Piece p : pieces) {
            if(p.getColor() == Piece.Color.White)
                whiteMoves.addAll(p.getValidMoves(this, true));
            else
                blackMoves.addAll(p.getValidMoves(this, true));
        }
        
        return (whiteMoves.size() == 0 || blackMoves.size() == 0);
    }
    
    public Board clone() {
        return new Board(turn, previousState, pieces, lastMoved, inCheck, ai);
    }
    
    public Board getPreviousState() {
        if(previousState != null)
            return previousState;
        return this;
    }
    
    public boolean validLocation(Point p) {
        return (p.x >= 0 && p.x <= 7) && (p.y >= 0 && p.y <= 7);
    }
}
