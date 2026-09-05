// ========================================
// PLAYER LOGIC (AI)
// ========================================

const Player = {
    getComputerMove(board, difficulty) {
        const emptyCells = board.getEmptyCells();
        if (emptyCells.length === 0) return null;
        
        switch (difficulty) {
            case DIFFICULTY_EASY:
                return this._easyMove(emptyCells);
            case DIFFICULTY_MEDIUM:
                return this._mediumMove(board, emptyCells);
            case DIFFICULTY_HARD:
                return this._hardMove(board);
            default:
                return this._easyMove(emptyCells);
        }
    },
    
    _easyMove(emptyCells) {
        return emptyCells[Math.floor(Math.random() * emptyCells.length)];
    },
    
    _mediumMove(board, emptyCells) {
        const winMove = this._findWinningMove(board, AI);
        if (winMove !== null) return winMove;
        
        const blockMove = this._findWinningMove(board, HUMAN);
        if (blockMove !== null) return blockMove;
        
        if (Math.random() < 0.6) {
            const optimal = this._hardMove(board);
            if (optimal !== null) return optimal;
        }
        
        return this._easyMove(emptyCells);
    },
    
    _hardMove(board) {
        return this._minimaxMove(board);
    },
    
    _findWinningMove(board, symbol) {
        for (const index of board.getEmptyCells()) {
            board.cells[index] = symbol;
            if (board.checkWin(symbol)) {
                board.cells[index] = null;
                return index;
            }
            board.cells[index] = null;
        }
        return null;
    },
    
    _minimaxMove(board) {
        let bestScore = -Infinity;
        let bestMove = null;
        
        for (const move of board.getEmptyCells()) {
            board.cells[move] = AI;
            const score = this._minimax(board, 0, false);
            board.cells[move] = null;
            
            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
        }
        return bestMove;
    },
    
    _minimax(board, depth, isMaximizing) {
        if (board.checkWin(AI)) return 10 - depth;
        if (board.checkWin(HUMAN)) return -10 + depth;
        if (board.isFull()) return 0;
        
        if (isMaximizing) {
            let bestScore = -Infinity;
            for (const move of board.getEmptyCells()) {
                board.cells[move] = AI;
                const score = this._minimax(board, depth + 1, false);
                board.cells[move] = null;
                bestScore = Math.max(score, bestScore);
            }
            return bestScore;
        } else {
            let bestScore = Infinity;
            for (const move of board.getEmptyCells()) {
                board.cells[move] = HUMAN;
                const score = this._minimax(board, depth + 1, true);
                board.cells[move] = null;
                bestScore = Math.min(score, bestScore);
            }
            return bestScore;
        }
    }
};