import java.awt.Point;
import java.util.List;
import java.util.ArrayList;
import java.awt.image.BufferedImage;

public class Bishop extends Piece{
       
    private final int imageNumber = 2;
    
    public Bishop(Point location, Color color) {
        this.numMoves = 0;
        this.color = color;
        this.location = location;
    }
    
    private Bishop(Point location, Color color, int moves) {
        this.numMoves = moves;
        this.color = color;
        this.location = location;
    }
    
    public int getImageNumber() {
        return imageNumber;
    }
    
    public BufferedImage getWhiteImage() {
        return whiteImages[imageNumber];
    }
    
    public BufferedImage getBlackImage() {
        return blackImages[imageNumber];
    }
    
    public Piece clone() {
        return new Bishop(new Point(this.location.x, this.location.y),
                this.color, this.numMoves);
    }
    
    public List<Move> getValidMoves(Board board, boolean checkKing) {       
        List<Move> moves = new ArrayList<Move>();

        if (board == null)
            return moves;
        
        addMovesInLine(board, moves, 1, 1);
        addMovesInLine(board, moves, -1, 1);
        addMovesInLine(board, moves, 1, -1);
        addMovesInLine(board, moves, -1, -1);

        if (checkKing)
            for(int i = 0; i < moves.size(); i++)
                if (board.movePutsKingInCheck(moves.get(i), this.color)) {
                    moves.remove(moves.get(i));
                    i--;
                }
        return moves;
    }
    
    private void addMovesInLine(Board board, List<Move> moves, int xi, int yi) {
        int x = location.x;
        int y = location.y;
        
        Point pt = new Point(x + xi, y + yi);
        Piece pc;
        
        while(board.validLocation(pt)) {
            pc = board.getPieceAt(pt);
            if(pc == null) {
                moves.add(new Move(this, pt, pc));
            } else if(pc.getColor() != this.color) {
                moves.add(new Move(this, pt, pc));
                break;
            } else {
                break;
            }
            pt = new Point(pt.x + xi, pt.y + yi);
        }
    }
}
