import java.awt.Point;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.ArrayList;

public class King extends Piece{
       
    private final int imageNumber = 5;
    
    public King(Point location, Color color) {
        numMoves = 0;
        this.color = color;
        this.location = location;
    }

    private King(Point location, Color color, int moves) {
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
        return new King(new Point(this.location.x, this.location.y),
                this.color, this.numMoves);
    }
    
    public List<Move> getValidMoves(Board board, boolean checkKing) {
        int x = location.x;
        int y = location.y;

        List<Move> moves = new ArrayList<Move>();

        if (board == null)
            return moves;

        addIfValid(board, moves, new Point(x - 1, y - 1));
        addIfValid(board, moves, new Point(x, y - 1));
        addIfValid(board, moves, new Point(x + 1, y - 1));
        addIfValid(board, moves, new Point(x + 1, y));
        addIfValid(board, moves, new Point(x + 1, y + 1));
        addIfValid(board, moves, new Point(x, y + 1));
        addIfValid(board, moves, new Point(x - 1, y + 1));
        addIfValid(board, moves, new Point(x - 1, y));

        if (this.numMoves == 0) {
            if (checkKing && this != board.getPieceInCheck())
            {
                List<Piece> pieces = board.getPieces();
                List<Piece> okRooks = new ArrayList<Piece>();

                for(int i = 0; i < pieces.size(); i++)
                    if (pieces.get(i).getColor() == this.color &&
                        pieces.get(i) instanceof Rook &&
                        pieces.get(i).getNumberOfMoves() == 0)
                        okRooks.add(pieces.get(i));

                for(Piece p : okRooks) {
                    boolean canCastle = true;
                    if (p.getLocation().x == 7) {
                        for(int ix = this.location.x + 1; ix < 7; ix++) {
                            if (board.getPieceAt(new Point(ix, y)) != null) {
                                canCastle = false;
                                break;
                            }
                        }
                        if (canCastle)
                            moves.add(new CastleMove(this, new Point(x + 2, y),
                                    p, new Point(x + 1, y)));
                    } else if (p.getLocation().x == 0) {
                        for(int ix = this.location.x - 1; ix > 0; ix--) {
                            if (board.getPieceAt(new Point(ix, y)) != null) {
                                canCastle = false;
                                break;
                            }
                        }
                        if (canCastle)
                            moves.add(new CastleMove(this, new Point(x - 2, y),
                                    p, new Point(x - 1, y)));                    
                    }
                }
            }
        }

        if (checkKing)
            for(int i = 0; i < moves.size(); i++)
                if (board.movePutsKingInCheck(moves.get(i), this.color)) {
                    moves.remove(moves.get(i));
                    i--;
                }
        return moves;
    }
    
    private void addIfValid(Board board, List<Move> list, Point pt) {
        if(board.validLocation(pt)) {
            Piece pc = board.getPieceAt(pt);
            if(pc == null || pc.getColor() != this.color) {
                list.add(new Move(this, pt, pc));
            }
        }
    }
}
