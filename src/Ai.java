import java.util.List;
import java.util.ArrayList;
import java.io.Serializable;

public class Ai implements Serializable{
    
    private Piece.Color aiColor;
    private int depth;

    public Ai(Piece.Color color, int depth) {
        this.aiColor = color;
        this.depth = depth;
    }
    
    public Piece.Color getColor() {
        return aiColor;
    }
    
    public Move getMove(Board game) {     
        if (game == null)
            return null;
        if (game.getTurn() != aiColor)
            return null;
        int bestValue = Integer.MIN_VALUE;
        Move bestMove = null;
        
        for (Move m : getMoves(game)) {
            int moveValue = min(game.tryMove(m), depth - 1, bestValue, Integer.MAX_VALUE);
            
            if (moveValue > bestValue || bestValue == Integer.MIN_VALUE) {
                bestValue = moveValue;
                bestMove = m;
            }
        }
        
        return bestMove;
    }
    
    private int max(Board game, int depth, int alpha, int beta) {
        if (depth == 0)
            return valueOfBoard(game);

        List<Move> possibleMoves = getMoves(game);

        if (possibleMoves.size() == 0)
            return valueOfBoard(game);

        for(Move m : possibleMoves) {
            int moveValue = min(game.tryMove(m), depth - 1, alpha, beta);
            
            if (moveValue > alpha) {
                alpha = moveValue;
            }            
            if (alpha >= beta)
                return alpha;
        }

        return alpha;
    }
    
    private int min(Board game, int depth, int alpha, int beta) {
        if (depth == 0)
            return valueOfBoard(game);

        List<Move> possibleMoves = getMoves(game);

        if (possibleMoves.size() == 0)
            return valueOfBoard(game);

        for(Move m : possibleMoves) {
            int moveValue = max(game.tryMove(m), depth - 1, alpha, beta);
            if (moveValue < beta) {
                beta = moveValue;
            }             
            if (alpha >= beta)
                return beta;
        }       
        return beta;
    }
    
    private List<Move> getMoves(Board game) {
        List<Move> moves = new ArrayList<Move>();
        
        for (Piece p : game.getPieces())
            if (p.getColor() == game.getTurn())
                moves.addAll(p.getValidMoves(game, true));
        return moves;
    }
    
    private int valueOfBoard(Board gameBoard) {
        int value = 0;
        int aiPieces = 0;
        int aiMoves = 0;
        int playerPieces = 0;
        int playerMoves = 0;
        int aiCaptures = 0;
        int playerCaptures = 0;

        for(Piece pc : gameBoard.getPieces())
            if(pc.getColor() == aiColor) {
                aiPieces += valueOfPiece(pc);

                if (aiColor == gameBoard.getTurn())
                {
                    List<Move> validMoves = pc.getValidMoves(gameBoard, true);
                    for(Move m : validMoves) {
                        aiMoves++;
                        if (m.getCaptured() != null) {
                            aiCaptures += valueOfPiece(m.getCaptured());
                        }
                    }
                }
            } else {
                playerPieces += valueOfPiece(pc);

                if (aiColor != gameBoard.getTurn())
                {
                    List<Move> validMoves = pc.getValidMoves(gameBoard, true);
                    for(Move m : validMoves) {
                        playerMoves++;
                        if (m.getCaptured() != null) {
                            playerCaptures += valueOfPiece(m.getCaptured());
                        }
                    }
                }
            }

        value = (aiPieces - playerPieces) + (aiMoves - playerMoves)
                + (aiCaptures - playerCaptures);

        if (gameBoard.getTurn() == aiColor && aiMoves == 0)
            value = Integer.MIN_VALUE;
        else if (gameBoard.getTurn() != aiColor && playerMoves == 0)
            value = Integer.MAX_VALUE;
        

        return value;
    }
    
    private int valueOfPiece(Piece pc) {
        return (int)Math.pow(pc.getImageNumber() + 1, 3) * 100;
    }
}
