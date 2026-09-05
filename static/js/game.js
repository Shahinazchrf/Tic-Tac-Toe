// ========================================
// GAME MANAGER
// ========================================

const Game = {
    board: Board,
    mode: MODE_PVP,
    difficulty: DIFFICULTY_MEDIUM,
    currentPlayer: PLAYER_X,
    gameOver: false,
    scores: { X: 0, O: 0, T: 0 },
    isAIThinking: false,
    
    statusElement: document.getElementById('status'),
    scoreXElement: document.getElementById('scoreX'),
    scoreOElement: document.getElementById('scoreO'),
    scoreTElement: document.getElementById('scoreT'),
    
    init() {
        this.board.init();
        this.currentPlayer = PLAYER_X;
        this.gameOver = false;
        this.isAIThinking = false;
        this.updateStatus();
        this.updateScores();
    },
    
    onCellClick(index) {
        if (this.gameOver) return;
        if (this.board.cells[index] !== null) return;
        if (this.mode === MODE_PVC && this.currentPlayer !== HUMAN) return;
        if (this.isAIThinking) return;
        
        this.board.placeMark(index, this.currentPlayer);
        
        if (this.checkGameOver()) return;
        
        this.switchPlayer();
        this.updateStatus();
        
        if (this.mode === MODE_PVC && this.currentPlayer === AI && !this.gameOver) {
            this.isAIThinking = true;
            setTimeout(() => this.aiTurn(), 450);
        }
    },
    
    aiTurn() {
        if (this.gameOver) {
            this.isAIThinking = false;
            return;
        }
        
        const move = Player.getComputerMove(this.board, this.difficulty);
        
        if (move !== null) {
            this.board.placeMark(move, AI);
            if (this.checkGameOver()) {
                this.isAIThinking = false;
                return;
            }
        }
        
        this.currentPlayer = HUMAN;
        this.isAIThinking = false;
        this.updateStatus();
    },
    
    switchPlayer() {
        this.currentPlayer = this.currentPlayer === PLAYER_X ? PLAYER_O : PLAYER_X;
    },
    
    checkGameOver() {
        const winCombination = this.board.getWinningCombination(this.currentPlayer);
        if (winCombination) {
            this.gameOver = true;
            this.board.drawWinLine(winCombination);
            this.scores[this.currentPlayer]++;
            this.updateScores();
            
            if (this.mode === MODE_PVC) {
                this.statusElement.innerHTML = this.currentPlayer === HUMAN ? 
                    '🎉 <b>you win!</b>' : '🤖 <b>computer wins</b>';
            } else {
                this.statusElement.innerHTML = `🎉 <b>${this.currentPlayer} wins!</b>`;
            }
            return true;
        }
        
        if (this.board.isFull()) {
            this.gameOver = true;
            this.scores.T++;
            this.updateScores();
            this.statusElement.innerHTML = `<b>tie game</b> &mdash; nobody wins`;
            return true;
        }
        
        return false;
    },
    
    updateStatus() {
        if (this.mode === MODE_PVC && this.currentPlayer === AI) {
            this.statusElement.innerHTML = `<b>computer</b> is thinking&hellip;`;
        } else {
            this.statusElement.innerHTML = `Your turn &mdash; <b>${this.currentPlayer}</b>`;
        }
    },
    
    updateScores() {
        this.scoreXElement.textContent = this.scores.X;
        this.scoreOElement.textContent = this.scores.O;
        this.scoreTElement.textContent = this.scores.T;
    },
    
    setMode(mode) {
        this.mode = mode;
        this.resetGame();
    },
    
    setDifficulty(difficulty) {
        this.difficulty = difficulty;
        this.resetGame();
    },
    
    resetGame() {
        this.board.clear();
        this.currentPlayer = PLAYER_X;
        this.gameOver = false;
        this.isAIThinking = false;
        this.updateStatus();
    }
};