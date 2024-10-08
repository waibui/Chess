"""
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible
for determining the valid moves at the current state. It will also keep a move log.
"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        
    def makeMove(self, move):
        """
        This will make the move

        Args:
            move (Move): The move to make
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        
    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            
    def getValidMoves(self):
        """
        Get the valid moves

        Returns:
            _list_: The list of valid moves
        """
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        """
        Get all the possible moves
        """
        move = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of columns
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == "p":
                        self.getPawnMoves(r, c, move)
                    elif piece == "R":
                        self.getRookMoves(r, c, move)
                    elif piece == "N":
                        self.getKnightMoves(r, c, move)
                    elif piece == "B":
                        self.getBishopMoves(r, c, move)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, move)
                    elif piece == "K":
                        self.getKingMoves(r, c, move)
        return move
    
    
    def getPawnMoves(self, r, c, moves):
        pass
    
    def getRookMoves(self, r, c, moves):
        pass
    
    def getKnightMoves(self, r, c, moves):
        pass
    
    def getBishopMoves(self, r, c, moves):
        pass
    
    def getQueenMoves(self, r, c, moves):
        pass
    
    def getKingMoves(self, r, c, moves):
        pass
        
class Move():
    """
    maps keys to values
    """
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)
        
    def __eq__(self, other):
        """
        Check if two moves are equal

        Args:
            other (_Move_): The other move

        Returns:
            bool: __
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID  
        return False
        
    def getChessNotation(self):
        """
        Get the chess notation

        Returns:
            _None_: __
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        """
        Get the rank and file

        Args:
            r (int): The row of the square
            c (int): The column of the square

        Returns:
            str: The rank and file of the square
        """
        return self.colsToFiles[c] + self.rowsToRanks[r]