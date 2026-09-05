// ========================================
// MAIN ENTRY POINT
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    Game.init();
    
    // Cell clicks
    document.getElementById('cells').addEventListener('click', (e) => {
        const cell = e.target.closest('.cell');
        if (cell) {
            Game.onCellClick(parseInt(cell.dataset.index));
        }
    });
    
    // Mode tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const mode = tab.dataset.mode;
            Game.setMode(mode);
            
            const difficultyRow = document.getElementById('difficultyRow');
            if (mode === MODE_PVC) {
                difficultyRow.classList.remove('hidden');
            } else {
                difficultyRow.classList.add('hidden');
            }
        });
    });
    
    // Difficulty pills
    document.querySelectorAll('.pill').forEach(pill => {
        pill.addEventListener('click', () => {
            document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            Game.setDifficulty(pill.dataset.diff);
        });
    });
    
    // New game button
    document.getElementById('newGame').addEventListener('click', () => {
        Game.resetGame();
    });
});