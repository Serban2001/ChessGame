import java.awt.Point;
import java.util.List;
import java.io.Serializable;
import java.awt.image.BufferedImage;

public abstract class Piece implements Serializable, Cloneable{
    public static enum Color {White, Black};
    protected static BufferedImage[] whiteImages;
    protected static BufferedImage[] blackImages;
    protected int numMoves;
    protected Color color;
    protected Point location;
    
    public int getNumberOfMoves() {
        return numMoves;
    }    
    
    public Color getColor() {
        return this.color;
    }    
    
    public void moveTo(Point p) {
        this.location = p;
        numMoves++;
    }    
    
    public Point getLocation() {
        return this.location;
    }    
    
    public abstract int getImageNumber() ;
    
    public abstract BufferedImage getWhiteImage() ; 
    
    public abstract BufferedImage getBlackImage() ;   
    
    public abstract List<Move> getValidMoves(Board board, boolean checkKing);   
    
    public abstract Piece clone();   
    
    public static void setWhiteImages(BufferedImage[] images) {
        whiteImages = images;
    } 
    
    public static void setBlackImages(BufferedImage[] images) {
        blackImages = images;
    }
}
